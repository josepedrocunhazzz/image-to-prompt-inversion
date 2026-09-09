# Ronda 14 - Massive Variation Generation

## Objetivo

Decompor os melhores prompts históricos em seis blocos, amostrar 1 000
combinações em inglês por target e comparar com 200 prompts em chinês.

## Conteúdo

- `codigo/datasets/gerar_datasets_ronda_14.py`: gera os datasets.
- `codigo/datasets/ingles/`: bancos em inglês/romanizados por target.
- `codigo/datasets/chines/`: bancos alternativos em chinês.
- `codigo/datasets/manifest.json`: descrição do conjunto gerado.
- `codigo/datasets/executar_ronda_14_top20*.ipynb`: execução local e Colab.
- `resultados/*_metrics_all.csv`: métricas completas por target e variante.
- `resultados/*_top20_metrics.json`: top-20 estruturado.
- `resultados/ronda_14_final_ingles_top3.csv`: seleção inglesa consolidada.
- `resultados/ronda_14_ingles_vs_chines_top1.csv`: comparação entre famílias.
- `resultados/ronda_14_ingles_top3_contact_sheet.png`: inspeção dos top-3.
- `resultados/ronda_14_runs_summary.csv`: resumo das execuções.

## Conclusão

A pesquisa ampla em inglês produziu o melhor perfil global e forneceu vários
finalistas. Os prompts chineses foram consistentemente dominados.
