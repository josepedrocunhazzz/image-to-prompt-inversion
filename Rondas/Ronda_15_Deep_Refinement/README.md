# Ronda 15 - Targeted Deep Refinement

## Objetivo

Concentrar a pesquisa nos targets `1159_7` e `9338`. Foram amostrados 10 000
prompts por target num espaço de oito blocos e adicionada uma reparação dirigida
para reduzir drift de `9338` para dragão/asa.

## Conteúdo

- `codigo/datasets/gerar_datasets_ronda_15.py`: gera o espaço de pesquisa profundo.
- `codigo/datasets/pt/`: datasets para cubo-ouriço e criatura fantástica.
- `codigo/datasets/executar_ronda_15_top20*.ipynb`: execução local e Colab.
- `codigo/src/gerar_ronda_15_targeted_repair.py`: banco de reparação dirigida.
- `codigo/src/search_*.py`: pesquisa top-k, multiseed e seed sweep.
- `notebook/TP2_RunAll_Ronda_15_Targeted_Repair.ipynb`: execução da reparação.
- `prompts/prompts_ronda_15_targeted_repair.json`: prompts preservados.
- `RESULTADOS_RONDA_15_*.md`: análise detalhada por target.
- `RONDA_15_GERACAO_CLASSES_PIORES.md`: descrição da geração massiva.
- `resultados/ronda_15_*top3.png`: candidatos visuais retidos.
- `resultados/targeted_repair/`: métricas compactas da reparação adicional.

## Conclusão

A ronda forneceu os três finalistas do cubo-ouriço e melhorou os atributos
estruturais dos dois targets mais difíceis.
