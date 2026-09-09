#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BEST_CSV = ROOT.parent.parent / "best_of_runs" / "best_of_runs.csv"
INGLES_DIR = ROOT / "ingles"
CN_DIR = ROOT / "chines"
INGLES_COUNT = 1_000
CN_COUNT = 200


def read_top_prompts() -> dict[str, dict[str, object]]:
    rows_by_target: dict[str, list[dict[str, str]]] = {}
    with BEST_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            target = row["target_name"]
            rows_by_target.setdefault(target, []).append(row)

    result: dict[str, dict[str, object]] = {}
    for target_name, rows in rows_by_target.items():
        sorted_rows = sorted(rows, key=lambda r: float(r.get("cross_run_score") or 0.0), reverse=True)
        prompts_raw = [r["prompt"].strip() for r in sorted_rows]
        unique_prompts: list[str] = []
        seen: set[str] = set()
        for prompt in prompts_raw:
            if prompt in seen:
                continue
            seen.add(prompt)
            unique_prompts.append(prompt)
        category = target_name.replace(".png", "")
        result[category] = {
            "target_name": target_name,
            "top_rows_prompts": prompts_raw[:5],
            "top_unique_prompts": unique_prompts[:5],
        }
    return result


INGLES_BLOCKS: dict[str, list[dict[str, object]]] = {
    "1159_25": [
        {"name": "scene", "base": 0, "options": [
            "photorealistic orange juice still life",
            "realistic orange juice still life",
            "orange juice still life",
            "photorealistic citrus drink still life",
            "warm orange juice still life",
            "clean citrus drink still life",
        ]},
        {"name": "glass", "base": 0, "options": [
            "single clear glass",
            "single tall clear glass",
            "clear cylindrical glass",
            "straight clear glass",
            "single minimalist clear glass",
            "single central clear glass",
        ]},
        {"name": "liquid", "base": 0, "options": [
            "pale creamy orange juice",
            "pale orange juice",
            "light creamy orange juice",
            "soft pale orange juice",
            "muted orange juice",
            "smooth pale orange smoothie",
        ]},
        {"name": "garnish", "base": 0, "options": [
            "small orange garnish on the rim",
            "orange slice on the rim",
            "tiny orange garnish on the rim",
            "small orange wedge on the rim",
            "paired orange slices on the rim",
            "thin orange slice on the rim",
        ]},
        {"name": "foreground", "base": 0, "options": [
            "scattered pale citrus cubes on brown tabletop",
            "scattered tiny citrus pieces on brown tabletop",
            "orange halves and tiny cubes on a smooth brown surface",
            "small pale citrus cubes in foreground",
            "minimal citrus pieces on brown studio surface",
            "diced citrus pieces on warm brown tabletop",
        ]},
        {"name": "style", "base": 0, "options": [
            "warm realistic product photo",
            "realistic food photography",
            "soft depth of field",
            "soft realistic product photo",
            "clean studio product photo",
            "natural product photo",
        ]},
    ],
    "1159_29": [
        {"name": "subject", "base": 0, "options": [
            "single slender palm tree rising from shallow turquoise ocean",
            "single slender palm tree in calm turquoise water",
            "single isolated slender palm tree in shallow turquoise water",
            "solitary slender palm tree in shallow ocean",
            "single delicate palm tree in calm turquoise sea",
            "single slender tropical palm tree in shallow water",
        ]},
        {"name": "foreground", "base": 0, "options": [
            "shallow surf and reflective water in foreground",
            "water fills foreground around the palm",
            "gentle surf and reflective foreground water",
            "calm reflective water in foreground",
            "small waves at the trunk base",
            "soft reflective turquoise foreground water",
        ]},
        {"name": "sun", "base": 0, "options": [
            "low sun reflection behind the tree",
            "low sunset reflection behind the tree",
            "soft pale sunset haze",
            "warm sun glow behind the tree",
            "golden reflection behind the palm",
            "muted sunset reflection behind the tree",
        ]},
        {"name": "horizon", "base": 0, "options": [
            "",
            "faint distant land on right horizon",
            "hazy island silhouette on right horizon",
            "subtle right horizon landform",
            "very soft distant coastline",
            "minimal horizon detail",
        ]},
        {"name": "water_color", "base": 0, "options": [
            "clear turquoise ocean",
            "calm turquoise water",
            "shallow turquoise sea",
            "gentle turquoise water",
            "soft teal ocean water",
            "bright turquoise tropical water",
        ]},
        {"name": "style", "base": 0, "options": [
            "soft atmospheric tropical photo",
            "natural ocean photograph",
            "muted colors",
            "soft hazy tropical photo",
            "warm tropical sunset photo",
            "realistic tropical seascape photo",
        ]},
    ],
    "1159_3": [
        {"name": "subject", "base": 0, "options": [
            "single blond anime warrior mage in reflective silver armor",
            "single blond anime warrior in reflective silver armor",
            "single stern blond anime warrior mage in reflective silver armor",
            "single blond fantasy warrior mage in reflective silver armor",
            "single blond armored mage",
            "blond anime warrior mage in reflective silver armor",
        ]},
        {"name": "energy", "base": 0, "options": [
            "diagonal yellow energy blade across the waist",
            "curved amber energy blade crossing the lower body",
            "warm yellow blade arc across lower frame",
            "golden blade glow at the bottom edge",
            "yellow energy arc across the torso",
            "yellow glowing energy streak across the waist",
        ]},
        {"name": "background", "base": 0, "options": [
            "blue green mist and orange fire clouds behind",
            "cyan mist and orange fire clouds behind",
            "blue green spectral haze and orange fire clouds behind",
            "blue green haze and orange flames behind",
            "moody blue green mist and orange fire clouds behind",
            "spectral blue green mist and orange fire clouds behind",
        ]},
        {"name": "mood", "base": 0, "options": [
            "soft brushwork",
            "moody anime key art",
            "desaturated anime concept art",
            "painterly dark fantasy mood",
            "soft painterly finish",
            "dramatic fantasy lighting",
        ]},
        {"name": "frame", "base": 0, "options": [
            "square crop",
            "tight square crop",
            "centered square composition",
            "portrait-like square framing",
            "high detail square crop",
            "balanced square framing",
        ]},
        {"name": "tone", "base": 0, "options": [
            "low contrast",
            "subdued color palette",
            "dark concept art tone",
            "soft shadowed lighting",
            "high detail fantasy illustration",
            "moody portrait rendering",
        ]},
    ],
    "1159_7": [
        {"name": "subject", "base": 0, "options": [
            "small hedgehog with compact cubical wooden block body",
            "tiny hedgehog with compact cubical wooden block body",
            "small studio hedgehog with compact wooden block body",
            "little hedgehog with compact cube body",
            "tiny studio hedgehog with compact cubical body",
            "small hedgehog with compact wooden cube body",
        ]},
        {"name": "body_grid", "base": 0, "options": [
            "warm peach beige 4 by 4 cube grid sides",
            "warm peach beige cube grid sides",
            "peach beige 4 by 4 grid sides",
            "soft peach beige cube grid sides",
            "warm sandy beige cube grid sides",
            "beige cube grid sides",
        ]},
        {"name": "face", "base": 0, "options": [
            "tiny face mostly hidden below orange spiky fur",
            "small face mostly hidden below orange spiky fur",
            "tiny hidden face below orange fur",
            "tiny face tucked below orange fur",
            "small hidden face below orange spiky fur",
            "face mostly hidden below orange spiky fur",
        ]},
        {"name": "quills", "base": 0, "options": [
            "amber quill fur only on the top surface",
            "spiky amber bristles forming a square top cap",
            "soft amber bristles forming a low square cap on top",
            "orange spiky fur only on the top surface",
            "soft amber quills on the top surface",
            "tiny amber quills on the top surface",
        ]},
        {"name": "material", "base": 0, "options": [
            "soft timber block texture",
            "subtle wood block texture",
            "clean timber cube texture",
            "matte wooden block texture",
            "light studio wood texture",
            "fine grain wood texture",
        ]},
        {"name": "style", "base": 0, "options": [
            "realistic studio object photo",
            "soft shallow depth of field",
            "clean studio object photo",
            "neutral studio product photo",
            "warm studio lighting",
            "soft studio lighting",
        ]},
    ],
    "7836": [
        {"name": "subject", "base": 0, "options": [
            "small space explorer at bottom edge",
            "small astronaut at bottom edge",
            "tiny space explorer at bottom edge",
            "small helmeted explorer at lower edge",
            "small space traveler at bottom edge",
            "tiny astronaut near the lower edge",
        ]},
        {"name": "stripe", "base": 0, "options": [
            "sloping pink white cosmic dust stripe in empty sky",
            "sloping pink white cosmic dust stripe across empty sky",
            "diagonal pink white cosmic dust stripe in empty sky",
            "broad pale pink cosmic dust stripe in empty sky",
            "soft pink white nebula stripe in empty sky",
            "wide sloping cosmic dust band in empty sky",
        ]},
        {"name": "sky", "base": 0, "options": [
            "moody blue black cosmic background",
            "empty dark blue starfield",
            "deep blue black cosmic background",
            "dark cosmic background",
            "shadowy blue black sky",
            "near black starfield background",
        ]},
        {"name": "ground", "base": 0, "options": [
            "small rim-lit grey ground below the figure",
            "tiny rim-lit grey ground below the explorer",
            "small grey ground below the figure",
            "thin grey ground below the figure",
            "faint grey ground below the figure",
            "narrow rim-lit ground below the character",
        ]},
        {"name": "style", "base": 0, "options": [
            "dark high contrast digital painting",
            "realistic sci fi landscape",
            "moody high contrast digital painting",
            "dark sci fi concept art",
            "cinematic sci fi painting",
            "moody space painting",
        ]},
        {"name": "framing", "base": 0, "options": [
            "",
            "square crop",
            "tight square crop",
            "centered crop",
            "balanced crop",
            "clean centered framing",
        ]},
    ],
    "9338": [
        {"name": "subject", "base": 0, "options": [
            "colorful dragon hamster with orange face and teal belly",
            "rainbow dragon hamster with orange snout and blue green oval belly",
            "small dragon hamster with orange face and teal belly",
            "bright fantasy hamster with orange snout and teal belly",
            "storybook dragon hamster with orange face and teal belly",
            "rainbow fantasy hamster with orange snout and teal belly",
        ]},
        {"name": "quills", "base": 0, "options": [
            "rainbow quills behind the back",
            "colorful bristles around the shoulders",
            "rainbow quills behind the shoulders",
            "orange yellow blue spines",
            "colorful spines behind the back",
            "bright rainbow quills behind the back",
        ]},
        {"name": "paws", "base": 0, "options": [
            "tiny clawed paws",
            "small paws near the belly",
            "tiny paws near the belly",
            "small clawed paws",
            "tiny forepaws near the belly",
            "small front paws near the belly",
        ]},
        {"name": "style", "base": 0, "options": [
            "vertical storybook illustration",
            "painterly fantasy background",
            "vertical fantasy illustration",
            "storybook creature illustration",
            "illustrated fantasy portrait",
            "storybook fantasy art",
        ]},
        {"name": "background", "base": 0, "options": [
            "",
            "soft colorful background",
            "gentle pastel background",
            "clean illustration background",
            "bright fantasy portrait background",
            "soft fantasy background",
        ]},
        {"name": "lighting", "base": 0, "options": [
            "warm lighting",
            "soft lighting",
            "bright lighting",
            "gentle lighting",
            "storybook lighting",
            "soft pastel lighting",
        ]},
    ],
}


