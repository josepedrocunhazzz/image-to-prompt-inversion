# Ronda 5 - Micro Visual Metrics

## Objetivo

Melhorar a seleção automática através de métricas de cor, bordas Sobel, layout e
regiões específicas, complementando CLIP, LPIPS, RMSE e SSIM.

## Conteúdo

- `codigo/src/gerar_ronda_05_micro_visual_metrics.py`: gera microvariações.
- `codigo/src/tp2_metrics.py`: métricas gerais e visuais auxiliares.
- `codigo/src/search_*.py`: avaliação e retenção dos candidatos.
- `codigo/tests/test_ronda_05.py`: teste estrutural.
- `notebook/TP2_RunAll_Ronda_05.ipynb`: execução da ronda.
- `resultados/metrics*.csv`: métricas por candidato.
- `resultados/top5*.csv` e `contact_sheet_top5.jpg`: ranking e inspeção visual.
- `resultados/ronda_05_resumo_visual.png`: resumo da ronda.

## Conclusão

A principal melhoria ocorreu no ranking: foram rejeitados candidatos
semanticamente plausíveis, mas com cor, estrutura ou ocupação espacial erradas.
