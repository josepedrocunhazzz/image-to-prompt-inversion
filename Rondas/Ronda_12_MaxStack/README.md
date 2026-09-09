# Ronda 12 - MaxStack

## Objetivo

Combinar métricas globais, regionais e heurísticas por target com ablações e
permutações da ordem dos termos.

## Conteúdo

- `codigo/src/gerar_ronda_12_maxstack.py`: gera o banco MaxStack.
- `codigo/src/tp2_metrics.py`: scores globais e específicos.
- `codigo/src/search_multiseed_validate.py`: pesquisa e validação.
- `codigo/tests/test_ronda_12.py`: teste do banco.
- `notebook/TP2_RunAll_Ronda_12.ipynb`: execução integral.
- `prompts_ronda_12_maxstack.json`: banco de prompts preservado.
- `resultados/*_stage1_fixed_seed_top30.csv`: top inicial por target.
- `resultados/*_selected_for_multiseed.csv`: candidatos enviados para validação.
- `resultados/ronda_12_resumo_visual.png`: síntese visual disponível.

## Conclusão

MaxStack foi a fase de diagnóstico local mais completa para `1159_7` e `9338`,
sobretudo na deteção de atributos ausentes em regiões específicas.
