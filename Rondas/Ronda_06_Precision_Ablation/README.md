# Ronda 6 - Precision Ablation

## Objetivo

Remover termos individuais e pares de termos dos melhores prompts para distinguir
componentes essenciais, neutros e prejudiciais.

## Conteúdo

- `codigo/src/gerar_ronda_06_precision_ablation.py`: cria as ablações.
- `codigo/src/tp2_*.py` e `search_*.py`: pipeline de avaliação.
- `codigo/tests/test_ronda_06.py`: teste do gerador.
- `notebook/TP2_RunAll_Ronda_06.ipynb`: execução reproduzível.
- `resultados/metrics*.csv`: efeito quantitativo das remoções.
- `resultados/top5*.csv` e `contact_sheet_top5.jpg`: melhores variantes.
- `resultados/ronda_06_resumo_visual.png`: comparação target/render.

## Leitura dos resultados

As diferenças entre variantes devem ser interpretadas como efeito dos termos
removidos, mantendo a restante estrutura do prompt tão estável quanto possível.

## Conclusão

A ablação tornou os prompts mais curtos, interpretáveis e controláveis.
