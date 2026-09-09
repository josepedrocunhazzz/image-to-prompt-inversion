# Ronda 10 - Hybrid Multiseed

## Objetivo

Combinar prompts das rondas anteriores e avaliar a sua robustez com seeds
auxiliares, mantendo a seed oficial para os renders submetidos.

## Conteúdo

- `codigo/src/gerar_ronda_10_hybrid_multiseed.py`: banco híbrido.
- `codigo/src/search_multiseed_validate.py`: pesquisa em duas fases.
- `codigo/tests/test_ronda_10.py`: teste do gerador.
- `notebook/TP2_RunAll_Ronda_10.ipynb`: execução Run All.
- `resultados/stage1_fixed_seed_metrics.csv`: pesquisa com seed oficial.
- `resultados/stage2_aux_seed_metrics.csv`: validação auxiliar.
- `resultados/*_robust_prompt_ranking.csv`: ranking de robustez por target.
- `resultados/top12_robust_fixed_seed.csv`: seleção final novamente na seed oficial.
- `resultados/contact_sheet_top12_robust.jpg`: inspeção visual.

## Conclusão

A ronda filtrou coincidências favoráveis de uma única seed e melhorou a
avaliação de robustez, sem substituir o critério oficial fixed-seed.
