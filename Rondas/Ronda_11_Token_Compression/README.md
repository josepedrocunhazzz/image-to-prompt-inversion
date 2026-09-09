# Ronda 11 - Token Compression

## Objetivo

Remover redundâncias e comprimir os prompts para controlar o contexto efetivo do
encoder CLIP, mantendo primeiro os atributos mais discriminativos.

## Conteúdo

- `codigo/src/gerar_ronda_11_token_compression.py`: gera prompts compactos.
- `codigo/src/search_multiseed_validate.py`: validação em duas fases.
- `codigo/tests/test_ronda_11.py`: teste estrutural.
- `notebook/TP2_RunAll_Ronda_11.ipynb`: execução da ronda.
- `resultados/stage1_fixed_seed_metrics.csv`: métricas com seed oficial.
- `resultados/stage2_aux_seed_metrics.csv`: robustez em seeds auxiliares.
- `resultados/*_robust_prompt_ranking.csv`: ranking por target.
- `resultados/top12_robust_fixed_seed.csv`: candidatos finais.
- `resultados/contact_sheet_top12_robust.jpg`: comparação visual.

## Conclusão

Prompts concisos e diagnósticos foram mais fáceis de controlar, mas a compressão
isolada não resolveu a geometria dos targets complexos.
