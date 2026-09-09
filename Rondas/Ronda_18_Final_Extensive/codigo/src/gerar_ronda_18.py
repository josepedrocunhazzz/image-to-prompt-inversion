from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from tp2_prompt_gen import make_entry, unique_keep_order


SOURCE = "round41_final_extensive"
COUNTS = {
    "1159_25.png": 500,
    "1159_29.png": 900,
    "1159_3.png": 750,
    "1159_7.png": 850,
    "7836.png": 900,
    "9338.png": 1000,
}


def join_parts(*parts: str) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def sample_prompts(prompts: list[str], limit: int, seed: int, head_size: int = 220) -> list[str]:
    prompts = unique_keep_order(prompts)
    if len(prompts) <= limit:
        return prompts
    rng = random.Random(seed)
    head = prompts[: min(head_size, limit)]
    tail = prompts[min(head_size, len(prompts)) :]
    rng.shuffle(tail)
    return head + tail[: limit - len(head)]


def ablate(parts: list[str], min_parts: int = 4) -> list[str]:
    prompts = [join_parts(*parts)]
    for index in range(len(parts)):
        kept = [part for i, part in enumerate(parts) if i != index]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    for i, j in itertools.combinations(range(len(parts)), 2):
        kept = [part for k, part in enumerate(parts) if k not in {i, j}]
        if len(kept) >= min_parts:
            prompts.append(join_parts(*kept))
    return prompts


def reorder_cores(core: list[str], tails: list[str], max_orders: int = 48) -> list[str]:
    prompts: list[str] = []
    for order in list(itertools.permutations(core))[:max_orders]:
        prompts.append(join_parts(*order, *tails))
    return prompts


def product_prompts(*groups: list[str]) -> list[str]:
    return [join_parts(*parts) for parts in itertools.product(*groups)]


def entries_for(target: str, prompts: list[str], seed: int) -> list[dict[str, str]]:
    prompts = sample_prompts(prompts, limit=COUNTS[target], seed=seed)
    return [make_entry(target, prompt, index + 1, "", SOURCE) for index, prompt in enumerate(prompts)]


def orange_juice_prompts() -> list[dict[str, str]]:
    target = "1159_25.png"
    anchor = [
        "realistic orange juice still life",
        "single tall clear glass of creamy orange juice",
        "curved yellow fruit garnish on the rim",
        "two bright orange slices behind the glass",
        "round wooden plate cropped on the left",
        "small citrus cubes scattered on brown tabletop",
        "warm product photography",
    ]
    subjects = [
        "realistic orange juice still life",
        "warm citrus drink product photo",
        "single tall glass of creamy orange juice",
        "minimal orange juice tabletop scene",
        "studio orange juice still life",
    ]
    glass = [
        "single tall clear glass of creamy orange juice",
        "transparent glass with pale orange juice",
        "centered glass with smooth orange drink",
        "clear tumbler filled with creamy orange liquid",
    ]
    garnish = [
        "curved yellow fruit garnish on the rim",
        "banana shaped yellow garnish on glass rim",
        "small pineapple colored garnish over the rim",
        "orange slice pair on right rim",
        "yellow garnish and orange slice on rim",
    ]
    background = [
        "two bright orange slices behind the glass",
        "round wooden plate cropped on the left",
        "large orange slice at lower right",
        "simple brown tabletop with orange halves",
        "minimal citrus pieces around the glass",
    ]
    details = [
        "small citrus cubes scattered on brown tabletop",
        "tiny orange chunks in the foreground",
        "smooth warm brown surface",
        "thin clear glass rim and reflective base",
    ]
    style = [
        "warm product photography",
        "realistic studio food photo",
        "soft warm commercial lighting",
        "clean realistic tabletop photo",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:6], [anchor[6]]))
    prompts.extend(product_prompts(subjects, glass, garnish, background, details, style))
    return entries_for(target, prompts, seed=4125)


