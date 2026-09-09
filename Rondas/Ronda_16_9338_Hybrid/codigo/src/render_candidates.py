from __future__ import annotations

import argparse
from pathlib import Path

from tp2_common import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TARGET_DIR,
    LCMConfig,
    create_run_dir,
    list_target_images,
    load_lcm_pipeline,
    normalise_prompt_entries,
    read_json,
    render_prompt,
    safe_stem,
    seed_from_filename,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render TP2 prompt candidates with the fixed LCM setup.")
    parser.add_argument("--prompts", type=Path, default=Path("prompts/candidates.json"))
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--identity", default="candidate_render")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--only", nargs="*", help="Optional target filenames to render, e.g. 1159_25.png")
    parser.add_argument("--limit-per-target", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--disable-progress-bar", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = LCMConfig()

    targets = list_target_images(args.targets)
    if args.only:
        wanted = set(args.only)
        targets = [path for path in targets if path.name in wanted]
    if not targets:
        raise FileNotFoundError(f"No target images found in {args.targets}")

    prompt_bank = normalise_prompt_entries(read_json(args.prompts))
    target_by_name = {path.name: path for path in targets}

    print("Targets:", ", ".join(target_by_name))

    pipe, device = load_lcm_pipeline(config, args.device)
    if hasattr(pipe, "set_progress_bar_config"):
        pipe.set_progress_bar_config(disable=args.disable_progress_bar)
    print("Device:", device)

    run_dir = create_run_dir(args.output_dir, args.identity)
    print("Run directory:", run_dir)

    rows: list[dict[str, object]] = []
    for target_name, target_path in target_by_name.items():
        entries = prompt_bank.get(target_name, [])
        if args.limit_per_target > 0:
            entries = entries[: args.limit_per_target]
        if not entries:
            print("Skipping target without prompts:", target_name)
            continue

        seed = seed_from_filename(target_path, config.seed)
        target_output_dir = run_dir / safe_stem(target_path)
        target_output_dir.mkdir(parents=True, exist_ok=True)

        for index, entry in enumerate(entries, start=1):
            image_path = target_output_dir / f"candidate_{index:03d}.png"
            if image_path.exists() and not args.overwrite:
                print("Keeping existing render:", image_path)
            else:
                print(f"Rendering {target_name} #{index:03d}: {entry['prompt']}")
                image = render_prompt(
                    entry["prompt"],
                    seed=seed,
                    pipe=pipe,
                    config=config,
                    device=device,
                    negative_prompt=entry.get("negative_prompt", ""),
                )
                image.save(image_path)

            rows.append(
                {
                    "target_name": target_name,
                    "target_path": str(target_path),
                    "render_seed": seed,
                    "candidate_index": index,
                    "prompt_id": entry["id"],
                    "prompt_source": entry["source"],
                    "prompt": entry["prompt"],
                    "negative_prompt": entry.get("negative_prompt", ""),
                    "render_path": str(image_path),
                    "model_id": config.model_id,
                    "num_inference_steps": config.num_inference_steps,
                    "guidance_scale": config.guidance_scale,
                    "original_inference_steps": config.lcm_origin_steps,
                    "width": config.width,
                    "height": config.height,
                }
            )

    write_csv(run_dir / "manifest.csv", rows)
    write_json(run_dir / "manifest.json", rows)
    print("Wrote:", run_dir / "manifest.csv")
    print("Rendered candidates:", len(rows))


if __name__ == "__main__":
    main()