CN_BLOCKS: dict[str, list[dict[str, object]]] = {
    "1159_25": [
        {"name": "构图", "base": 0, "options": ["单杯居中构图", "玻璃杯略偏右", "紧凑静物构图", "产品摄影构图", "前景留白更多", "杯口细节优先"]},
        {"name": "液体", "base": 0, "options": ["浅橙色奶油质感果汁", "淡橙色果汁", "顺滑浅橙色果昔", "更透明的浅橙液体", "柔和低饱和橙色", "均匀细腻液面"]},
        {"name": "杯口装饰", "base": 0, "options": ["杯口小橙片", "杯口薄橙片", "杯口迷你橙角", "杯口双层橙片", "杯口单片装饰", "杯口极简柑橘装饰"]},
        {"name": "质感", "base": 0, "options": ["暖棕色桌面", "磨砂棕色台面", "柔和棚拍光", "真实食品摄影", "浅景深", "自然产品照"]},
    ],
    "1159_29": [
        {"name": "主体", "base": 0, "options": ["单棵细长棕榈树", "孤立棕榈树", "细长棕榈位于画面中央", "远景单树", "细高棕榈树干", "极简海景单树"]},
        {"name": "海水", "base": 0, "options": ["浅青绿色海水", "平静青绿色海面", "浅海反光水面", "前景柔和浪花", "清澈热带海水", "轻微波纹海面"]},
        {"name": "光线", "base": 0, "options": ["树后低位日光反射", "日落反射光", "柔和金色反光", "淡雾夕阳氛围", "低对比暖光", "远处微弱光带"]},
        {"name": "风格", "base": 0, "options": ["自然海景照片", "柔和热带氛围照", "低饱和摄影", "轻雾感热带照片", "真实海洋摄影", "安静极简海景"]},
    ],
    "1159_3": [
        {"name": "角色", "base": 0, "options": ["金发动漫战斗法师", "银色反光盔甲角色", "严肃表情金发战士", "奇幻盔甲法师", "居中半身角色", "单角色构图"]},
        {"name": "能量刃", "base": 0, "options": ["腰部斜向黄色能量刃", "下半身弧形琥珀能量刃", "底部金色刀光", "暖黄色能量弧线", "发光黄色刃线", "更细的能量轨迹"]},
        {"name": "背景", "base": 0, "options": ["蓝绿色雾气与橙色火云", "青蓝灵雾与橙色火焰", "暗色奇幻烟雾背景", "低饱和火云背景", "戏剧化云雾氛围", "深色概念背景"]},
        {"name": "画风", "base": 0, "options": ["柔和笔触", "偏情绪化动漫关键视觉", "去饱和概念艺术", "方形裁切", "暗调奇幻插画", "柔和阴影渲染"]},
    ],
    "1159_7": [
        {"name": "主体", "base": 0, "options": ["小刺猬方块木质身体", "紧凑立方体木块刺猬", "迷你刺猬产品照", "棚拍小型立方体角色", "木块主体更规整", "方块化刺猬"]},
        {"name": "表面", "base": 0, "options": ["暖桃米色四乘四格纹侧面", "米桃色格纹木块", "柔和浅木纹", "细腻木材纹理", "哑光木质触感", "更干净的木纹结构"]},
        {"name": "面部与毛刺", "base": 0, "options": ["脸部大多藏在橙色刺毛下", "微小面部被毛发遮挡", "顶部琥珀色刺毛方帽", "顶部低矮刺毛层", "顶部刺毛更整齐", "仅顶部有刺毛"]},
        {"name": "风格", "base": 0, "options": ["真实棚拍物体照", "柔和浅景深", "中性棚拍光", "产品摄影风格", "干净白棚背景", "柔和工作室光线"]},
    ],
    "7836": [
        {"name": "主体", "base": 0, "options": ["底部小型太空探索者", "底边小宇航员", "极小人物位于下沿", "下方单角色", "头盔探索者", "低位角色构图"]},
        {"name": "天空条带", "base": 0, "options": ["斜向粉白宇宙尘带", "宽幅粉白星云带", "淡粉色尘带横跨天空", "柔和粉白斜线云带", "稀薄粉白宇宙条纹", "明显对角尘带"]},
        {"name": "背景", "base": 0, "options": ["蓝黑宇宙背景", "深蓝空旷星场", "近黑色太空背景", "低照度宇宙环境", "阴郁深空底色", "冷色黑蓝天空"]},
        {"name": "地面与风格", "base": 0, "options": ["人物下方小片灰色轮廓地面", "高反差数字绘画", "科幻概念画风", "电影感科幻绘画", "方形构图", "暗调空间绘画"]},
    ],
    "9338": [
        {"name": "主体", "base": 0, "options": ["彩色龙仓鼠橙色脸青绿色腹部", "彩虹龙仓鼠橙色口鼻蓝绿色腹部", "童话风龙仓鼠", "亮色奇幻仓鼠", "单角色竖构图", "居中角色"]},
        {"name": "背刺", "base": 0, "options": ["背后彩虹刺毛", "肩后彩色鬃刺", "橙黄蓝三色背刺", "柔和彩虹刺", "更密集背部刺毛", "背部彩色脊刺"]},
        {"name": "爪子", "base": 0, "options": ["小巧带爪前爪", "前爪贴近腹部", "迷你前爪", "小爪子更清晰", "短小爪部细节", "双前爪靠近身体"]},
        {"name": "风格", "base": 0, "options": ["竖版童话插画", "绘本风奇幻背景", "柔和粉彩背景", "明亮插画照明", "故事书角色插画", "干净插画背景"]},
    ],
}


