# Ronda 13 - VLM Refinement with Codex

## Objetivo

Testar refinamento iterativo assistido por VLM nos targets de sumo, palmeira e
guerreiro. Em cada iteração, o target e o render eram comparados antes da
proposta de um novo prompt.

## Conteúdo

- `codigo/src/executar_ronda_13_codex_vlm.py`: entrada principal da experiência.
- `codigo/src/codex_vlm_schedules.py`: sequências de refinamento.
- `codigo/vlm_refinement/run_ronda_13.py`: runner VLM.
- `codigo/vlm_refinement/config/ronda_13_config.json`: configuração da ronda.
- `codigo/vlm_refinement/README.md`: documentação técnica detalhada do runner.
- `resultados/ronda_13_resumo_metricas.csv`: comparação quantitativa das iterações.
- `resultados/ronda_13_resumo_visual.png`: comparação target/render.
- `resultados/CURRENT_RUN.txt`: identificação do conjunto resumido.
- `resultados/README.md`: notas específicas dos resultados VLM.

## Leitura dos resultados

O resumo de métricas deve ser confrontado com o resumo visual para verificar se
uma melhoria numérica corresponde a uma correção efetiva do objeto ou layout.

## Conclusão

Nenhuma proposta superou o anchor inicial. A experiência mostrou que o espaço
local de prompts é pouco suave para este gerador.
