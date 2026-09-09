from __future__ import annotations

import argparse
import base64
import gc
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import torch
from PIL import Image

from codex_vlm_schedules import schedule_response
from search_multiseed_validate import add_maxstack_scores, evaluate_render
from tp2_common import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TARGET_DIR,
    EvalConfig,
    LCMConfig,
    create_run_dir,
    list_target_images,
    load_image,
    load_lcm_pipeline,
    read_csv,
    render_prompt,
    safe_stem,
    seed_from_filename,
    setup_logging,
    write_csv,
    write_json,
)
from tp2_metrics import (
    add_weighted_scores,
    clip_image_embedding,
    load_clip,
    load_lpips,
    pil_to_lpips_tensor,
)


log = setup_logging("tp2.vlm_ronda_13")
log.propagate = False


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Ronda_13 VLM refinement: compare target vs current render through OpenRouter or a manual VLM, "
            "generate prompt variants, render them, evaluate them, and iterate."
        )
    )
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--source-output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Existing outputs root used to resolve anchor renders from best_of_runs.csv.",
    )
    parser.add_argument("--identity", default="ronda_13_vlm_refinement")
    parser.add_argument("--anchor-csv", type=Path, default=DEFAULT_OUTPUT_DIR / "best_of_runs" / "best_of_runs.csv")
    parser.add_argument("--only", nargs="*", default=["1159_25.png"], help="Target filenames. Default: first TP2 target.")
    parser.add_argument("--top-anchors", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--variants-per-call", type=int, default=5)
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it:free")
    parser.add_argument(
        "--fallback-models",
        nargs="*",
        default=[],
        help="Optional OpenRouter models tried after the primary model fails with a retryable error.",
    )
    parser.add_argument("--api-key-env", default="OPENROUTER_API_KEY")
    parser.add_argument("--request-timeout", type=float, default=120.0)
    parser.add_argument("--max-retries", type=int, default=4)
    parser.add_argument("--retry-base-sleep", type=float, default=12.0)
    parser.add_argument("--sleep-between-calls", type=float, default=20.0)
    parser.add_argument("--temperature", type=float, default=0.75)
    parser.add_argument("--max-tokens", type=int, default=1800)
    parser.add_argument(
        "--vlm-provider",
        choices=["openrouter", "stdin", "file", "schedule", "dry-run"],
        default="openrouter",
        help=(
            "Where prompt refinements come from. Use stdin when Codex is acting as the VLM; "
            "use file to poll each iteration directory for a JSON response; "
            "use schedule for the built-in Codex refinement plan."
        ),
    )
    parser.add_argument(
        "--manual-response-name",
        default="codex_response.json",
        help="Filename used by --vlm-provider=file and mirrored for --vlm-provider=stdin.",
    )
    parser.add_argument(
        "--manual-poll-seconds",
        type=float,
        default=2.0,
        help="Polling interval for --vlm-provider=file.",
    )
    parser.add_argument(
        "--manual-timeout",
        type=float,
        default=0.0,
        help="Seconds to wait for --vlm-provider=file. 0 means wait forever.",
    )
    parser.add_argument("--render-device", default="mps", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--metric-device", default="mps", choices=["cuda", "cpu", "mps"])
    parser.add_argument("--clip-model", default=None)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--disable-progress-bar", action="store_true")
    parser.add_argument("--maxstack-scoring", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--dry-run-openrouter",
        action="store_true",
        help="Do not call OpenRouter. Use deterministic placeholder variants for smoke testing.",
    )
    return parser.parse_args()


def image_data_url(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        parsed = json.loads(cleaned[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("VLM response JSON root must be an object.")
    return parsed


def compact_metrics(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    fields = [
        "clip_iisim",
        "lpips_alex",
        "pixel_rmse_01",
        "pixel_ssim_01",
        "color_hist_sim",
        "edge_sim",
        "layout_sim",
        "visual_specific_score",
        "region_score",
        "heuristic_score",
        "selection_score",
        "maxstack_score",
    ]
    result: dict[str, Any] = {}
    for field in fields:
        if field in row:
            value = row[field]
            try:
                result[field] = round(float(value), 6)
            except (TypeError, ValueError):
                result[field] = value
    return result


def prompt_instruction(
    *,
    target_name: str,
    current_prompt: str,
    current_metrics: dict[str, Any],
    iteration: int,
    variants_per_call: int,
    previous_failures: list[str],
) -> str:
    failures_text = "\n".join(f"- {item}" for item in previous_failures[-12:]) or "- none yet"
    prompt_examples = ",\n    ".join(
        f'{{"prompt": "candidate prompt {index}", "reason": "why this variant may improve the render"}}'
        for index in range(1, variants_per_call + 1)
    )
    return f"""
You are refining a discrete text prompt for image-to-prompt inversion.

Target file: {target_name}
Current prompt:
{current_prompt}

Current metrics from the local evaluator:
{json.dumps(current_metrics, indent=2)}

Previous variant prompts that did not win this anchor chain:
{failures_text}

Task:
1. Describe the TARGET image in exhaustive visual detail. On iteration 1 this description must be especially detailed, because it becomes the visual reference for the refinement chain.
2. Describe the CURRENT GENERATED image in detail.
3. Identify detailed visual differences between the generated image and the target: object count, composition, colors, pose, background, materials, scale, lighting, crop, and style.
4. Preserve prompt terms that are clearly working.
5. Produce exactly {variants_per_call} new English prompts for the same fixed LCM renderer.

Hard constraints:
- Final prompts must be plain discrete text prompts, not instructions.
- No negative prompt. Do not use phrases like "not", "avoid", "without", or "no wings" inside the final prompts.
- Do not mention "target image", "current image", "generated image", metrics, CLIP, LPIPS, or iteration inside the final prompts.
- Each prompt should be <= 75 words.
- Keep prompts concrete, visual, and render-friendly for a 768x768 LCM Dreamshaper image.
- Prefer small controlled edits over completely changing the subject.

Return only valid JSON with this exact structure:
{{
  "target_description_detailed": "long, concrete visual description of the target image",
  "current_image_description_detailed": "long, concrete visual description of the current generated image",
  "detailed_visual_differences": {{
    "composition_and_crop": ["specific difference"],
    "main_subject": ["specific difference"],
    "objects_and_props": ["specific difference"],
    "color_and_lighting": ["specific difference"],
    "texture_and_materials": ["specific difference"]
  }},
  "visual_differences": ["short difference 1", "short difference 2"],
  "terms_to_keep": ["term 1", "term 2"],
  "terms_to_change": ["term 1", "term 2"],
  "strategy": "one short sentence",
  "prompt_revision_plan": ["specific edit to make in the next prompt"],
  "prompts": [
    {prompt_examples}
  ]
}}
""".strip()


def openrouter_payload(
    *,
    model: str,
    target_image: Path,
    current_image: Path,
    instruction: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    return {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise vision-language prompt refiner. "
                    "You compare two images and return strict JSON only."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "TARGET image:"},
                    {"type": "image_url", "image_url": {"url": image_data_url(target_image)}},
                    {"type": "text", "text": "CURRENT GENERATED image:"},
                    {"type": "image_url", "image_url": {"url": image_data_url(current_image)}},
                    {"type": "text", "text": instruction},
                ],
            },
        ],
    }


def call_openrouter_once(
    *,
    api_key: str,
    payload: dict[str, Any],
    timeout: float,
    max_retries: int,
    retry_base_sleep: float,
) -> tuple[dict[str, Any], str]:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost/tp2-ronda_13-vlm",
        "X-Title": "TP2 Ronda_13 VLM Refinement",
    }
    last_error = ""
    for attempt in range(1, max_retries + 1):
        request = urllib.request.Request(OPENROUTER_URL, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
            content = parsed["choices"][0]["message"]["content"]
            if not isinstance(content, str):
                content = json.dumps(content)
            return parsed, content
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code}: {detail[:1000]}"
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            sleep_s = float(retry_after) if retry_after and retry_after.isdigit() else retry_base_sleep * attempt
            if exc.code not in {408, 409, 425, 429, 500, 502, 503, 504} or attempt == max_retries:
                raise RuntimeError(last_error) from exc
            log.info("OpenRouter retry %d/%d after %ss due to %s", attempt, max_retries, sleep_s, last_error)
            time.sleep(sleep_s)
        except (TimeoutError, urllib.error.URLError) as exc:
            last_error = str(exc)
            if attempt == max_retries:
                raise RuntimeError(last_error) from exc
            sleep_s = retry_base_sleep * attempt
            log.info("OpenRouter retry %d/%d after %ss due to timeout/network error", attempt, max_retries, sleep_s)
            time.sleep(sleep_s)
    raise RuntimeError(last_error or "OpenRouter call failed")


def call_openrouter_with_fallbacks(
    *,
    api_key: str,
    base_payload: dict[str, Any],
    models: list[str],
    timeout: float,
    max_retries: int,
    retry_base_sleep: float,
) -> tuple[dict[str, Any], str, str]:
    errors: list[str] = []
    for model in models:
        payload = dict(base_payload)
        payload["model"] = model
        log.info("Trying OpenRouter model: %s", model)
        try:
            parsed, content = call_openrouter_once(
                api_key=api_key,
                payload=payload,
                timeout=timeout,
                max_retries=max_retries,
                retry_base_sleep=retry_base_sleep,
            )
            return parsed, content, model
        except RuntimeError as exc:
            errors.append(f"{model}: {exc}")
            log.info("OpenRouter model failed: %s", errors[-1][:500])
    raise RuntimeError("All OpenRouter models failed:\n" + "\n".join(errors))


def placeholder_vlm_response(current_prompt: str, variants_per_call: int, iteration: int) -> dict[str, Any]:
    prompts = []
    suffixes = [
        "balanced composition, faithful colors, clean square crop",
        "closer object scale, matching background, soft realistic lighting",
        "clearer silhouette, accurate color placement, compact subject",
        "stronger local details, similar texture, centered framing",
        "refined visual structure, matching style, simple background",
    ]
    for index in range(variants_per_call):
        prompts.append({
            "prompt": f"{current_prompt}, {suffixes[index % len(suffixes)]}",
            "reason": f"dry-run placeholder variant {index + 1} for iteration {iteration}",
        })
    return {
        "target_description_detailed": "dry run: no target image analysis",
        "current_image_description_detailed": "dry run: no current image analysis",
        "detailed_visual_differences": {
            "composition_and_crop": ["dry run: no model call"],
            "main_subject": [],
            "objects_and_props": [],
            "color_and_lighting": [],
            "texture_and_materials": [],
        },
        "visual_differences": ["dry run: no model call"],
        "terms_to_keep": [],
        "terms_to_change": [],
        "strategy": "dry run placeholder",
        "prompt_revision_plan": ["dry run placeholder"],
        "prompts": prompts,
    }


def manual_response_template(variants_per_call: int) -> dict[str, Any]:
    return {
        "target_description_detailed": "very detailed target image description",
        "current_image_description_detailed": "detailed current generated image description",
        "detailed_visual_differences": {
            "composition_and_crop": ["precise mismatch in framing/layout"],
            "main_subject": ["precise mismatch in the main subject"],
            "objects_and_props": ["precise mismatch in objects/props"],
            "color_and_lighting": ["precise mismatch in color/lighting"],
            "texture_and_materials": ["precise mismatch in texture/materials"],
        },
        "visual_differences": ["main visible mismatch", "secondary visible mismatch"],
        "terms_to_keep": ["working phrase from current prompt"],
        "terms_to_change": ["phrase to refine"],
        "strategy": "one short sentence explaining the next prompt edit",
        "prompt_revision_plan": ["concrete edit applied to the next prompt"],
        "prompts": [
            {
                "prompt": f"candidate prompt {index}",
                "reason": "why this prompt should move the render closer to the target",
            }
            for index in range(1, variants_per_call + 1)
        ],
    }


def write_manual_response_template(iteration_dir: Path, variants_per_call: int, response_name: str) -> Path:
    template_path = iteration_dir / f"{Path(response_name).stem}_template.json"
    write_json(template_path, manual_response_template(variants_per_call))
    return template_path


def read_stdin_vlm_response(
    *,
    iteration_dir: Path,
    target_image: Path,
    current_image: Path,
    variants_per_call: int,
    response_name: str,
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    template_path = write_manual_response_template(iteration_dir, variants_per_call, response_name)
    response_path = iteration_dir / response_name
    marker = "END_JSON"
    log.info("Manual VLM request ready: %s", iteration_dir / "vlm_request.json")
    sys.stdout.write(
        "\n"
        "CODEX_VLM_REQUEST\n"
        f"request_json={iteration_dir / 'vlm_request.json'}\n"
        f"target_image={target_image}\n"
        f"current_image={current_image}\n"
        f"response_template={template_path}\n"
        f"Paste one JSON response, then a line with only {marker}.\n"
    )
    sys.stdout.flush()

    lines: list[str] = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            raise RuntimeError("stdin closed while waiting for manual VLM JSON.")
        if line.strip() == marker:
            break
        lines.append(line)
    raw_content = "".join(lines).strip()
    parsed = extract_json_object(raw_content)
    write_json(response_path, parsed)
    return {"provider": "stdin", "response_file": str(response_path)}, raw_content, parsed


def wait_for_file_vlm_response(
    *,
    iteration_dir: Path,
    variants_per_call: int,
    response_name: str,
    poll_seconds: float,
    timeout_seconds: float,
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    template_path = write_manual_response_template(iteration_dir, variants_per_call, response_name)
    response_path = iteration_dir / response_name
    log.info("Waiting for manual VLM response file: %s", response_path)
    log.info("Response template: %s", template_path)
    start = time.time()
    while not response_path.exists():
        if timeout_seconds > 0 and time.time() - start > timeout_seconds:
            raise TimeoutError(f"Timed out waiting for {response_path}")
        time.sleep(max(0.1, poll_seconds))
    raw_content = response_path.read_text(encoding="utf-8")
    parsed = extract_json_object(raw_content)
    return {"provider": "file", "response_file": str(response_path)}, raw_content, parsed


def normalise_prompt_items(parsed: dict[str, Any], variants_per_call: int) -> list[dict[str, str]]:
    raw_items = parsed.get("prompts")
    if not isinstance(raw_items, list):
        raise ValueError("VLM JSON did not contain a prompts list.")
    items: list[dict[str, str]] = []
    for item in raw_items:
        if isinstance(item, str):
            prompt = item
            reason = ""
        elif isinstance(item, dict):
            prompt = str(item.get("prompt", "")).strip()
            reason = str(item.get("reason", "")).strip()
        else:
            continue
        if prompt:
            items.append({"prompt": prompt, "reason": reason})
    if len(items) < variants_per_call:
        raise ValueError(f"Expected {variants_per_call} prompts, got {len(items)}.")
    return items[:variants_per_call]


def resolve_render_path(row: dict[str, str], output_dir: Path, preview_dir: Path) -> Path | None:
    for key in ("render_path", "render"):
        raw = row.get(key)
        if raw:
            candidate = Path(raw)
            if candidate.exists():
                return candidate
    target_name = row.get("target_name", "")
    run_name = row.get("run_name", "")
    candidate_index = row.get("candidate_index", "")
    if run_name and target_name and candidate_index:
        try:
            index = int(float(candidate_index))
        except ValueError:
            index = -1
        if index >= 0:
            pattern = f"rank_*_candidate_{index:03d}.png"
            matches = sorted((output_dir / run_name / safe_stem(target_name)).glob(pattern))
            if matches:
                return matches[0]
            preview_pattern = f"{Path(target_name).stem}_rank*_{run_name}_cand{index:03d}.png"
            preview_matches = sorted(preview_dir.glob(preview_pattern))
            if preview_matches:
                return preview_matches[0]
    return None


def load_anchor_rows(args: argparse.Namespace, target_name: str) -> list[dict[str, str]]:
    if not args.anchor_csv.exists():
        raise FileNotFoundError(args.anchor_csv)
    rows = [row for row in read_csv(args.anchor_csv) if row.get("target_name") == target_name]
    if not rows:
        raise ValueError(f"No anchor rows found for {target_name} in {args.anchor_csv}")

    def sort_key(row: dict[str, str]) -> tuple[float, float, float]:
        def as_float(value: str, fallback: float) -> float:
            try:
                return float(value)
            except (TypeError, ValueError):
                return fallback

        cross_rank = as_float(row.get("cross_run_rank", ""), 1e9)
        cross_score = as_float(row.get("cross_run_score", ""), -1.0)
        rank = as_float(row.get("rank", ""), 1e9)
        return cross_rank, -cross_score, rank

    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for row in sorted(rows, key=sort_key):
        prompt = row.get("prompt", "").strip()
        if not prompt or prompt in seen:
            continue
        seen.add(prompt)
        unique.append(row)
        if len(unique) >= args.top_anchors:
            break
    return unique


def save_safe_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() == destination.resolve():
        return
    shutil.copy2(source, destination)


def release_torch_cache() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        try:
            torch.mps.empty_cache()
        except RuntimeError:
            pass


def evaluate_image_path(
    *,
    target_name: str,
    target_path: Path,
    target_image: Image.Image,
    target_clip: torch.Tensor,
    target_lpips: torch.Tensor,
    render_path: Path,
    entry: dict[str, str],
    candidate_index: int,
    seed: int,
    stage: str,
    clip_processor: Any,
    clip_model: Any,
    lpips_model: Any,
    metric_device: str,
    eval_cfg: EvalConfig,
    config: LCMConfig,
    use_maxstack: bool,
) -> dict[str, Any]:
    render_image = load_image(render_path)
    row = evaluate_render(
        target_name=target_name,
        target_path=target_path,
        target_image=target_image,
        target_clip=target_clip,
        target_lpips=target_lpips,
        render_image=render_image,
        entry=entry,
        candidate_index=candidate_index,
        seed=seed,
        seed_role="fixed",
        stage=stage,
        clip_processor=clip_processor,
        clip_model=clip_model,
        lpips_model=lpips_model,
        metric_device=metric_device,
        eval_cfg=eval_cfg,
        config=config,
        use_maxstack=use_maxstack,
    )
    row["render_path"] = str(render_path)
    return row


def main() -> Path:
    args = parse_args()
    vlm_provider = "dry-run" if args.dry_run_openrouter else args.vlm_provider
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    if args.render_device == "mps" or args.metric_device == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError(
                "MPS was requested, but torch.backends.mps.is_available() is False in this Python environment. "
                "Use CPU/CUDA or fix the local PyTorch/MPS installation before running this script."
            )

    api_key = os.environ.get(args.api_key_env, "")
    if vlm_provider == "openrouter" and not api_key:
        raise RuntimeError(
            f"Missing {args.api_key_env}. Export the OpenRouter key in the environment; "
            "the script intentionally does not store API keys in source files."
        )

    targets = list_target_images(args.targets)
    if args.only:
        wanted = set(args.only)
        targets = [path for path in targets if path.name in wanted]
    if not targets:
        raise FileNotFoundError(f"No targets matched {args.only or args.targets}")

    config = LCMConfig()
    eval_cfg = EvalConfig(clip_model=args.clip_model or EvalConfig.clip_model)
    run_dir = create_run_dir(args.output_dir, args.identity)
    preview_dir = args.source_output_dir / "final_selection_preview"
    log.info("Run directory: %s", run_dir)
    log.info("VLM provider: %s", vlm_provider)
    if vlm_provider == "openrouter":
        log.info("OpenRouter model: %s", args.model)
    log.info("Targets: %s", ", ".join(path.name for path in targets))
    log.info("Top anchors: %d | iterations: %d | variants/call: %d", args.top_anchors, args.iterations, args.variants_per_call)
    if vlm_provider == "openrouter":
        log.info("Timeout: %.1fs | retries: %d | sleep between calls: %.1fs", args.request_timeout, args.max_retries, args.sleep_between_calls)

    log.info("Loading LCM renderer...")
    pipe, render_device = load_lcm_pipeline(config, args.render_device)
    if hasattr(pipe, "set_progress_bar_config"):
        pipe.set_progress_bar_config(disable=args.disable_progress_bar)
    log.info("Renderer device: %s", render_device)

    log.info("Loading evaluation models...")
    clip_processor, clip_model = load_clip(eval_cfg.clip_model, args.metric_device, local_files_only=args.offline)
    lpips_model = load_lpips(eval_cfg.lpips_net, args.metric_device)
    log.info("Metric device: %s", args.metric_device)

    all_generated_rows: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []
    generated_prompt_bank: dict[str, list[dict[str, str]]] = {}
    trace_index: list[dict[str, Any]] = []

    for target_path in targets:
        target_name = target_path.name
        target_dir = run_dir / safe_stem(target_path)
        target_dir.mkdir(parents=True, exist_ok=True)
        save_safe_copy(target_path, target_dir / "target.png")

        target_image = load_image(target_path)
        target_clip = clip_image_embedding(target_image, clip_processor, clip_model, args.metric_device)
        target_lpips = pil_to_lpips_tensor(target_image, args.metric_device)
        fixed_seed = seed_from_filename(target_path, config.seed)
        anchor_rows = load_anchor_rows(args, target_name)
        generated_prompt_bank[target_name] = []
        log.info("[%s] Loaded %d anchor rows from %s", target_name, len(anchor_rows), args.anchor_csv)

        for anchor_number, anchor_row in enumerate(anchor_rows, start=1):
            anchor_dir = target_dir / f"anchor_{anchor_number:02d}"
            anchor_dir.mkdir(parents=True, exist_ok=True)
            prompt = anchor_row["prompt"].strip()
            anchor_render = resolve_render_path(anchor_row, args.source_output_dir, preview_dir)
            current_image_path = anchor_dir / "iteration_00_start.png"
            if anchor_render and anchor_render.exists():
                save_safe_copy(anchor_render, current_image_path)
                log.info("[%s anchor %02d] Copied initial render: %s", target_name, anchor_number, anchor_render)
            else:
                log.info("[%s anchor %02d] Initial render not found locally; rendering anchor prompt", target_name, anchor_number)
                image = render_prompt(prompt, seed=fixed_seed, pipe=pipe, config=config, device=render_device)
                image.save(current_image_path)

            current_entry = {
                "id": f"{safe_stem(target_name)}_anchor{anchor_number:02d}_current",
                "prompt": prompt,
                "negative_prompt": "",
                "source": f"ronda_13_anchor:{anchor_row.get('run_name', 'unknown')}",
            }
            current_metrics = evaluate_image_path(
                target_name=target_name,
                target_path=target_path,
                target_image=target_image,
                target_clip=target_clip,
                target_lpips=target_lpips,
                render_path=current_image_path,
                entry=current_entry,
                candidate_index=0,
                seed=fixed_seed,
                stage="iteration_00_anchor",
                clip_processor=clip_processor,
                clip_model=clip_model,
                lpips_model=lpips_model,
                metric_device=args.metric_device,
                eval_cfg=eval_cfg,
                config=config,
                use_maxstack=args.maxstack_scoring,
            )
            write_json(anchor_dir / "anchor.json", {
                "target_name": target_name,
                "fixed_seed": fixed_seed,
                "anchor_number": anchor_number,
                "source_row": anchor_row,
                "initial_prompt": prompt,
                "initial_render_path": str(current_image_path),
                "initial_metrics": compact_metrics(current_metrics),
            })
            trace_path = anchor_dir / "vlm_trace.json"
            trace: dict[str, Any] = {
                "target_name": target_name,
                "anchor_number": anchor_number,
                "fixed_seed": fixed_seed,
                "source_row": anchor_row,
                "initial": {
                    "prompt": prompt,
                    "render_path": str(current_image_path),
                    "metrics": compact_metrics(current_metrics),
                },
                "iterations": [],
            }
            write_json(trace_path, trace)
            trace_index.append({
                "target_name": target_name,
                "anchor_number": anchor_number,
                "trace_path": str(trace_path),
                "initial_prompt": prompt,
                "initial_render_path": str(current_image_path),
                "initial_metrics": compact_metrics(current_metrics),
            })

            rejected_prompts: list[str] = []
            for iteration in range(1, args.iterations + 1):
                iteration_dir = anchor_dir / f"iteration_{iteration:02d}"
                renders_dir = iteration_dir / "renders"
                renders_dir.mkdir(parents=True, exist_ok=True)
                log.info("[%s anchor %02d iter %02d] Preparing VLM request", target_name, anchor_number, iteration)

                instruction = prompt_instruction(
                    target_name=target_name,
                    current_prompt=current_entry["prompt"],
                    current_metrics=compact_metrics(current_metrics),
                    iteration=iteration,
                    variants_per_call=args.variants_per_call,
                    previous_failures=rejected_prompts,
                )
                request_meta = {
                    "vlm_provider": vlm_provider,
                    "model": args.model,
                    "fallback_models": args.fallback_models,
                    "target_image": str(target_dir / "target.png"),
                    "current_image": str(current_image_path),
                    "current_prompt": current_entry["prompt"],
                    "current_metrics": compact_metrics(current_metrics),
                    "expected_variants": args.variants_per_call,
                    "response_schema": manual_response_template(args.variants_per_call),
                    "instruction": instruction,
                }
                write_json(iteration_dir / "vlm_request.json", request_meta)

                if vlm_provider == "dry-run":
                    parsed_response = placeholder_vlm_response(current_entry["prompt"], args.variants_per_call, iteration)
                    raw_content = json.dumps(parsed_response, indent=2)
                    api_response: dict[str, Any] = {"provider": "dry-run"}
                elif vlm_provider == "schedule":
                    parsed_response = schedule_response(
                        target_name=target_name,
                        current_prompt=current_entry["prompt"],
                        iteration=iteration,
                        variants_per_call=args.variants_per_call,
                    )
                    raw_content = json.dumps(parsed_response, indent=2)
                    api_response = {"provider": "schedule", "schedule_iteration": iteration}
                elif vlm_provider == "stdin":
                    api_response, raw_content, parsed_response = read_stdin_vlm_response(
                        iteration_dir=iteration_dir,
                        target_image=target_dir / "target.png",
                        current_image=current_image_path,
                        variants_per_call=args.variants_per_call,
                        response_name=args.manual_response_name,
                    )
                elif vlm_provider == "file":
                    api_response, raw_content, parsed_response = wait_for_file_vlm_response(
                        iteration_dir=iteration_dir,
                        variants_per_call=args.variants_per_call,
                        response_name=args.manual_response_name,
                        poll_seconds=args.manual_poll_seconds,
                        timeout_seconds=args.manual_timeout,
                    )
                else:
                    payload = openrouter_payload(
                        model=args.model,
                        target_image=target_dir / "target.png",
                        current_image=current_image_path,
                        instruction=instruction,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
                    log.info("[%s anchor %02d iter %02d] Calling OpenRouter", target_name, anchor_number, iteration)
                    api_response, raw_content, used_model = call_openrouter_with_fallbacks(
                        api_key=api_key,
                        base_payload=payload,
                        models=[args.model, *args.fallback_models],
                        timeout=args.request_timeout,
                        max_retries=args.max_retries,
                        retry_base_sleep=args.retry_base_sleep,
                    )
                    log.info("[%s anchor %02d iter %02d] OpenRouter model used: %s", target_name, anchor_number, iteration, used_model)
                    api_response["ronda_13_model_used"] = used_model
                    parsed_response = extract_json_object(raw_content)

                write_json(iteration_dir / "vlm_response_meta.json", api_response)
                (iteration_dir / "vlm_content.txt").write_text(raw_content, encoding="utf-8")
                if vlm_provider == "openrouter":
                    write_json(iteration_dir / "openrouter_response.json", api_response)
                    (iteration_dir / "openrouter_content.txt").write_text(raw_content, encoding="utf-8")
                elif vlm_provider in {"stdin", "file"}:
                    write_json(iteration_dir / args.manual_response_name, parsed_response)
                write_json(iteration_dir / "parsed_response.json", parsed_response)
                prompt_items = normalise_prompt_items(parsed_response, args.variants_per_call)
                write_json(iteration_dir / "prompt_variants.json", prompt_items)
                log.info("[%s anchor %02d iter %02d] Received %d prompt variants", target_name, anchor_number, iteration, len(prompt_items))

                baseline_row = dict(current_metrics)
                baseline_row["variant_index"] = 0
                baseline_row["variant_role"] = "baseline_current"
                baseline_row["anchor_number"] = anchor_number
                baseline_row["iteration"] = iteration
                iteration_rows = [baseline_row]

                for variant_index, item in enumerate(prompt_items, start=1):
                    entry = {
                        "id": f"{safe_stem(target_name)}_a{anchor_number:02d}_i{iteration:02d}_v{variant_index:02d}",
                        "prompt": item["prompt"],
                        "negative_prompt": "",
                        "source": "ronda_13_vlm_refinement",
                    }
                    image_path = renders_dir / f"variant_{variant_index:02d}.png"
                    log.info("[%s anchor %02d iter %02d] Rendering variant %02d", target_name, anchor_number, iteration, variant_index)
                    image = render_prompt(entry["prompt"], seed=fixed_seed, pipe=pipe, config=config, device=render_device)
                    image.save(image_path)
                    row = evaluate_image_path(
                        target_name=target_name,
                        target_path=target_path,
                        target_image=target_image,
                        target_clip=target_clip,
                        target_lpips=target_lpips,
                        render_path=image_path,
                        entry=entry,
                        candidate_index=variant_index,
                        seed=fixed_seed,
                        stage=f"iteration_{iteration:02d}_variant",
                        clip_processor=clip_processor,
                        clip_model=clip_model,
                        lpips_model=lpips_model,
                        metric_device=args.metric_device,
                        eval_cfg=eval_cfg,
                        config=config,
                        use_maxstack=args.maxstack_scoring,
                    )
                    row["variant_index"] = variant_index
                    row["variant_role"] = "vlm_variant"
                    row["anchor_number"] = anchor_number
                    row["iteration"] = iteration
                    row["vlm_reason"] = item.get("reason", "")
                    iteration_rows.append(row)
                    release_torch_cache()
                    generated_prompt_bank[target_name].append({
                        "id": entry["id"],
                        "prompt": entry["prompt"],
                        "negative_prompt": "",
                        "source": "ronda_13_vlm_refinement",
                        "anchor_number": str(anchor_number),
                        "iteration": str(iteration),
                        "variant_index": str(variant_index),
                        "reason": item.get("reason", ""),
                        "render_path": str(image_path),
                    })

                add_weighted_scores(iteration_rows)
                if args.maxstack_scoring:
                    add_maxstack_scores(iteration_rows)
                ranking_field = "maxstack_score" if args.maxstack_scoring else "selection_score"
                ranked = sorted(iteration_rows, key=lambda row: -float(row.get(ranking_field, row["selection_score"])))
                for rank, row in enumerate(ranked, start=1):
                    row["iteration_rank"] = rank

                write_csv(iteration_dir / "metrics.csv", ranked)
                write_json(iteration_dir / "metrics.json", ranked)
                all_generated_rows.extend([row for row in ranked if row.get("variant_role") == "vlm_variant"])

                winner = ranked[0]
                previous_prompt = current_entry["prompt"]
                previous_image_path = current_image_path
                if winner["variant_role"] == "baseline_current":
                    rejected_prompts.extend(item["prompt"] for item in prompt_items)
                    current_metrics = winner
                    log.info(
                        "[%s anchor %02d iter %02d] Baseline kept | %s=%.4f",
                        target_name,
                        anchor_number,
                        iteration,
                        ranking_field,
                        float(winner.get(ranking_field, 0.0)),
                    )
                else:
                    rejected_prompts.extend(
                        row["prompt"] for row in ranked
                        if row.get("variant_role") == "vlm_variant" and row["prompt"] != winner["prompt"]
                    )
                    current_entry = {
                        "id": str(winner["prompt_id"]),
                        "prompt": str(winner["prompt"]),
                        "negative_prompt": "",
                        "source": "ronda_13_vlm_refinement_winner",
                    }
                    current_image_path = Path(str(winner["render_path"]))
                    current_metrics = winner
                    log.info(
                        "[%s anchor %02d iter %02d] New winner variant %02d | %s=%.4f",
                        target_name,
                        anchor_number,
                        iteration,
                        int(winner["variant_index"]),
                        ranking_field,
                        float(winner.get(ranking_field, 0.0)),
                    )

                winner_payload = {
                    "ranking_field": ranking_field,
                    "previous_prompt": previous_prompt,
                    "previous_render_path": str(previous_image_path),
                    "winner_prompt": current_entry["prompt"],
                    "winner_render_path": str(current_image_path),
                    "winner_metrics": compact_metrics(current_metrics),
                    "baseline_kept": winner["variant_role"] == "baseline_current",
                }
                write_json(iteration_dir / "winner.json", winner_payload)

                analysis_payload = {
                    key: value
                    for key, value in parsed_response.items()
                    if key != "prompts"
                }

                trace["iterations"].append({
                    "iteration": iteration,
                    "request_path": str(iteration_dir / "vlm_request.json"),
                    "response_path": str(
                        iteration_dir / (args.manual_response_name if vlm_provider in {"stdin", "file"} else "parsed_response.json")
                    ),
                    "previous": {
                        "prompt": previous_prompt,
                        "render_path": str(previous_image_path),
                        "metrics": compact_metrics(baseline_row),
                    },
                    "analysis": analysis_payload,
                    "candidates": [
                        {
                            "variant_index": row.get("variant_index"),
                            "prompt": row.get("prompt"),
                            "reason": row.get("vlm_reason", ""),
                            "render_path": row.get("render_path", ""),
                            "rank": row.get("iteration_rank"),
                            "metrics": compact_metrics(row),
                        }
                        for row in ranked
                        if row.get("variant_role") == "vlm_variant"
                    ],
                    "winner": winner_payload,
                })
                write_json(trace_path, trace)
                release_torch_cache()

                if vlm_provider == "openrouter" and args.sleep_between_calls > 0:
                    log.info("Sleeping %.1fs before next OpenRouter call", args.sleep_between_calls)
                    time.sleep(args.sleep_between_calls)

            final_row = dict(current_metrics)
            final_row["anchor_number"] = anchor_number
            final_row["final_prompt"] = current_entry["prompt"]
            final_row["final_render_path"] = str(current_image_path)
            final_rows.append(final_row)
            trace["final"] = {
                "prompt": current_entry["prompt"],
                "render_path": str(current_image_path),
                "metrics": compact_metrics(current_metrics),
            }
            write_json(trace_path, trace)

    write_csv(run_dir / "all_generated_variant_metrics.csv", all_generated_rows)
    write_csv(run_dir / "final_anchor_winners.csv", final_rows)
    write_json(run_dir / "ronda_13_generated_prompts.json", generated_prompt_bank)
    write_json(run_dir / "vlm_trace_index.json", trace_index)
    write_json(run_dir / "summary.json", {
        "mode": "VLM iterative refinement over previous best anchors",
        "vlm_provider": vlm_provider,
        "model": args.model,
        "fallback_models": args.fallback_models,
        "top_anchors": args.top_anchors,
        "iterations": args.iterations,
        "variants_per_call": args.variants_per_call,
        "request_timeout": args.request_timeout,
        "max_retries": args.max_retries,
        "sleep_between_calls": args.sleep_between_calls,
        "targets": [path.name for path in targets],
        "trace_index_path": str(run_dir / "vlm_trace_index.json"),
        "final_winners": [
            {
                "target_name": row["target_name"],
                "anchor_number": row["anchor_number"],
                "prompt": row["final_prompt"],
                "render_path": row["final_render_path"],
                "metrics": compact_metrics(row),
            }
            for row in final_rows
        ],
    })
    log.info("Wrote generated prompt bank: %s", run_dir / "ronda_13_generated_prompts.json")
    log.info("Wrote final winners: %s", run_dir / "final_anchor_winners.csv")

    del pipe, clip_model, lpips_model
    release_torch_cache()
    return run_dir


if __name__ == "__main__":
    main()
