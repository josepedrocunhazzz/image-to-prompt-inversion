# Ronda 19 - Seed Sweep

## Objetivo

Renderizar os melhores prompts em 64 seeds por target para medir sensibilidade
ao espaço latente e identificar famílias robustas.

## Conteúdo

- `codigo/src/gerar_ronda_19.py`: prepara os prompts do sweep.
- `codigo/src/search_seed_sweep.py`: executa a variação de seeds.
- `codigo/src/evaluate_candidates.py`: calcula as métricas.
- `notebook/TP2_RunAll_Ronda_19.ipynb`: execução da experiência.
- `prompts/prompts_ronda_19.json`: prompts analisados.
- `resultados/20260603-182138_round42_seed_sweep_metric64/`: métricas por target,
  resumo e top do sweep.

## Interpretação

Esta ronda é diagnóstica. Seeds alternativas mostram o potencial de uma família
de prompts, mas não substituem a avaliação com a seed oficial do filename.

## Conclusão

O sweep confirmou sensibilidade elevada à seed e orientou as microvariações das
rondas seguintes; não forneceu diretamente imagens submetidas.