CN_SEEDS: dict[str, list[str]] = {
    "1159_25": [
        "写实橙汁静物，杯口小橙片，棕色桌面有浅色柑橘小块，温暖产品摄影",
        "淡橙色果昔置于直筒玻璃杯，杯口橙片，前景有细小柑橘颗粒，柔和景深",
        "高透明高杯中的浅奶油质感橙汁，杯口橙片，棕色台面上有橙块，真实食品摄影",
    ],
    "1159_29": [
        "单棵细长棕榈树立于浅青绿海水中，前景反光水面，树后低位日光反射，柔和热带照片",
        "单棵细长棕榈树位于平静青绿色海面，前景被海水覆盖，低位夕阳反光，自然海景摄影",
        "孤立棕榈树与浅海水面，前景平静反光，轻微夕阳薄雾，低饱和海洋照片",
    ],
    "1159_3": [
        "金发动漫战斗法师，银色反光盔甲，腰部斜向黄色能量刃，背后蓝绿雾与橙色火云，柔和笔触方形构图",
        "金发动漫战斗法师，银色盔甲，下半身琥珀色弧形能量刃，背后蓝绿雾与火云，情绪化关键视觉",
        "金发盔甲法师，底部金色刀光，蓝绿雾与橙色火云背景，去饱和奇幻概念画",
    ],
    "1159_7": [
        "小刺猬方块木质身体，暖桃米色四乘四格纹侧面，面部被橙色刺毛遮挡，顶部琥珀刺毛，真实棚拍",
        "紧凑立方体木块刺猬，微小面部隐藏在刺毛下，顶部低矮方形刺毛帽，浅景深产品照",
        "方块化刺猬木质主体，米桃色格纹，顶部刺毛更规整，仅顶部有刺毛，工作室光线",
    ],
    "7836": [
        "底部小型太空探索者，天空有斜向粉白宇宙尘带，蓝黑深空背景，人物下方小片灰色地面，高反差数字绘画",
        "底边小宇航员，宽幅粉白星云带穿过空旷天空，深蓝星场背景，灰色轮廓地面，科幻概念画",
        "下方单角色构图，淡粉宇宙尘带与暗色深空，极简地面轮廓，电影感科幻绘画",
    ],
    "9338": [
        "彩色龙仓鼠，橙色脸与青绿色腹部，背后彩虹刺毛，小巧前爪，竖版童话插画",
        "彩虹龙仓鼠，橙色口鼻与蓝绿色腹部，肩后彩色鬃刺，前爪贴近腹部，绘本风奇幻背景",
        "童话风龙仓鼠，橙色面部，背部橙黄蓝三色刺，迷你爪部，明亮故事书插画",
    ],
}


