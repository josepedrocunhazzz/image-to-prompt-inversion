# Ronda 7 - Long Design of Experiments

## Objetivo

Aplicar um desenho fatorial com múltiplos fatores e níveis, amostrando centenas
ou milhares de combinações de blocos.

## Conteúdo

- `codigo/src/gerar_ronda_07_long_doe.py`: constrói a amostra fatorial.
- `codigo/src/tp2_*.py` e `search_*.py`: renderização e avaliação.
- `codigo/tests/test_ronda_07.py`: validação da geração.
- `notebook/TP2_RunAll_Ronda_07.ipynb`: execução completa.
- `resultados/metrics*.csv`: medições da experiência.
- `resultados/top5*.csv` e `contact_sheet_top5.jpg`: candidatos retidos.
- `resultados/ronda_07_resumo_visual.png`: síntese visual.

## Leitura dos resultados

Esta ronda deve ser analisada como estudo de interação entre blocos, e não como
otimização independente de cada palavra.

## Conclusão

As interações observadas justificaram bancos de prompts e pesos de métricas
específicos por target.
