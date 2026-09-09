# Ronda 2 - PEZ Evolution

## Objetivo

Explorar os targets `1159_7` e `9338` através de mutações de blocos semânticos e
otimização discreta de tokens inspirada em PEZ.

## Conteúdo

- `codigo/src/gerar_ronda_02_pez_evolution.py`: constrói o banco evolutivo.
- `codigo/src/tp2_*.py` e `search_*.py`: pipeline reutilizável.
- `codigo/tests/test_ronda_02.py`: teste estrutural do banco.
- `notebook/TP2_RunAll_Ronda_02.ipynb`: execução Run All.
- `resultados/metrics*.csv`: medições dos candidatos.
- `resultados/top5*.csv`: melhores resultados da pesquisa.
- `resultados/contact_sheet_top5.jpg`: comparação visual.
- `resultados/ronda_02_resumo_visual.png`: resumo target/render.

## Leitura dos resultados

Os CSV permitem relacionar cada candidato com o respetivo score; a contact sheet
é necessária para verificar se o objeto gerado mantém a geometria do target.

## Conclusão

Foram encontrados termos úteis, como `cubical wooden block` e `rainbow quills`,
mas a aparência dos targets complexos continuou instável.