def join_prompt(parts: list[str]) -> str:
    return ", ".join(part.strip() for part in parts if part and part.strip())


def combo_distance(combo: tuple[int, ...], blocks: list[dict[str, object]]) -> int:
    score = 0
    for idx, block in zip(combo, blocks):
        score += abs(idx - int(block["base"]))
    return score


def generate_from_blocks(
    seeds: list[str],
    blocks: list[dict[str, object]],
    target_count: int,
    language: str,
    include_seed_text: bool,
) -> tuple[list[dict[str, object]], int]:
    ranges = [range(len(block["options"])) for block in blocks]
    total_space = len(seeds)
    for block in blocks:
        total_space *= len(block["options"])

    rows: list[tuple[int, int, tuple[int, ...], str]] = []
    for seed_index, seed in enumerate(seeds):
        for combo in itertools.product(*ranges):
            fragments = [str(block["options"][opt_idx]) for block, opt_idx in zip(blocks, combo)]
            if language == "ingles":
                prompt_parts = [seed] + fragments if include_seed_text else fragments
                prompt = join_prompt(prompt_parts)
            else:
                prompt_parts = [seed] + fragments if include_seed_text else fragments
                prompt = "，".join([part.strip("， ").strip() for part in prompt_parts if part and part.strip()])
            dist = combo_distance(combo, blocks)
            rows.append((dist, seed_index, combo, prompt))

    rows.sort(key=lambda item: (item[0], item[1], item[2]))
    output: list[dict[str, object]] = []
    seen: set[str] = set()
    for rank, (_, seed_index, combo, prompt) in enumerate(rows, start=1):
        if prompt in seen:
            continue
        seen.add(prompt)
        output.append(
            {
                "id": f"{rank:05d}",
                "seed_index": seed_index + 1,
                "combo": list(combo),
                "prompt": prompt,
            }
        )
        if len(output) >= target_count:
            break

    if len(output) < target_count:
        raise RuntimeError(f"Generated only {len(output)} prompts, expected {target_count}")

    return output, total_space


