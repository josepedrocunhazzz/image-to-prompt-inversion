# Inversão de Imagem para Prompt

[Português](README.md) | [English](README.en.md)

Pipeline experimental para recuperar prompts textuais capazes de reproduzir
seis imagens-alvo com um modelo de difusão e seed fixos. O problema é tratado
como pesquisa discreta e mensurável sobre prompts, em vez de simples image
captioning.

## Abordagem

O projeto evoluiu ao longo de 23 rondas documentadas. Cada ronda testa uma
hipótese específica: pesquisa guiada por CLIP, anchors visuais, evolução de
prompts, compressão de tokens, variações massivas, validação multi-seed,
ablação, correções dirigidas e refinamento por target.

```mermaid
flowchart LR
    A[Imagem-alvo] --> B[Banco de prompts]
    B --> C[LCM DreamShaper v7]
    C --> D[Imagens candidatas]
    D --> E[CLIP + LPIPS + RMSE + SSIM]
    E --> F[Ranking e Pareto]
    F --> G[Inspeção visual limitada]
    G --> H[Top 3 por target]
```

O ranking combina métricas complementares:

- CLIP para proximidade semântica;
- LPIPS para distância percetual;
- RMSE e SSIM para semelhança ao nível do pixel e estrutura;
- métricas específicas de cor, contornos e layout em rondas posteriores;
- validação multi-seed como teste auxiliar de robustez, mantendo a seed oficial
  na seleção final.

## Resultados finais

Foram selecionados três prompts para cada uma das seis imagens. O melhor score
comparável por target, documentado no relatório, foi:

| Target | Conteúdo | Melhor score |
| --- | --- | ---: |
| `1159_25` | Sumo de laranja | 0,851 |
| `1159_29` | Palmeira no oceano | 0,780 |
| `1159_3` | Guerreiro anime | 0,708 |
| `1159_7` | Ouriço com corpo cúbico | 0,822 |
| `7836` | Astronauta | 0,829 |
| `9338` | Hamster fantástico | 0,743 |

Os targets com identidade global e composição compacta foram mais estáveis. O
guerreiro e o hamster mostraram a principal dificuldade da inversão apenas por
texto: pequenas alterações no prompt modificam pose, anatomia e geometria.

Uma conclusão importante foi que prompts mais longos não são necessariamente
melhores. As melhores soluções usam poucos blocos visuais ordenados — sujeito,
material/cor, composição, fundo e estilo — e mutações locais controladas.

## Reprodução

Recomenda-se uma GPU compatível com PyTorch. O checkpoint
`SimianLuo/LCM_Dreamshaper_v7` é obtido através do Hugging Face na primeira
execução.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Cada pasta em `Rondas/` inclui o seu próprio README, notebook, scripts, testes e
resultados. Por exemplo:

```bash
python Rondas/Ronda_01_CLIP_Guided/codigo/src/gerar_ronda_01_clip_guided.py
pytest Rondas/Ronda_01_CLIP_Guided/codigo/tests
```

A execução offline requer que o checkpoint já esteja na cache local do Hugging
Face. A geração completa das 23 rondas é dispendiosa; para validar o trabalho,
os prompts finais, CSV, rankings, imagens selecionadas e contact sheets são os
artefactos mais relevantes.

## Estrutura

```text
image-to-prompt-inversion/
├── targets/                    # Seis imagens-alvo
├── Rondas/                     # Histórico das 23 experiências
│   └── Ronda_XX_*/
│       ├── codigo/
│       ├── notebook/
│       └── resultados/
├── dados/                      # Rankings e prompts finais consolidados
├── relatorio/
│   ├── Relatorio.pdf
│   └── fonte/                  # Fonte LaTeX e artefactos de compilação
├── requirements.txt
├── README.md
└── README.en.md
```

`dados/final_current_top3.csv` é a referência principal entre target, ranking,
prompt, métricas, imagem e ronda de origem. O relatório completo encontra-se em
[relatorio/Relatorio.pdf](relatorio/Relatorio.pdf).

## Competências demonstradas

Modelos de difusão, prompt engineering sistemático, CLIP, métricas percetuais,
experimentação iterativa, pesquisa top-k, controlo de seeds, testes automatizados
e rastreabilidade de resultados.

## Contexto académico

Projeto apresentado no portefólio de **José Cunha**. A autoria académica completa
encontra-se no relatório. Os resultados representam uma experiência de inversão
de prompts com restrições fixas de modelo e seed, não um método geral de
reconstrução exata de imagens.
