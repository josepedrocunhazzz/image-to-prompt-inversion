# Ronda 3 - Visual Anchors

## Objetivo

Reutilizar os melhores renders anteriores como referências visuais e gerar
variações locais de blocos cujo efeito já tinha sido observado.

## Conteúdo

- `codigo/src/gerar_ronda_03_visual_anchors.py`: gera prompts calibrados.
- `codigo/src/tp2_*.py` e `search_*.py`: avaliação e seleção.
- `codigo/tests/test_ronda_03.py`: teste do gerador.
- `notebook/TP2_RunAll_Ronda_03.ipynb`: reprodução da ronda.
- `resultados/metrics*.csv` e `top5*.csv`: métricas e ranking.
- `resultados/contact_sheet_top5.jpg`: melhores candidatos.
- `resultados/ronda_03_resumo_visual.png`: comparação compacta.

## Leitura dos resultados

O ranking deve ser lido em conjunto com o resumo visual, porque esta ronda
avaliou sobretudo se pequenas alterações preservavam uma direção já promissora.

## Conclusão

Foi a melhoria qualitativa inicial mais clara e estabeleceu famílias de prompts
estáveis para os targets visualmente mais simples.
