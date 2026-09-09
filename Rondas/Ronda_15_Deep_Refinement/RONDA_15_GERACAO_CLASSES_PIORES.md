# Ronda_15 - Geracao das Classes Piores

## Objetivo

Esta ronda foi criada para focar a geracao em massa apenas nas classes que estavam a precisar de mais refinamento depois da ronda anterior. Em vez de voltar a gerar prompts para todos os alvos, a Ronda_15 concentra o esforco em dois targets especificos:

- `1159_7`: o animal/cubo, visualmente um pequeno hedgehog/hamster com corpo cubico de madeira, pelos/espinhos no topo e cara parcialmente escondida.
- `9338`: o animal colorido com aspeto de hamster/dragao, com escamas/pontos luminosos tipo LED, barriga azul-esverdeada, cara laranja e fundo painterly multicolor.

A pasta desta ronda esta em:

```text
TP2-students/students/outputs/ronda_15_gerracaoclasses_piores
```

## O que existia na Ronda 14

Na Ronda 14, a pasta `ronda_14_geracaoemmassa_top5prompts` foi usada para gerar datasets de prompts a partir dos melhores prompts ja encontrados em rondas anteriores. O script `datasets/generate_datasets.py` lia o ficheiro:

```text
TP2-students/students/outputs/best_of_runs/best_of_runs.csv
```

Depois agrupava as linhas por `target_name`, ordenava cada grupo por `cross_run_score`, retirava os melhores prompts e usava essa informacao como base para construir variacoes.

Na Ronda 14, a geracao era mais geral:

- incluia 6 categorias: `1159_25`, `1159_29`, `1159_3`, `1159_7`, `7836`, `9338`;
- gerava `1000` prompts em portugues por categoria;
- gerava tambem `200` prompts em chines por categoria;
- cada dataset PT tinha 6 blocos de variacao com 6 opcoes cada;
- o espaco teorico de variacao PT era `46656` combinacoes por categoria;
- as combinacoes eram ordenadas por distancia aos blocos-base, para testar primeiro prompts mais proximos dos melhores prompts conhecidos.

A Ronda 14 tambem tinha notebooks de avaliacao em massa que renderizavam cada prompt, calculavam metricas e guardavam um top-20 por categoria.

## O que mudou na Ronda_15

Na Ronda_15 a logica de base foi mantida, mas o foco mudou. Em vez de explorar todas as classes, esta ronda e uma geracao concentrada para melhorar apenas os dois casos mais problematicos.

As principais alteracoes foram:

- o dataset ficou limitado a `1159_7` e `9338`;
- foram gerados `10000` prompts por categoria, em vez de `1000`;
- nao foi criado dataset em chines nesta ronda;
- cada alvo passou a ter 8 blocos de variacao mais especificos;
- cada bloco passou a ter 7 opcoes;
- o espaco teorico de variacao passou para `5764801` combinacoes por categoria;
- a selecao dos prompts continua ordenada por proximidade ao bloco-base, mas agora usa `heapq.nsmallest` para escolher os `10000` melhores sem ordenar todos os milhoes de combinacoes em memoria;
- os prompts foram compactados para respeitar o limite do text encoder CLIP, que so aceita ate `77` tokens;
- cada prompt guarda `clip_token_count`, permitindo confirmar que nao ha truncagem antes da avaliacao;
- os notebooks `run_mass_generation_top20.ipynb` e `run_mass_generation_top20_colab.ipynb` foram copiados e adaptados para apontar para a pasta da Ronda_15 e correr apenas `pt/1159_7` e `pt/9338`.

## Como os prompts sao gerados

O script principal desta ronda e:

```text
TP2-students/students/outputs/ronda_15_gerracaoclasses_piores/datasets/generate_datasets.py
```

O script continua a ler o `best_of_runs.csv` para recuperar metadata dos melhores prompts anteriores. Esses prompts ficam guardados em `top5_seed_prompts` dentro de cada JSON, para manter o historico e a ligacao com as rondas anteriores.

No entanto, tal como acontecia no dataset PT da Ronda 14, os prompts finais nao sao simplesmente os prompts antigos com texto colado. Eles sao criados a partir de blocos semanticos novos, escritos para descrever partes visuais importantes do target.

Cada bloco representa uma dimensao visual. O script faz o produto cartesiano das opcoes dos blocos, calcula a distancia de cada combinacao aos indices-base e escolhe as combinacoes mais proximas. Em termos praticos:

1. cada bloco tem uma opcao `base`, normalmente a opcao de indice `0`;
2. uma combinacao como `[0, 0, 0, 0, 0, 0, 0, 0]` e a mais proxima do prompt-base;
3. combinacoes com pequenas mudancas, como `[0, 0, 1, 0, 0, 0, 0, 0]`, aparecem cedo;
4. combinacoes cada vez mais afastadas aparecem depois;
5. o script guarda os primeiros `10000` prompts unicos.

Cada entrada no JSON final tem esta estrutura:

```json
{
  "id": "00001",
  "seed_index": 1,
  "combo": [0, 0, 0, 0, 0, 0, 0, 0],
  "prompt": "..."
}
```

## Prompt design para `1159_7`

