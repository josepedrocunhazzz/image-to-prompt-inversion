# Ronda 23 - Palm Minimal Ladder

## Objetivo

Começar com uma descrição mínima da palmeira e acrescentar detalhes
progressivamente para medir quando o prompt começava a introduzir elementos
visuais indesejados.

## Conteúdo

- `codigo/src/gerar_ronda_23.py`: gera a sequência minimal-to-detailed.
- `codigo/src/search_seed_sweep.py`: renderização na seed oficial.
- `codigo/src/evaluate_candidates.py`: métricas da ladder.
- `notebook/TP2_RunAll_Ronda_23.ipynb`: execução completa.
- `prompts/prompts_ronda_23.json`: níveis de detalhe testados.
- `resultados/20260604-011758_round46_palm_minimal_ladder/`: métricas,
  ranking e resumo da experiência.

## Leitura dos resultados

As linhas devem ser comparadas pela quantidade de detalhe adicionada, observando
em especial ondas, ilhas, posição do tronco e reflexo do sol.

## Conclusão

Prompts curtos e controlados foram mais estáveis; acrescentar detalhes de praia
nem sempre aproximou o render do target.
