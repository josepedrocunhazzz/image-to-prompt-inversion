from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


METRIC_FIELDS = [
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in METRIC_FIELDS:
        if field not in metrics:
            continue
        value = metrics[field]
        try:
            result[field] = round(float(value), 6)
        except (TypeError, ValueError):
            result[field] = value
    return result


def detail_to_text(value: Any, level: int = 0) -> str:
    prefix = "  " * level
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        lines = []
        for item in value:
            text = detail_to_text(item, level + 1).strip()
            if text:
                lines.append(f"{prefix}- {text}")
        return "\n".join(lines)
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            title = str(key).replace("_", " ").title()
            rendered = detail_to_text(item, level + 1).strip()
            if rendered:
                lines.append(f"{prefix}{title}:\n{rendered}")
        return "\n\n".join(lines)
    return str(value)


def append_analysis_markdown(lines: list[str], analysis: dict[str, Any]) -> None:
    sections = [
        ("Target Description", analysis.get("target_description_detailed")),
        ("Current Image Description", analysis.get("current_image_description_detailed")),
        ("Detailed Differences", analysis.get("detailed_visual_differences")),
        ("Prompt Revision Plan", analysis.get("prompt_revision_plan")),
    ]
    for title, value in sections:
        text = detail_to_text(value).strip()
        if not text:
            continue
        lines.extend([f"{title}:", "", text, ""])


def safe_link_or_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        destination.unlink()
    try:
        destination.symlink_to(source)
    except OSError:
        shutil.copy2(source, destination)


def resolve_run_path(run_dir: Path, raw_path: str | Path) -> Path:
    path = Path(raw_path)
    if path.exists():
        return path
    parts = path.parts
    if run_dir.name in parts:
        index = parts.index(run_dir.name)
        candidate = run_dir.joinpath(*parts[index + 1 :])
        if candidate.exists():
            return candidate
    return path


def make_run_readme(run_dir: Path, final_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# VLM Refinement Run",
        "",
        f"Raw run folder: `{run_dir}`",
        "",
        "## Where To Look",
        "",
        "- `review/` has the clean, human-readable view.",
        "- `summary.json` and CSV files are the raw machine outputs.",
        "- Each target has `trace.md`, `initial_prompt.txt`, `final_prompt.txt`, and per-iteration folders.",
        "",
        "## Final Winners",
        "",
    ]
    for row in final_rows:
        metrics = compact_metrics(row.get("metrics", row))
        lines.extend([
            f"### {row.get('target_name', 'unknown')}",
            "",
            f"Prompt: {row.get('prompt') or row.get('final_prompt', '')}",
            "",
            f"Render: `{row.get('render_path') or row.get('final_render_path', '')}`",
            "",
            f"Metrics: `{json.dumps(metrics, ensure_ascii=False)}`",
            "",
        ])
    return "\n".join(lines)


def make_target_trace_markdown(trace: dict[str, Any]) -> str:
    lines = [
        f"# {trace['target_name']} Anchor {trace['anchor_number']:02d}",
        "",
        "## Initial",
        "",
        f"Prompt: {trace['initial']['prompt']}",
        "",
        f"Image: `{trace['initial']['render_path']}`",
        "",
        f"Metrics: `{json.dumps(compact_metrics(trace['initial'].get('metrics', {})), ensure_ascii=False)}`",
        "",
        "## Iterations",
        "",
    ]
    for item in trace.get("iterations", []):
        winner = item.get("winner", {})
        candidates = item.get("candidates", [])
        candidate = candidates[0] if candidates else {}
        analysis = item.get("analysis", {})
        lines.extend([
            f"### Iteration {int(item['iteration']):02d}",
            "",
            f"Strategy: {analysis.get('strategy', '')}",
            "",
        ])
        append_analysis_markdown(lines, analysis)
        lines.extend([
            f"Prompt tested: {candidate.get('prompt', '')}",
            "",
            f"Reason: {candidate.get('reason', '')}",
            "",
            f"Decision: {'baseline kept' if winner.get('baseline_kept') else 'new prompt won'}",
            "",
            f"Generated image: `{candidate.get('render_path', '')}`",
            "",
            f"Winner image: `{winner.get('winner_render_path', '')}`",
            "",
            f"Winner metrics: `{json.dumps(compact_metrics(winner.get('winner_metrics', {})), ensure_ascii=False)}`",
            "",
        ])
    return "\n".join(lines)


def make_target_review(run_dir: Path, trace_path: Path, review_dir: Path) -> dict[str, Any]:
    trace = read_json(trace_path)
    target_name = trace["target_name"]
    target_review = review_dir / target_name.replace(".png", "")
    target_review.mkdir(parents=True, exist_ok=True)

    target_image = run_dir / target_name.replace(".png", "") / "target.png"
    safe_link_or_copy(target_image, target_review / "target.png")
    safe_link_or_copy(resolve_run_path(run_dir, trace["initial"]["render_path"]), target_review / "initial.png")
    write_text(target_review / "initial_prompt.txt", trace["initial"]["prompt"] + "\n")
    write_json(target_review / "initial_metrics.json", compact_metrics(trace["initial"].get("metrics", {})))

    final = trace.get("final", trace["initial"])
    safe_link_or_copy(resolve_run_path(run_dir, final["render_path"]), target_review / "best.png")
    write_text(target_review / "final_prompt.txt", final["prompt"] + "\n")
    write_json(target_review / "final_metrics.json", compact_metrics(final.get("metrics", {})))
    write_text(target_review / "trace.md", make_target_trace_markdown(trace))

    for item in trace.get("iterations", []):
        iteration = int(item["iteration"])
        iteration_dir = target_review / "iterations" / f"{iteration:02d}"
        iteration_dir.mkdir(parents=True, exist_ok=True)
        candidates = item.get("candidates", [])
        candidate = candidates[0] if candidates else {}
        if candidate.get("render_path"):
            safe_link_or_copy(resolve_run_path(run_dir, candidate["render_path"]), iteration_dir / "generated.png")
        previous = item.get("previous", {})
        if previous.get("render_path"):
            safe_link_or_copy(resolve_run_path(run_dir, previous["render_path"]), iteration_dir / "previous.png")
        winner = item.get("winner", {})
        if winner.get("winner_render_path"):
            safe_link_or_copy(resolve_run_path(run_dir, winner["winner_render_path"]), iteration_dir / "winner.png")
        write_text(iteration_dir / "prompt.txt", candidate.get("prompt", "") + "\n")
        write_text(iteration_dir / "reason.txt", candidate.get("reason", "") + "\n")
        write_json(iteration_dir / "analysis.json", item.get("analysis", {}))
        target_description = detail_to_text(item.get("analysis", {}).get("target_description_detailed")).strip()
        if target_description:
            write_text(iteration_dir / "target_description.txt", target_description + "\n")
            if iteration == 1:
                write_text(target_review / "target_description_detailed.txt", target_description + "\n")
        current_description = detail_to_text(item.get("analysis", {}).get("current_image_description_detailed")).strip()
        if current_description:
            write_text(iteration_dir / "current_image_description.txt", current_description + "\n")
        detailed_differences = detail_to_text(item.get("analysis", {}).get("detailed_visual_differences")).strip()
        if detailed_differences:
            write_text(iteration_dir / "detailed_differences.txt", detailed_differences + "\n")
        revision_plan = detail_to_text(item.get("analysis", {}).get("prompt_revision_plan")).strip()
        if revision_plan:
            write_text(iteration_dir / "prompt_revision_plan.txt", revision_plan + "\n")
        write_json(iteration_dir / "metrics.json", {
            "candidate": compact_metrics(candidate.get("metrics", {})),
            "winner": compact_metrics(winner.get("winner_metrics", {})),
            "baseline_kept": bool(winner.get("baseline_kept")),
        })
        decision = "baseline_kept" if winner.get("baseline_kept") else "new_prompt_won"
        write_text(iteration_dir / "decision.txt", decision + "\n")

    return {
        "target_name": target_name,
        "review_path": str(target_review),
        "trace_path": str(trace_path),
        "final_prompt": final["prompt"],
        "final_render_path": final["render_path"],
        "final_metrics": compact_metrics(final.get("metrics", {})),
    }


def update_current_pointer(run_dir: Path) -> None:
    output_root = run_dir.parent.parent if run_dir.parent.name == "runs" else run_dir.parent
    write_text(output_root / "CURRENT_RUN.txt", str(run_dir) + "\n")
    current = output_root / "current"
    if current.exists() or current.is_symlink():
        if current.is_dir() and not current.is_symlink():
            return
        current.unlink()
    try:
        current.symlink_to(run_dir)
    except OSError:
        pass


def make_friendly_view(run_dir: Path | str) -> Path:
    run_dir = Path(run_dir).resolve()
    summary_path = run_dir / "summary.json"
    trace_index_path = run_dir / "vlm_trace_index.json"
    if not summary_path.exists() or not trace_index_path.exists():
        raise FileNotFoundError(f"Missing summary or trace index in {run_dir}")

    summary = read_json(summary_path)
    trace_index = read_json(trace_index_path)
    review_dir = run_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)

    targets = []
    for entry in trace_index:
        trace_path = resolve_run_path(run_dir, entry["trace_path"])
        if not trace_path.exists():
            target_stem = Path(entry["target_name"]).stem
            anchor_number = int(entry.get("anchor_number", 1))
            trace_path = run_dir / target_stem / f"anchor_{anchor_number:02d}" / "vlm_trace.json"
        targets.append(make_target_review(run_dir, trace_path, review_dir))

    write_json(review_dir / "index.json", {
        "run_dir": str(run_dir),
        "mode": summary.get("vlm_provider"),
        "targets": targets,
    })
    write_text(run_dir / "RUN_README.md", make_run_readme(run_dir, summary.get("final_winners", [])))
    update_current_pointer(run_dir)
    return review_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a clean review folder for a VLM refinement run.")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    path = make_friendly_view(args.run_dir)
    print(path)
