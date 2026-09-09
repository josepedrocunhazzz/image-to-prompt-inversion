# Ronda 1 - CLIP-Guided Hard Prompt Search

## Objetivo

Criar o primeiro banco de prompts para os seis targets. A ronda partiu de
anchors manuais e expandiu blocos de sujeito, fundo, estilo e composição através
de pesquisa guiada por CLIP.

## Conteúdo

- `codigo/src/gerar_ronda_01_clip_guided.py`: gera os candidatos desta ronda.
- `codigo/src/tp2_*.py`: configuração, métricas e utilitários partilhados.
- `codigo/src/search_*.py`: renderização e seleção top-k/multiseed.
- `codigo/tests/test_ronda_01.py`: valida a estrutura do gerador.
- `notebook/TP2_RunAll_Ronda_01.ipynb`: execução integral da experiência.
- `resultados/metrics*.csv`: métricas completas e parciais.
- `resultados/top5*.csv`: candidatos melhor classificados.
- `resultados/contact_sheet_top5.jpg`: inspeção visual dos melhores resultados.
- `resultados/ronda_01_resumo_visual.png`: comparação compacta target/render.

## Leitura dos resultados

O `summary.json` descreve a execução; os CSV preservam valores quantitativos e
a contact sheet permite detetar falsos positivos que CLIP classificou bem.

## Conclusão

A ronda criou um banco inicial utilizável, mas mostrou que similaridade
semântica isolada não garante fidelidade visual.