def palm_prompts() -> list[dict[str, str]]:
    target = "1159_29.png"
    anchor = [
        "single palm tree trunk rising from shallow turquoise ocean",
        "large foamy waves in the foreground",
        "white surf swirling around the tree roots",
        "low sunset reflection behind the trunk",
        "grey cloud bank on the right",
        "distant island silhouette on right horizon",
        "realistic muted beach photograph",
    ]
    subject = [
        "single palm tree trunk rising from shallow turquoise ocean",
        "solitary palm tree in choppy shallow water",
        "slender palm tree rooted in foamy surf",
        "tropical palm tree standing in ocean waves",
        "palm tree at sunset in turquoise sea",
    ]
    waves = [
        "large foamy waves in the foreground",
        "white surf swirling around the tree roots",
        "choppy turquoise ocean with bigger wave crests",
        "rolling foreground waves with white foam",
        "shallow water wave breaking around the trunk",
        "glossy reflected wave surface in front",
    ]
    sky = [
        "low sunset reflection behind the trunk",
        "soft sunset glow near the horizon",
        "grey cloud bank on the right",
        "muted pastel sunset sky",
        "bright sun low over the water",
    ]
    horizon = [
        "distant island silhouette on right horizon",
        "mountain island far right",
        "flat ocean horizon behind foamy water",
        "small dark island shape at far right",
    ]
    style = [
        "realistic muted beach photograph",
        "natural ocean photography",
        "cinematic tropical seascape",
        "soft realistic coastal photo",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:6], [anchor[6]]))
    prompts.extend(product_prompts(subject, waves, sky, horizon, style))
    prompts.extend(product_prompts(subject[:4], waves, waves[:3], sky, horizon, style[:3]))
    return entries_for(target, prompts, seed=4129)


def warrior_prompts() -> list[dict[str, str]]:
    target = "1159_3.png"
    anchor = [
        "single stern blond anime warrior mage",
        "pale off white armor with silver plates",
        "curved yellow energy blade crossing the torso",
        "teal ghost smoke cloud on the left",
        "orange smoke blob behind right shoulder",
        "flat painterly anime concept art",
        "centered square composition",
    ]
    subject = [
        "single stern blond anime warrior mage",
        "blond armored anime fighter",
        "serious blond warrior in pale armor",
        "fantasy anime swordsman with energy blade",
        "centered blond battle mage",
    ]
    armor = [
        "pale off white armor with silver plates",
        "light grey segmented armor",
        "matte silver shoulder armor",
        "white chest armor with grey metal edges",
        "compact anime armor silhouette",
    ]
    blade = [
        "curved yellow energy blade crossing the torso",
        "thin amber arc blade across the lower body",
        "glowing yellow curved sword at the waist",
        "diagonal golden energy slash across front",
        "orange yellow blade sweeping from lower left to right",
    ]
    background = [
        "teal ghost smoke cloud on the left",
        "orange smoke blob behind right shoulder",
        "blue green mist and orange fire clouds behind",
        "dark grey smoky background",
        "soft teal and orange elemental smoke",
    ]
    style = [
        "flat painterly anime concept art",
        "soft brushwork square crop",
        "low contrast character illustration",
        "semi realistic anime game art",
        "centered square composition",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:6], [anchor[6]]))
    prompts.extend(product_prompts(subject, armor, blade, background, style))
    prompts.extend(product_prompts(subject[:4], armor, blade, background[:3], background[3:], style[:3]))
    return entries_for(target, prompts, seed=4103)


def cube_prompts() -> list[dict[str, str]]:
    target = "1159_7.png"
    anchor = [
        "small hedgehog emerging from a wooden cube",
        "sharp 4 by 4 wooden cube grid sides",
        "visible individual square blocks on front and right faces",
        "tiny hidden face under orange spiky fur",
        "amber quills only on the top surface",
        "warm brown studio object photo",
    ]
    subject = [
        "small hedgehog emerging from a wooden cube",
        "compact cubical hedgehog object",
        "hedgehog nestled in a peach wooden block cube",
        "tiny spiky animal inside square wooden cube",
        "cube shaped hedgehog sculpture",
    ]
    grid = [
        "sharp 4 by 4 wooden cube grid sides",
        "visible individual square blocks on front and right faces",
        "regular peach square lattice sides",
        "vertical block columns on cube faces",
        "front and side faces made of small wooden blocks",
        "clear cubical perspective with grid sides",
    ]
    face = [
        "tiny hidden face under orange spiky fur",
        "small dark nose buried in top fur",
        "tiny eyes partly hidden below quills",
        "small centered face at the top front edge",
    ]
    top = [
        "amber quills only on the top surface",
        "low square cap of orange spines",
        "spiky fur crown sitting on the cube top",
        "radial amber quills emerging from top opening",
    ]
    style = [
        "warm brown studio object photo",
        "realistic macro product photo",
        "soft warm tabletop lighting",
        "centered studio crop",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:5], [anchor[5]]))
    prompts.extend(product_prompts(subject, grid, face, top, style))
    prompts.extend(product_prompts(subject[:4], grid, grid[:3], face, top, style[:3]))
    return entries_for(target, prompts, seed=4107)


