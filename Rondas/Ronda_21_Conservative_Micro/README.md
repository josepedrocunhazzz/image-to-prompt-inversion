# Ronda 21 - Conservative Micro

## Objetivo

Aplicar variações conservadoras, modificando um detalhe de cada vez para
distinguir melhorias reais de alterações globais causadas pelo prompt.

## Conteúdo

- `codigo/src/gerar_ronda_21.py`: gera variantes conservadoras.
- `codigo/src/search_seed_sweep.py`: execução na seed oficial.
- `codigo/src/evaluate_candidates.py`: métricas comparáveis.
- `notebook/TP2_RunAll_Ronda_21.ipynb`: reprodução da ronda.
- `prompts/prompts_ronda_21.json`: banco testado.
- `resultados/20260603-212442_round44_conservative_micro/`: métricas e ranking.
- `resultados/finalistas/7836/`: rank 1 do astronauta.
- `resultados/finalistas/9338/`: rank 3 da criatura fantástica.

## Conclusão

A abordagem conservadora forneceu dois finalistas e confirmou que alterações
locais pequenas eram mais fiáveis do que reescrever todo o prompt.
