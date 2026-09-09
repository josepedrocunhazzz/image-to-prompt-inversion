from __future__ import annotations

import argparse
import itertools
import json
import os
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import torch
import torch.nn.functional as F

from tp2_common import DEFAULT_TARGET_DIR, load_image
from tp2_prompt_gen import make_entry, sample, unique_keep_order


CLIP_MODEL_ID = "openai/clip-vit-large-patch14"
SOURCE = "ronda_02_pez_evolution"


@dataclass(frozen=True)
class PezConfig:
    target: str
    prefix: str
    suffix: str
    seed_words: list[str]
    base_templates: list[str]
    slot_count: int
    restarts: int
    steps: int
    lr: float
    top_tokens_per_slot: int
    phrase_limit: int
    seed: int
    banned_terms: set[str]
    allowed_terms: list[str]


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def entries_for(
    target: str,
    prompts: list[str],
    limit: int,
    seed: int,
    source: str,
    head_size: int = 80,
) -> list[dict[str, str]]:
    prompts = sample(unique_keep_order(prompts), limit=limit, seed=seed, head_size=head_size)
    return [make_entry(target, prompt, index + 1, "", source) for index, prompt in enumerate(prompts)]


def build_cube_evolution_prompts(limit: int = 120) -> list[dict[str, str]]:
    target = "1159_7.png"
    priority = [
        "pale wooden cube hedgehog block, strict cube silhouette, tiny dark eyes and small snout on the upper front face, short amber quills only on the top surface, warm brown studio macro photo",
        "single cube shaped hedgehog object, square tiled wooden sides, tiny face embedded in the top front edge, dense orange spines forming a flat top cap, soft brown product photograph",
        "wooden block cube animal sculpture, flat 4 by 4 tiled front, small hedgehog eyes and nose peeking from upper front, spiky tan fur on top plane, warm close up render",
        "cubical hedgehog toy made from pale wood tiles, front face visible and square, small snout tucked under the spiky top, orange quill crown on top, shallow depth of field",
        "beige wooden cube with hedgehog face carved into the upper front, square tile seams on every side, soft orange spikes covering only the top, warm studio object photo",
        "small hedgehog cube sculpture, block body like a wooden dice, tiny organic face on front top row, dense tan quills rising from top surface, brown background",
    ]
    bodies = [
        "pale wooden cube hedgehog block",
        "single cube shaped hedgehog object",
        "wooden block cube animal sculpture",
        "cubical hedgehog toy made from pale wood tiles",
        "small hedgehog cube sculpture",
        "beige tiled cube with a hedgehog face",
        "wooden checker cube creature figurine",
        "strict cube silhouette hedgehog object",
    ]
    cube_constraints = [
        "flat square front face visible",
        "4 by 4 tiled wooden sides",
        "straight cube edges and square tile seams",
        "block body like a wooden dice",
        "pale checker block sides",
        "front wall made of small wooden squares",
        "clean cubic body with flat blocky silhouette",
    ]
    faces = [
        "tiny dark eyes and small snout on the upper front face",
        "small face embedded in the top front edge",
        "hedgehog eyes and nose peeking from upper front",
        "tiny organic face tucked below the spiky top",
        "small round snout centered on the front top row",
        "furry face peeking through the upper front tiles",
        "dark bead eyes barely visible under the top quills",
    ]
    tops = [
        "short amber quills only on the top surface",
        "dense orange spines forming a flat top cap",
        "spiky tan fur on top plane",
        "orange quill crown on top",
        "soft brown spikes rising from the top face",
        "compact hedgehog bristles covering the top square",
        "tan spines arranged like a fur lid",
    ]
    styles = [
        "warm brown studio macro photo",
        "soft brown product photograph",
        "realistic warm close up render",
        "shallow depth of field, square crop",
        "gentle shadows on a brown studio surface",
        "macro object render with warm beige material",
    ]
    prompts = list(priority)
    for body, cube, face, top, style in itertools.product(bodies, cube_constraints, faces, tops, styles):
        prompts.append(join_parts(body, cube, face, top, style))
    return entries_for(target, prompts, limit=limit, seed=2507, source=f"{SOURCE}_cube_evolution", head_size=90)


