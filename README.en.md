# Image-to-Prompt Inversion

[Português](README.md) | [English](README.en.md)

An experimental pipeline for recovering text prompts capable of reproducing
six target images with a fixed diffusion model and seed. The task is framed as
a measurable discrete prompt-search problem rather than ordinary image
captioning.

## Approach

The project evolved through 23 documented rounds. Each round tests a focused
hypothesis: CLIP-guided search, visual anchors, prompt evolution, token
compression, large-scale variations, multi-seed validation, ablation, targeted
corrections and per-target refinement.

```mermaid
flowchart LR
    A[Target image] --> B[Prompt bank]
    B --> C[LCM DreamShaper v7]
    C --> D[Candidate images]
    D --> E[CLIP + LPIPS + RMSE + SSIM]
    E --> F[Ranking and Pareto]
    F --> G[Limited visual review]
    G --> H[Top 3 per target]
```

The ranking combines complementary metrics:

- CLIP for semantic similarity;
- LPIPS for perceptual distance;
- RMSE and SSIM for pixel-level and structural similarity;
- target-specific color, edge and layout metrics in later rounds;
- auxiliary multi-seed validation for robustness while preserving the official
  seed for final selection.

## Final results

Three prompts were selected for each of the six targets. The best comparable
score per target reported in the paper was:

| Target | Content | Best score |
| --- | --- | ---: |
| `1159_25` | Orange juice | 0.851 |
| `1159_29` | Palm tree in the ocean | 0.780 |
| `1159_3` | Anime warrior | 0.708 |
| `1159_7` | Cube-bodied hedgehog | 0.822 |
| `7836` | Astronaut | 0.829 |
| `9338` | Fantasy hamster | 0.743 |

Targets with a stable global identity and compact layout were easier to
reproduce. The warrior and hamster demonstrate the main difficulty of
text-only inversion: small wording changes can alter pose, anatomy and geometry.

One important negative result was that longer prompts did not consistently
improve quality. The strongest candidates use a small number of ordered visual
blocks — subject, material/color, composition, background and style — followed
by controlled local mutations.

## Reproduction

A PyTorch-compatible GPU is recommended. The
`SimianLuo/LCM_Dreamshaper_v7` checkpoint is downloaded from Hugging
Face during the first run.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Every directory under `Rondas/` includes its own README, notebook, scripts,
tests and results. For example:

```bash
python Rondas/Ronda_01_CLIP_Guided/codigo/src/gerar_ronda_01_clip_guided.py
pytest Rondas/Ronda_01_CLIP_Guided/codigo/tests
```

Offline execution requires the checkpoint to be present in the local Hugging
Face cache. Reproducing all 23 rounds is expensive; the final prompts, CSV
files, rankings, selected images and contact sheets are the main validation
artifacts.

## Repository structure

```text
image-to-prompt-inversion/
├── targets/                    # Six target images
├── Rondas/                     # History of 23 experiments
│   └── Ronda_XX_*/
│       ├── codigo/
│       ├── notebook/
│       └── resultados/
├── dados/                      # Consolidated rankings and final prompts
├── relatorio/
│   ├── Relatorio.pdf
│   └── fonte/                  # LaTeX source and build artifacts
├── requirements.txt
├── README.md
└── README.en.md
```

`dados/final_current_top3.csv` is the authoritative link between target, rank,
prompt, metrics, image and source round. The full report is available at
[relatorio/Relatorio.pdf](relatorio/Relatorio.pdf).

## Skills demonstrated

Diffusion models, systematic prompt engineering, CLIP, perceptual metrics,
iterative experimentation, top-k search, seed control, automated tests and
result traceability.

## Academic context

Developed by José Cunha and Gabriel Pinto. The results represent prompt
inversion under fixed model and seed constraints, not a general exact-image
reconstruction method.
