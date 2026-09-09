# VLM Refinement

Pasta da ronda 13. A ideia e usar o Codex como VLM: comparar a target com a ultima imagem gerada, melhorar o prompt, gerar outra imagem, medir, e repetir.

## O Que Interessa

```text
vlm_refinement/
  README.md
  run_ronda_13.py
  config/
    ronda_13_config.json
  prompts/
    codex_vlm_schedules.py
  tools/
    friendly_view.py
```

As runs ficam fora desta pasta, em:

```text
TP2-students/students/outputs/vlm_refinement/
  CURRENT_RUN.txt
  current -> runs/<ultima_run>
  runs/
    <timestamp>_ronda_13_codex_<mode>/
      RUN_README.md
      review/
      ...ficheiros brutos da pipeline...
```

Para analisar resultados, abre primeiro `RUN_README.md` e depois `review/`.

## Modo Interativo

Este e o fluxo que querias: tu corres o comando, o script para quando precisa de mim, eu comparo as imagens e respondo ao processo.

```bash
.venv/bin/python vlm_refinement/run_ronda_13.py \
  --mode interactive \
  --offline \
  --render-device mps \
  --metric-device mps \
  --only 1159_25.png
```

Quando aparecer `CODEX_VLM_REQUEST`, eu leio:

```text
target_image=...
current_image=...
request_json=...
```

Depois eu devolvo o JSON diretamente ao processo. Tu nao tens de colar nada se eu estiver a conduzir a execucao.

## Modo File

Este modo tambem evita colar JSON no terminal. O runner espera por `codex_response.json` em cada pasta de iteracao.

```bash
.venv/bin/python vlm_refinement/run_ronda_13.py \
  --mode file \
  --offline \
  --render-device mps \
  --metric-device mps \
  --only 1159_25.png
```

## Modo Automatico

Usa os 20 prompts por categoria definidos em `prompts/codex_vlm_schedules.py`.

```bash
.venv/bin/python vlm_refinement/run_ronda_13.py \
  --mode schedule \
  --offline \
  --render-device mps \
  --metric-device mps
```

## Vista Limpa Da Run

No fim, cada run cria automaticamente:

```text
review/
  1159_25/
    target.png
    initial.png
    best.png
    initial_prompt.txt
    final_prompt.txt
    initial_metrics.json
    final_metrics.json
    trace.md
    iterations/
      01/
        previous.png
        generated.png
        winner.png
        prompt.txt
        reason.txt
        analysis.json
        metrics.json
        decision.txt
```

Os ficheiros brutos continuam presentes porque sao uteis para reproduzir e auditar, mas a pasta `review/` e a vista humana.

## Nota MPS

No teste, MPS so ficou disponivel quando a execucao foi autorizada fora do sandbox das ferramentas. A run correta mostra:

```text
Renderer device: mps
Metric device: mps
```