def build_spiny_creature_evolution_prompts(limit: int = 120) -> list[dict[str, str]]:
    target = "9338.png"
    priority = [
        "small round fuzzy porcupine mascot, orange face and snout, glossy black eye, turquoise oval belly patch, short rainbow bristles around the back, centered storybook painting",
        "tiny upright spiny plush creature, warm orange rounded face, teal oval chest gem, little paws, rainbow porcupine quills behind the shoulders, vertical colored light streaks",
        "round baby echidna toy creature, orange muzzle and cheek, blue green belly oval, stubby arms, multicolor soft spines, painterly dark warm background",
        "compact fuzzy orange faced creature, small black eyes, cyan belly patch, rainbow bristle mane around shoulders, little claws, soft fantasy illustration",
        "tiny round porcupine character, orange head and snout, teal belly shield, shaggy rainbow quills on the back, upright centered pose, textured brush strokes",
        "small cute spiny animal figurine, orange face, turquoise chest patch, short colorful quills, round fuzzy body, warm rainbow backdrop",
    ]
    subjects = [
        "small round fuzzy porcupine mascot",
        "tiny upright spiny plush creature",
        "round baby echidna toy creature",
        "compact fuzzy orange faced creature",
        "tiny round porcupine character",
        "small cute spiny animal figurine",
        "upright fuzzy bristle creature",
        "round orange faced hedgehog mascot",
    ]
    faces = [
        "orange face and snout",
        "warm orange rounded face",
        "orange muzzle and cheek",
        "small black eyes and orange snout",
        "glossy dark eye on a peach orange face",
        "soft orange head with tiny nose",
    ]
    bodies = [
        "turquoise oval belly patch",
        "teal oval chest gem",
        "blue green belly oval",
        "cyan belly patch and little paws",
        "teal chest shield on a fuzzy body",
        "round body with blue green belly",
    ]
    spines = [
        "short rainbow bristles around the back",
        "rainbow porcupine quills behind the shoulders",
        "multicolor soft spines",
        "rainbow bristle mane around shoulders",
        "shaggy rainbow quills on the back",
        "short colorful quills framing the body",
    ]
    styles = [
        "centered storybook painting",
        "vertical colored light streaks",
        "painterly dark warm background",
        "soft fantasy illustration",
        "textured brush strokes",
        "warm rainbow backdrop, square crop",
    ]
    prompts = list(priority)
    for subject, face, body, spine, style in itertools.product(subjects, faces, bodies, spines, styles):
        prompts.append(join_parts(subject, face, body, spine, style))
    return entries_for(target, prompts, limit=limit, seed=2538, source=f"{SOURCE}_creature_evolution", head_size=90)


def build_evolutionary_round(evolution_limit: int = 120) -> dict[str, list[dict[str, str]]]:
    return {
        "1159_7.png": build_cube_evolution_prompts(limit=evolution_limit),
        "9338.png": build_spiny_creature_evolution_prompts(limit=evolution_limit),
    }


def clean_decoded_token(text: str) -> str | None:
    text = text.strip().lower()
    text = text.replace("</w>", "")
    text = re.sub(r"[^a-z-]", "", text)
    if not (3 <= len(text) <= 16):
        return None
    if text.startswith("-") or text.endswith("-"):
        return None
    return text


def clean_phrase(words: Iterable[str], banned_terms: set[str]) -> str | None:
    cleaned: list[str] = []
    seen: set[str] = set()
    for word in words:
        token = clean_decoded_token(word)
        if not token or token in banned_terms:
            continue
        if token in seen:
            continue
        seen.add(token)
        cleaned.append(token)
    if len(cleaned) < 2:
        return None
    phrase = " ".join(cleaned)
    if any(term in phrase.split() for term in banned_terms):
        return None
    return phrase


