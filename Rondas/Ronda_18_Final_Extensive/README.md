# Ronda 18 - Final Extensive

## Objetivo

Executar uma pesquisa extensiva nos seis targets, com 4 900 prompts e validação
dos candidatos selecionados em cinco seeds auxiliares.

## Conteúdo

- `codigo/src/gerar_ronda_18.py`: gera o banco final extensivo.
- `codigo/src/search_multiseed_validate.py`: pesquisa em duas fases.
- `codigo/src/search_seed_sweep.py`: ferramentas de robustez.
- `codigo/src/evaluate_candidates.py`: métricas e scores.
- `notebook/TP2_RunAll_Ronda_18.ipynb`: execução completa.
- `prompts/prompts_ronda_18.json`: banco da ronda.
- `resultados/20260603-021040_round41_final_extensive/`: métricas por target,
  candidatos selecionados e ranking consolidado.
- `resultados/finalistas/1159_3/`: ranks 1 e 3 do guerreiro.
- `resultados/finalistas/7836/`: rank 3 do astronauta.

## Conclusão

A pesquisa ampla forneceu três imagens mantidas na seleção final e mostrou a
utilidade de combinar escala de pesquisa com validação de robustez.