def build_dataset() -> None:
    top_map = read_top_prompts()
    INGLES_DIR.mkdir(parents=True, exist_ok=True)
    CN_DIR.mkdir(parents=True, exist_ok=True)

    manifest_ingles: list[dict[str, object]] = []
    manifest_cn: list[dict[str, object]] = []

    categories = sorted(INGLES_BLOCKS.keys())
    for category in categories:
        if category not in top_map:
            raise KeyError(f"Category {category} missing in best_of_runs.csv")

        target_name = str(top_map[category]["target_name"])
        top_rows = list(top_map[category]["top_rows_prompts"])
        top_unique = list(top_map[category]["top_unique_prompts"])

        seeds_ingles = top_rows[:5]
        if len(seeds_ingles) < 5:
            seeds_ingles.extend(top_unique[: 5 - len(seeds_ingles)])
        if len(seeds_ingles) < 5:
            seeds_ingles.extend([top_unique[0]] * (5 - len(seeds_ingles)))

        prompts_ingles, space_ingles = generate_from_blocks(
            seeds=[""],
            blocks=INGLES_BLOCKS[category],
            target_count=INGLES_COUNT,
            language="ingles",
            include_seed_text=False,
        )
        ingles_payload = {
            "category": category,
            "target_name": target_name,
            "language": "ingles",
            "prompt_count": INGLES_COUNT,
            "top5_seed_prompts": seeds_ingles,
            "variation_blocks": INGLES_BLOCKS[category],
            "variation_space": space_ingles,
            "prompts": prompts_ingles,
        }
        ingles_path = INGLES_DIR / f"{category}.json"
        ingles_path.write_text(json.dumps(ingles_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest_ingles.append(
            {
                "category": category,
                "target_name": target_name,
                "path": str(ingles_path),
                "prompt_count": INGLES_COUNT,
                "variation_space": space_ingles,
            }
        )

        seeds_cn = CN_SEEDS[category][:3]
        prompts_cn, space_cn = generate_from_blocks(
            seeds=seeds_cn,
            blocks=CN_BLOCKS[category],
            target_count=CN_COUNT,
            language="cn",
            include_seed_text=True,
        )
        cn_payload = {
            "category": category,
            "target_name": target_name,
            "language": "zh",
            "prompt_count": CN_COUNT,
            "top3_seed_prompts_original": top_unique[:3],
            "top3_seed_prompts_cn": seeds_cn,
            "variation_blocks": CN_BLOCKS[category],
            "variation_space": space_cn,
            "prompts": prompts_cn,
        }
        cn_path = CN_DIR / f"{category}.json"
        cn_path.write_text(json.dumps(cn_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest_cn.append(
            {
                "category": category,
                "target_name": target_name,
                "path": str(cn_path),
                "prompt_count": CN_COUNT,
                "variation_space": space_cn,
            }
        )

    (INGLES_DIR / "manifest.json").write_text(json.dumps(manifest_ingles, ensure_ascii=False, indent=2), encoding="utf-8")
    (CN_DIR / "manifest.json").write_text(json.dumps(manifest_cn, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "source_csv": str(BEST_CSV),
        "ingles_dir": str(INGLES_DIR),
        "cn_dir": str(CN_DIR),
        "ingles_prompts_per_category": INGLES_COUNT,
        "cn_prompts_per_category": CN_COUNT,
        "categories": sorted(INGLES_BLOCKS.keys()),
    }
    (ROOT / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    build_dataset()