def build_pez_configs(
    restarts: int = 4,
    steps: int = 70,
    phrase_limit: int = 36,
) -> dict[str, PezConfig]:
    return {
        "1159_7.png": PezConfig(
            target="1159_7.png",
            prefix="wooden cube hedgehog object with",
            suffix="warm brown studio macro photo",
            seed_words=["wooden", "cube", "tiled", "front", "face", "spikes", "quills", "top"],
            base_templates=[
                "pale wooden cube hedgehog block, {phrase}, tiny face on upper front, orange quills on top, warm brown studio macro photo",
                "strict cube shaped hedgehog object, {phrase}, square tiled sides, small eyes and snout, spiky top cap",
                "wooden block cube animal sculpture, {phrase}, front square face visible, tan quills on the top plane, realistic object render",
            ],
            slot_count=6,
            restarts=restarts,
            steps=steps,
            lr=0.08,
            top_tokens_per_slot=7,
            phrase_limit=phrase_limit,
            seed=2517,
            banned_terms={"dragon", "dog", "cat", "fox", "human", "person", "warrior", "armor", "girl", "boy"},
            allowed_terms=[
                "wooden", "wood", "cube", "cubical", "block", "square", "tiled", "tile", "checker",
                "front", "face", "eyes", "snout", "nose", "tiny", "small", "embedded", "peeking",
                "hedgehog", "spines", "spiky", "quills", "bristles", "top", "surface", "cap",
                "amber", "orange", "tan", "beige", "pale", "warm", "brown", "macro", "studio",
                "object", "sculpture", "figurine", "toy", "seams", "straight", "strict",
            ],
        ),
        "9338.png": PezConfig(
            target="9338.png",
            prefix="small round orange faced fuzzy creature with",
            suffix="teal belly rainbow bristles storybook painting",
            seed_words=["orange", "face", "teal", "belly", "rainbow", "spines", "fuzzy", "small"],
            base_templates=[
                "small round fuzzy porcupine mascot, {phrase}, orange face, turquoise oval belly, rainbow bristles, centered storybook painting",
                "tiny upright spiny plush creature, {phrase}, warm orange snout, teal belly patch, short colorful quills, vertical colored light streaks",
                "round orange faced hedgehog mascot, {phrase}, blue green belly oval, rainbow bristle mane, soft fantasy illustration",
            ],
            slot_count=6,
            restarts=restarts,
            steps=steps,
            lr=0.08,
            top_tokens_per_slot=7,
            phrase_limit=phrase_limit,
            seed=2539,
            banned_terms={
                "dragon", "reptile", "lizard", "serpent", "snake", "horned", "humanoid",
                "muscular", "warrior", "armor", "woman", "man", "blueberry",
            },
            allowed_terms=[
                "small", "tiny", "round", "upright", "fuzzy", "soft", "cute", "orange", "face",
                "snout", "muzzle", "cheek", "black", "eye", "eyes", "teal", "turquoise",
                "cyan", "blue", "green", "belly", "chest", "oval", "patch", "gem", "paws",
                "claws", "porcupine", "hedgehog", "echidna", "spiny", "spines", "quills",
                "bristles", "rainbow", "colorful", "multicolor", "back", "shoulders",
                "storybook", "painting", "painterly", "warm", "vertical", "light", "streaks",
                "creature", "mascot", "animal", "figurine", "plush",
            ],
        ),
    }


def _encode_no_special(tokenizer, text: str) -> list[int]:
    return tokenizer(text, add_special_tokens=False)["input_ids"]


def _initial_slot_ids(tokenizer, seed_words: list[str], slot_count: int, rng: random.Random) -> list[int]:
    ids: list[int] = []
    words = list(seed_words)
    rng.shuffle(words)
    for word in words:
        for token_id in _encode_no_special(tokenizer, word):
            ids.append(int(token_id))
            if len(ids) >= slot_count:
                return ids
    while len(ids) < slot_count:
        ids.append(int(tokenizer.eos_token_id))
    return ids[:slot_count]


