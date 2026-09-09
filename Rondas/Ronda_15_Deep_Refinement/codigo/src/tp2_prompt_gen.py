"""Shared prompt generation utilities for TP2 combinatorial search.

Consolidates deduplication, sampling, and combinatorial expansion logic
previously duplicated across generate_auto_round.py, generate_focused_round.py,
and generate_negative_round.py.
"""
from __future__ import annotations

import itertools
import random
from pathlib import Path
from typing import Any, Callable, Sequence


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _normalise_key(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    return " ".join(text.lower().replace(",", " ").split())


def unique_keep_order(
    items: Sequence[Any],
    key_fn: Callable[[Any], str] | None = None,
) -> list[Any]:
    """Remove duplicates while preserving insertion order.

    *key_fn* extracts the comparison string from each item.
    Defaults to treating items as plain strings.
    """
    if key_fn is None:
        key_fn = str  # type: ignore[assignment]
    seen: set[str] = set()
    result: list[Any] = []
    for item in items:
        key = _normalise_key(key_fn(item))
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------

def sample(
    items: list[Any],
    limit: int,
    seed: int,
    key_fn: Callable[[Any], str] | None = None,
    head_size: int = 20,
) -> list[Any]:
    """Deduplicate, keep the first *head_size* items, then randomly sample the rest.

    *key_fn* is forwarded to :func:`unique_keep_order`.
    """
    items = unique_keep_order(items, key_fn=key_fn)
    if len(items) <= limit:
        return items
    rng = random.Random(seed)
    head = items[: min(head_size, limit)]
    tail = items[min(head_size, len(items)):]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


# ---------------------------------------------------------------------------
# Combinatorial expansion (string prompts)
# ---------------------------------------------------------------------------

def combine(
    subjects: list[str],
    compositions: list[str],
    styles: list[str],
    details: list[str],
    limit: int,
    seed: int,
    priority: list[str] | None = None,
) -> list[str]:
    """Build prompts from the Cartesian product of parts, with optional priority head.

    Each prompt is ``subject, composition, detail, style`` joined by ``, ``.
    *priority* prompts are prepended verbatim before combinatorial expansion.
    """
    prompts: list[str] = list(priority) if priority else []
    for subject, composition, style, detail in itertools.product(
        subjects, compositions, styles, details,
    ):
        parts = [subject, composition, detail, style]
        prompts.append(", ".join(p for p in parts if p))
    return sample(prompts, limit=limit, seed=seed)


# ---------------------------------------------------------------------------
# Dict-based helpers (for rounds with negative_prompt metadata)
# ---------------------------------------------------------------------------

def make_entry(
    target: str,
    prompt: str,
    index: int,
    negative_prompt: str = "",
    source: str = "auto",
) -> dict[str, str]:
    """Create a normalised prompt entry dict."""
    return {
        "id": f"{Path(target).stem}_{source}_{index:03d}",
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "source": source,
    }


def combine_with_negatives(
    target: str,
    priority: list[str],
    subjects: list[str],
    compositions: list[str],
    details: list[str],
    styles: list[str],
    negative_prompt: str,
    limit: int,
    seed: int,
    source: str = "auto",
) -> list[dict[str, str]]:
    """Like :func:`combine` but wraps each prompt in a dict with ``negative_prompt``."""
    entries = [
        make_entry(target, p, i + 1, negative_prompt, f"{source}_priority")
        for i, p in enumerate(priority)
    ]
    offset = len(entries) + 1
    for i, parts in enumerate(
        itertools.product(subjects, compositions, details, styles),
        start=offset,
    ):
        entries.append(make_entry(target, ", ".join(parts), i, negative_prompt, source))
    return sample(entries, limit, seed, key_fn=lambda e: e["prompt"])