O alvo `1159_7` e muito especifico: nao basta dizer "small hedgehog" ou "cube body". A imagem tem varios detalhes que precisam de aparecer ao mesmo tempo: corpo em cubo, madeira clara, blocos/tiles nas laterais, cara pequena escondida, espinhos longos no topo e fundo castanho de estudio.

Por isso foram criados 8 blocos:

- `subject`: define o animal como hedgehog/hamster pequeno integrado num corpo cubico.
- `cube_structure`: forca a ideia de cubo com lados em madeira clara, tiles quadrados, grelha e estrutura modular.
- `face`: descreve olhos pequenos, nariz e cara parcialmente escondida pelos pelos/espinhos.
- `quills`: reforca os espinhos longos, ambar/laranja, a crescer a partir do topo.
- `top_surface`: tenta preservar o plano superior do cubo visivel em volta da cabeca.
- `material`: especifica balsa wood, madeira palida, textura fibrosa e arestas suaves.
- `lighting`: aproxima o fundo castanho e a fotografia de estudio quente.
- `composition`: fixa o enquadramento quadrado, macro, centrado e em tres-quartos.

Exemplo do primeiro prompt gerado:

```text
small hedgehog in wooden cube, peach beige square tile sides, tiny hidden face front top, long amber top spikes, flat pale top rim visible, soft balsa wood grain, warm brown studio background, centered square three quarter view
```

## Prompt design para `9338`

O alvo `9338` tambem precisava de prompts mais dirigidos. A imagem tem uma criatura que parece hamster/dragao, mas o aspeto importante nao e apenas o animal: sao os pontos brilhantes tipo escamas/LEDs, a barriga teal, a cara laranja, os pequenos chifres/espinhos, a pose lateral e o fundo painterly com arcos de cor.

Foram criados 8 blocos:

- `subject`: define a criatura como dragon hamster/fantasy hamster em pose de retrato.
- `head`: reforca o focinho laranja, olho preto brilhante e bigodes.
- `belly`: fixa a barriga creme com zona teal/azul-esverdeada.
- `led_scales`: adiciona escamas/pontos luminosos, bead scales, jewel-like dots e aspeto de LEDs.
- `spines`: descreve chifre, orelha, espinhos coloridos, cauda e ridges de dragao.
- `paws`: tenta preservar as patas pequenas junto a barriga.
- `background`: aproxima o fundo escuro, painterly, com arcos amarelos/verdes e rastos de cor.
- `style`: mantem o estilo de ilustracao fantastica, pintura digital suave e retrato quadrado.

Exemplo do primeiro prompt gerado:

```text
rainbow dragon hamster profile, orange snout glossy black eye, cream chest teal oval belly, tiny LED bead scales, pink horn blue magenta spines, small clawed forepaws, dark background yellow green arcs, painterly fantasy square portrait
```

## Outputs gerados

Os ficheiros principais gerados pela Ronda_15 sao:

```text
datasets/generate_datasets.py
datasets/manifest.json
datasets/pt/manifest.json
datasets/pt/1159_7.json
datasets/pt/9338.json
datasets/run_mass_generation_top20.ipynb
datasets/run_mass_generation_top20_colab.ipynb
```

O manifest PT confirma:

```text
1159_7 -> 10000 prompts, variation_space 5764801, max_clip_tokens 52
9338   -> 10000 prompts, variation_space 5764801, max_clip_tokens 55
```

## Como correr a avaliacao

Os notebooks mantem o setup da ronda anterior:

- carregam `LCMConfig` e `EvalConfig`;
- usam `load_lcm_pipeline`;
- renderizam com a seed derivada do nome do target;
- calculam CLIP, LPIPS, RMSE, SSIM, metricas visuais especificas e score ponderado;
- escrevem `metrics_all.csv`;
- guardam as melhores imagens em `top20`;
- escrevem `top20_metrics.json` e `summary.json`.

A celula final dos notebooks corre apenas:

```python
RUNS_TO_EXECUTE = [
    ("pt", "1159_7"),
    ("pt", "9338"),
]

for language, category in RUNS_TO_EXECUTE:
    run_category(language=language, category=category, prompt_limit=PROMPT_LIMIT, top_k=TOP_K)
```

Isto significa que a geracao em massa da Ronda_15 fica alinhada com o setup que ja estava tratado na Ronda 14, mas evita gastar tempo nas classes que nao fazem parte deste foco.

## Resumo

A Ronda_15 nao e uma ronda totalmente nova em termos de pipeline. Ela reutiliza a estrutura da Ronda 14, mas muda a estrategia de exploracao:

- menos classes;
- muito mais prompts por classe;
- prompts mais descritivos e especificos ao target;
- maior espaco de variacao;
- selecao eficiente dos melhores combos sem ordenar tudo em memoria;
- notebooks copiados e reduzidos para correr so os dois alvos pretendidos.

O objetivo e aumentar a probabilidade de encontrar imagens mais proximas dos targets `1159_7` e `9338`, sobretudo nos detalhes que a geracao anterior tendia a perder: a geometria real do cubo em `1159_7` e o aspeto luminoso/multicolor das escamas em `9338`.