def _prepare_allowed_tokens(tokenizer, model, device: str, allowed_terms: list[str] | None = None) -> tuple[torch.Tensor, list[int], list[str]]:
    special = {
        token_id for token_id in [
            tokenizer.bos_token_id,
            tokenizer.eos_token_id,
            tokenizer.pad_token_id,
            tokenizer.unk_token_id,
        ] if token_id is not None
    }
    raw_token_ids: list[int]
    if allowed_terms:
        raw_token_ids = []
        for term in allowed_terms:
            raw_token_ids.extend(_encode_no_special(tokenizer, term))
        allowed_clean_terms = {
            cleaned for cleaned in (clean_decoded_token(term) for term in allowed_terms) if cleaned
        }
    else:
        raw_token_ids = list(range(int(model.text_model.embeddings.token_embedding.num_embeddings)))
        allowed_clean_terms = set()

    token_ids = []
    token_words = []
    seen: set[str] = set()
    for token_id in raw_token_ids:
        token_id = int(token_id)
        if token_id in special:
            continue
        decoded = tokenizer.decode([token_id]).strip()
        cleaned = clean_decoded_token(decoded)
        if cleaned is None or cleaned in seen:
            continue
        if allowed_clean_terms and cleaned not in allowed_clean_terms:
            continue
        seen.add(cleaned)
        token_ids.append(token_id)
        token_words.append(cleaned)
    if not token_ids:
        raise ValueError("No allowed PEZ tokens after filtering.")
    embeddings = model.text_model.embeddings.token_embedding.weight.detach()[token_ids].to(device)
    embeddings = F.normalize(embeddings, dim=-1)
    return embeddings, token_ids, token_words


def _clip_text_features_from_slot_embeddings(model, input_ids: torch.Tensor, slot_positions: list[int], slot_embeddings: torch.Tensor) -> torch.Tensor:
    from transformers.models.clip.modeling_clip import _create_4d_causal_attention_mask

    text_model = model.text_model
    hidden_states = text_model.embeddings(input_ids=input_ids)
    hidden_states = hidden_states.clone()
    hidden_states[:, slot_positions, :] = slot_embeddings.unsqueeze(0)

    input_shape = input_ids.size()
    causal_attention_mask = _create_4d_causal_attention_mask(
        input_shape, hidden_states.dtype, device=hidden_states.device,
    )
    encoder_outputs = text_model.encoder(
        inputs_embeds=hidden_states,
        attention_mask=None,
        causal_attention_mask=causal_attention_mask,
        output_attentions=False,
        output_hidden_states=False,
    )
    last_hidden_state = text_model.final_layer_norm(encoder_outputs.last_hidden_state)
    eos_position = (input_ids.to(dtype=torch.int, device=input_ids.device) == text_model.eos_token_id).int().argmax(dim=-1)
    pooled = last_hidden_state[torch.arange(last_hidden_state.shape[0], device=input_ids.device), eos_position]
    projection = model.text_projection
    text_features = projection(pooled) if callable(projection) else pooled @ projection
    return text_features / text_features.norm(dim=-1, keepdim=True)


def _rank_text_prompts(prompts: list[str], image, processor, model, device: str, batch_size: int = 64) -> list[tuple[str, float]]:
    prompts = unique_keep_order([prompt.strip() for prompt in prompts if prompt.strip()])
    image_inputs = processor(images=image, return_tensors="pt")
    image_inputs = {key: value.to(device) for key, value in image_inputs.items()}
    with torch.no_grad():
        image_embedding = model.get_image_features(**image_inputs)
        image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)

    scored: list[tuple[str, float]] = []
    for start in range(0, len(prompts), batch_size):
        batch = prompts[start:start + batch_size]
        text_inputs = processor(text=batch, return_tensors="pt", padding=True, truncation=True, max_length=77)
        text_inputs = {key: value.to(device) for key, value in text_inputs.items()}
        with torch.no_grad():
            text_embedding = model.get_text_features(**text_inputs)
            text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
            scores = (text_embedding @ image_embedding.T).squeeze(1)
        scored.extend((prompt, float(score)) for prompt, score in zip(batch, scores.detach().cpu()))
    return sorted(scored, key=lambda item: item[1], reverse=True)


