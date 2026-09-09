# Ronda 20 - Fixed-Seed Micro

## Objetivo

Transferir as melhores famílias descobertas para o regime válido de entrega:
prompt textual, modelo fixo e seed oficial, alterando um atributo de cada vez.

## Conteúdo

- `codigo/src/gerar_ronda_20.py`: gera microvariações fixed-seed.
- `codigo/src/search_seed_sweep.py`: runner reutilizado com offset zero.
- `codigo/src/evaluate_candidates.py`: métricas e ranking.
- `notebook/TP2_RunAll_Ronda_20.ipynb`: execução integral.
- `prompts/prompts_ronda_20.json`: banco de microvariações.
- `prompts/melhores_seeds_metricas_ronda_20.json`: informação do diagnóstico anterior.
- `resultados/20260603-210759_round43_fixed_seed_micro/`: métricas por target.
- `resultados/finalistas/1159_25/`: rank 1 do sumo.
- `resultados/finalistas/7836/`: rank 2 do astronauta.

## Conclusão

A ronda produziu dois finalistas através de correções locais de opacidade,
reflexo e distribuição da nebulosa.