def astronaut_prompts() -> list[dict[str, str]]:
    target = "7836.png"
    anchor = [
        "tiny astronaut standing bottom center",
        "curved dark planet horizon at the bottom",
        "massive diagonal pink planet band crossing the sky",
        "slanted planetary ring from lower left to upper right",
        "dark blue black starfield",
        "subtle blue nebula clouds around the edges",
        "cinematic realistic space landscape",
    ]
    subject = [
        "tiny astronaut standing bottom center",
        "small space explorer at lower edge",
        "rim lit astronaut on curved planet surface",
        "small suited figure looking up",
        "tiny astronaut on dark rocky horizon",
    ]
    planet = [
        "curved dark planet horizon at the bottom",
        "thin curved ground arc under the astronaut",
        "dark rocky planet surface below the figure",
        "clean crescent planet foreground",
    ]
    band = [
        "massive diagonal pink planet band crossing the sky",
        "slanted planetary ring from lower left to upper right",
        "wide pale pink diagonal planetary stripe",
        "huge tilted pink planet arc across space",
        "broad diagonal rose colored celestial band",
        "large sloping planet surface cutting across the upper sky",
    ]
    sky = [
        "dark blue black starfield",
        "subtle blue nebula clouds around the edges",
        "sparse stars in deep black space",
        "cold blue cosmic dust at image corners",
    ]
    style = [
        "cinematic realistic space landscape",
        "high contrast sci fi concept art",
        "moody realistic space illustration",
        "dramatic square space scene",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:6], [anchor[6]]))
    prompts.extend(product_prompts(subject, planet, band, sky, style))
    prompts.extend(product_prompts(subject[:4], planet, band, band[:3], sky, style[:3]))
    return entries_for(target, prompts, seed=4178)


def hamster_prompts() -> list[dict[str, str]]:
    target = "9338.png"
    anchor = [
        "orange colorful fantasy hamster creature",
        "three quarter left profile",
        "localized teal belly jewel",
        "rainbow red purple yellow scales on lower body",
        "blue teal shoulder scale patch",
        "small paws near belly",
        "orange yellow flame aura",
        "storybook painterly illustration",
    ]
    subject = [
        "orange colorful fantasy hamster creature",
        "compact jewel bellied fantasy hamster",
        "small rainbow quilled hamster creature",
        "cute spiny fantasy hamster with orange body",
        "orange teal fantasy hamster with scales",
        "storybook magical hamster creature",
    ]
    pose = [
        "three quarter left profile",
        "head turned left with compact body",
        "soft left profile pose",
        "single creature looking left",
        "slightly turned left silhouette",
    ]
    belly = [
        "localized teal belly jewel",
        "central blue green oval belly medallion",
        "clear turquoise chest gem",
        "teal spiral belly jewel",
        "small teal belly patch on orange body",
    ]
    color = [
        "rainbow red purple yellow scales on lower body",
        "multicolor mosaic scales across orange body",
        "purple red yellow blue spotted body scales",
        "rainbow scale quills on shoulder and back",
        "blue teal shoulder scale patch",
        "orange body with scattered rainbow scales",
    ]
    body = [
        "compact cute body",
        "small paws near belly",
        "tiny claws close to torso",
        "rounded orange body",
        "short ears and orange snout",
    ]
    aura = [
        "orange yellow flame aura",
        "dark teal multicolor fire background",
        "warm fire ribbons behind",
        "soft rainbow flame shapes behind",
        "yellow orange painterly aura",
    ]
    style = [
        "storybook painterly illustration",
        "soft fantasy creature portrait",
        "vertical storybook painting",
        "warm brushwork fantasy portrait",
    ]
    prompts = list(ablate(anchor))
    prompts.extend(reorder_cores(anchor[:7], [anchor[7]], max_orders=60))
    prompts.extend(product_prompts(subject, pose, belly, color, body, aura, style))
    prompts.extend(product_prompts(subject, pose, belly, color[:4], color[4:], body[:3], aura[:3], style[:3]))
    return entries_for(target, prompts, seed=4193)


def build_round() -> dict[str, list[dict[str, str]]]:
    return {
        "1159_25.png": orange_juice_prompts(),
        "1159_29.png": palm_prompts(),
        "1159_3.png": warrior_prompts(),
        "1159_7.png": cube_prompts(),
        "7836.png": astronaut_prompts(),
        "9338.png": hamster_prompts(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TP2 round-41 final extensive prompt bank.")
    parser.add_argument("--output", type=Path, default=Path("prompts/refinement_round41_final_extensive.json"))
    args = parser.parse_args()

    data = build_round()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {sum(len(entries) for entries in data.values())} prompts to {args.output}")
    print({target: len(entries) for target, entries in data.items()})


if __name__ == "__main__":
    main()