def pez_phrases_for_target(
    config: PezConfig,
    target_dir: Path,
    tokenizer,
    processor,
    model,
    device: str,
) -> list[str]:
    rng = random.Random(config.seed)
    allowed_embeddings, _allowed_ids, allowed_words = _prepare_allowed_tokens(
        tokenizer, model, device, allowed_terms=config.allowed_terms,
    )

    target_image = load_image(target_dir / config.target)
    image_inputs = processor(images=target_image, return_tensors="pt")
    image_inputs = {key: value.to(device) for key, value in image_inputs.items()}
    with torch.no_grad():
        image_embedding = model.get_image_features(**image_inputs)
        image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)

    prefix_ids = _encode_no_special(tokenizer, config.prefix)
    suffix_ids = _encode_no_special(tokenizer, config.suffix)
    max_payload = 75 - config.slot_count
    if len(prefix_ids) + len(suffix_ids) > max_payload:
        suffix_ids = suffix_ids[: max(0, max_payload - len(prefix_ids))]

    phrases: list[str] = []
    for restart in range(config.restarts):
        seed_ids = _initial_slot_ids(tokenizer, config.seed_words, config.slot_count, rng)
        input_ids_list = [tokenizer.bos_token_id] + prefix_ids + seed_ids + suffix_ids + [tokenizer.eos_token_id]
        input_ids = torch.tensor([input_ids_list], dtype=torch.long, device=device)
        slot_start = 1 + len(prefix_ids)
        slot_positions = list(range(slot_start, slot_start + config.slot_count))

        token_embedding = model.text_model.embeddings.token_embedding
        slot_embeddings = torch.nn.Parameter(token_embedding(torch.tensor(seed_ids, device=device)).detach().clone())
        optimizer = torch.optim.Adam([slot_embeddings], lr=config.lr)
        for _ in range(config.steps):
            optimizer.zero_grad(set_to_none=True)
            text_embedding = _clip_text_features_from_slot_embeddings(model, input_ids, slot_positions, slot_embeddings)
            loss = -(text_embedding * image_embedding).sum()
            loss.backward()
            optimizer.step()

        with torch.no_grad():
            slot_norm = F.normalize(slot_embeddings.detach(), dim=-1)
            similarities = slot_norm @ allowed_embeddings.T
            top_indices = similarities.topk(k=config.top_tokens_per_slot, dim=-1).indices.detach().cpu().tolist()

        top_words = [[allowed_words[index] for index in row] for row in top_indices]
        greedy = clean_phrase([row[0] for row in top_words], config.banned_terms)
        if greedy:
            phrases.append(greedy)
        for offset in range(1, config.top_tokens_per_slot):
            variant = clean_phrase([row[(offset + pos) % len(row)] for pos, row in enumerate(top_words)], config.banned_terms)
            if variant:
                phrases.append(variant)
        for _ in range(18):
            variant = clean_phrase([rng.choice(row[: min(4, len(row))]) for row in top_words], config.banned_terms)
            if variant:
                phrases.append(variant)

        print(config.target, "PEZ restart", restart + 1, "best phrase:", greedy or "(filtered)")

    return unique_keep_order(phrases)[: config.phrase_limit]


def pez_prompts_for_target(
    config: PezConfig,
    target_dir: Path,
    tokenizer,
    processor,
    model,
    device: str,
    prompt_limit: int,
) -> list[dict[str, str]]:
    phrases = pez_phrases_for_target(config, target_dir, tokenizer, processor, model, device)
    prompts: list[str] = []
    for phrase in phrases:
        for template in config.base_templates:
            prompts.append(template.format(phrase=phrase))

    target_image = load_image(target_dir / config.target)
    ranked = _rank_text_prompts(prompts, target_image, processor, model, device)
    entries: list[dict[str, str]] = []
    for index, (prompt, score) in enumerate(ranked[:prompt_limit], start=1):
        entry = make_entry(config.target, prompt, index, "", f"{SOURCE}_pez")
        entry["clip_text_image_score"] = score
        entries.append(entry)
    return entries


def generate_pez_entries(
    target_dir: Path,
    offline: bool,
    device: str,
    pez_prompt_limit: int,
    restarts: int,
    steps: int,
    phrase_limit: int,
) -> dict[str, list[dict[str, str]]]:
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    from transformers import CLIPModel, CLIPProcessor, CLIPTokenizer

    resolved_device = "cuda" if device == "auto" and torch.cuda.is_available() else ("cpu" if device == "auto" else device)
    tokenizer = CLIPTokenizer.from_pretrained(CLIP_MODEL_ID, local_files_only=offline)
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID, local_files_only=offline)
    model = CLIPModel.from_pretrained(CLIP_MODEL_ID, local_files_only=offline).to(resolved_device).eval()

    result: dict[str, list[dict[str, str]]] = {}
    for target, config in build_pez_configs(restarts=restarts, steps=steps, phrase_limit=phrase_limit).items():
        result[target] = pez_prompts_for_target(
            config,
            target_dir=target_dir,
            tokenizer=tokenizer,
            processor=processor,
            model=model,
            device=resolved_device,
            prompt_limit=pez_prompt_limit,
        )
    return result


def merge_rounds(
    evolution: dict[str, list[dict[str, str]]],
    pez: dict[str, list[dict[str, str]]],
    final_limit_per_target: int,
) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for target in sorted(set(evolution) | set(pez)):
        entries = list(evolution.get(target, [])) + list(pez.get(target, []))
        entries = unique_keep_order(entries, key_fn=lambda entry: entry["prompt"])
        entries = entries[:final_limit_per_target]
        for index, entry in enumerate(entries, start=1):
            entry["id"] = f"{Path(target).stem}_{SOURCE}_{index:03d}"
            entry["negative_prompt"] = ""
        result[target] = entries
    return result


def build_round_without_pez(evolution_limit: int = 120, final_limit_per_target: int = 160) -> dict[str, list[dict[str, str]]]:
    return merge_rounds(build_evolutionary_round(evolution_limit=evolution_limit), {}, final_limit_per_target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 ronda 2 PEZ + evolutionary prompt candidates.")
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET_DIR)
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_ronda_02_pez_evolution.json"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu", "mps"])
    parser.add_argument("--skip-pez", action="store_true", help="Generate only the deterministic evolutionary bank.")
    parser.add_argument("--evolution-limit", type=int, default=110)
    parser.add_argument("--pez-prompt-limit", type=int, default=60)
    parser.add_argument("--final-limit-per-target", type=int, default=160)
    parser.add_argument("--pez-restarts", type=int, default=4)
    parser.add_argument("--pez-steps", type=int, default=60)
    parser.add_argument("--pez-phrase-limit", type=int, default=30)
    args = parser.parse_args()

    evolution = build_evolutionary_round(evolution_limit=args.evolution_limit)
    pez: dict[str, list[dict[str, str]]] = {}
    if not args.skip_pez:
        pez = generate_pez_entries(
            target_dir=args.target_dir,
            offline=args.offline,
            device=args.device,
            pez_prompt_limit=args.pez_prompt_limit,
            restarts=args.pez_restarts,
            steps=args.pez_steps,
            phrase_limit=args.pez_phrase_limit,
        )

    data = merge_rounds(evolution, pez, final_limit_per_target=args.final_limit_per_target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote:", args.output)
    print("Total prompts:", sum(len(entries) for entries in data.values()))
    for target, entries in data.items():
        sources = sorted({entry.get("source", "") for entry in entries})
        print(target, len(entries), sources)


if __name__ == "__main__":
    main()
