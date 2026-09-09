# Resultados Ronda_15 - 1159_7

## Contexto

Este documento resume os resultados da run:

```text
TP2-students/students/outputs/ronda_15_gerracaoclasses_piores/runs_from_dataset/20260603-092124_pt_1159_7
```

Nesta execucao foram avaliados:

- `10000` prompts para a categoria `1159_7`
- `top_k = 20`
- `render_device = cuda`
- `metric_device = cuda`

O objetivo desta analise e responder a tres perguntas:

1. como ficou o top 20 da run atual;
2. se houve melhoria face a Ronda 14 para `1159_7`;
3. que conclusoes podem entrar no relatorio desta run e da estrategia global da Ronda_15.

## Resumo Executivo

O resultado principal e positivo: a Ronda_15 melhorou o melhor resultado e tambem melhorou a qualidade media do top 20 para `1159_7`.

Melhor score:

- Ronda 14 best selection score: `0.9546455018460696`
- Ronda_15 best selection score: `0.98340812840169`
- melhoria absoluta: `+0.0287626265556204`

Media do top 20:

- Ronda 14 media `selection_score`: `0.892149946928665`
- Ronda_15 media `selection_score`: `0.9049833227200935`
- melhoria absoluta: `+0.0128333757914285`

Em termos praticos, a Ronda_15 produziu um top 20 visualmente mais forte na maioria das metricas importantes de fidelidade estrutural e perceptual, embora tenha descido em algumas metricas mais heuristicas.

## Melhor Prompt Encontrado

Melhor prompt da Ronda_15 para `1159_7`:

```text
small hedgehog in wooden cube, peach beige square tile sides, muzzle peeking through bristles, tall orange radial quills, square wooden top plane, soft balsa wood grain, warm brown studio background, centered realistic square photo
```

Principais metricas do melhor resultado:

- `selection_score`: `0.98340812840169`
- `combined_score`: `0.95340812840169`
- `clip_iisim`: `0.7930729389190674`
- `lpips_alex`: `0.3118388056755066`
- `pixel_rmse_01`: `0.07226004127890961`
- `pixel_ssim_01`: `0.8715078363258614`
- `color_hist_sim`: `0.8030124240451388`
- `edge_sim`: `0.9333440447604584`
- `layout_sim`: `0.9897301229614253`
- `visual_specific_score`: `0.885972031078758`
- `region_score`: `0.828005016586915`
- `heuristic_score`: `0.6550654089481847`

## Top 20 Detalhado

### Tabela Resumida

| Rank | ID | Selection | Combined | CLIP | LPIPS | RMSE | SSIM | Color | Edge | Layout | Visual | Region | Pareto |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 07504 | 0.9834 | 0.9534 | 0.7931 | 0.3118 | 0.0723 | 0.8715 | 0.8030 | 0.9333 | 0.9897 | 0.8860 | 0.8280 | True |
| 2 | 07501 | 0.9491 | 0.9191 | 0.8468 | 0.3488 | 0.0733 | 0.8620 | 0.7640 | 0.9318 | 0.9903 | 0.8680 | 0.8217 | True |
| 3 | 05145 | 0.9433 | 0.9133 | 0.8023 | 0.3348 | 0.0863 | 0.8462 | 0.7621 | 0.9360 | 0.9873 | 0.8680 | 0.8036 | True |
| 4 | 01722 | 0.9197 | 0.8897 | 0.8251 | 0.3697 | 0.0748 | 0.8659 | 0.7880 | 0.9288 | 0.9937 | 0.8784 | 0.8286 | True |
| 5 | 07523 | 0.9163 | 0.9163 | 0.7923 | 0.3461 | 0.0761 | 0.8681 | 0.7705 | 0.9373 | 0.9845 | 0.8717 | 0.8138 | False |
| 6 | 01720 | 0.9096 | 0.9096 | 0.8299 | 0.3557 | 0.0779 | 0.8560 | 0.7818 | 0.9341 | 0.9862 | 0.8760 | 0.8144 | False |
| 7 | 07520 | 0.9090 | 0.9090 | 0.8055 | 0.3545 | 0.0769 | 0.8548 | 0.7967 | 0.9350 | 0.9841 | 0.8826 | 0.8211 | False |
| 8 | 07511 | 0.9083 | 0.8783 | 0.8102 | 0.3754 | 0.0779 | 0.8672 | 0.7527 | 0.9324 | 0.9933 | 0.8637 | 0.8071 | True |
| 9 | 03700 | 0.9044 | 0.9044 | 0.7556 | 0.3333 | 0.0800 | 0.8324 | 0.8018 | 0.9338 | 0.9777 | 0.8832 | 0.8204 | False |
| 10 | 09170 | 0.8949 | 0.8949 | 0.7962 | 0.3647 | 0.0773 | 0.8460 | 0.7863 | 0.9356 | 0.9871 | 0.8787 | 0.8290 | False |
| 11 | 03704 | 0.8948 | 0.8948 | 0.7781 | 0.3522 | 0.0767 | 0.8299 | 0.7832 | 0.9357 | 0.9737 | 0.8747 | 0.8288 | False |
| 12 | 03713 | 0.8945 | 0.8945 | 0.8088 | 0.3560 | 0.0769 | 0.8578 | 0.7507 | 0.9319 | 0.9918 | 0.8623 | 0.8112 | False |
| 13 | 07522 | 0.8912 | 0.8912 | 0.7817 | 0.3490 | 0.0783 | 0.8529 | 0.7263 | 0.9346 | 0.9869 | 0.8513 | 0.8327 | False |
| 14 | 03719 | 0.8879 | 0.8879 | 0.7898 | 0.3633 | 0.0770 | 0.8604 | 0.7610 | 0.9349 | 0.9822 | 0.8661 | 0.8019 | False |
| 15 | 07508 | 0.8866 | 0.8866 | 0.8152 | 0.3671 | 0.0749 | 0.8594 | 0.7746 | 0.9289 | 0.9962 | 0.8729 | 0.8238 | False |
| 16 | 02436 | 0.8839 | 0.8839 | 0.8053 | 0.3658 | 0.0823 | 0.8607 | 0.7433 | 0.9351 | 0.9882 | 0.8594 | 0.8144 | False |
| 17 | 03710 | 0.8826 | 0.8826 | 0.7975 | 0.3511 | 0.0803 | 0.8518 | 0.7636 | 0.9273 | 0.9915 | 0.8665 | 0.8088 | False |
| 18 | 07494 | 0.8820 | 0.8820 | 0.8108 | 0.3621 | 0.0778 | 0.8147 | 0.7744 | 0.9311 | 0.9841 | 0.8712 | 0.8380 | False |
| 19 | 02124 | 0.8816 | 0.8816 | 0.7395 | 0.3410 | 0.0940 | 0.8135 | 0.7764 | 0.9386 | 0.9773 | 0.8734 | 0.8236 | False |
| 20 | 00740 | 0.8765 | 0.8765 | 0.8025 | 0.3668 | 0.0778 | 0.8602 | 0.7526 | 0.9298 | 0.9919 | 0.8625 | 0.8202 | False |

### Leitura do Top 20

Observacoes principais:

- O top 4 esta claramente acima do resto em `selection_score`, com uma quebra mais visivel depois do rank 4.
- O melhor resultado absoluto (`rank 1`) nao e o melhor em `clip_iisim`, mas ganha muito em fidelidade perceptual e pixel-level, sobretudo `LPIPS`, `RMSE` e `SSIM`.
- Os prompts que mais se repetem no top 20 tendem a convergir para a mesma familia descritiva:
  - `small hedgehog in wooden cube`
  - `peach beige square tile sides`
  - `muzzle peeking through bristles`
  - `tall orange radial quills`
  - `warm brown studio background`
- A principal variacao entre os melhores resultados acontece em:
  - `top surface`: `square wooden top plane`, `flat pale top rim visible`, `clean square top edges`, `visible timber top face`
  - `material`: `soft balsa wood grain`, `matte pale timber texture`, `fibrous wooden block texture`
  - `composition`: `centered realistic square photo`, `tight square crop`, `centered square three quarter view`

## Estatisticas Agregadas do Top 20

### Ronda_15 - Top 20

- media `selection_score`: `0.9049833227200935`
- mediana `selection_score`: `0.894887047138553`
- minimo `selection_score`: `0.87649410900161`
- maximo `selection_score`: `0.98340812840169`
- media `combined_score`: `0.8974833227200935`
- media `clip_iisim`: `0.7992938101291657`
- media `lpips_alex`: `0.35346889197826387`
- media `pixel_rmse_01`: `0.07843767331814479`
- media `pixel_ssim_01`: `0.8515706310947111`
- media `color_hist_sim`: `0.7706527427390769`
- media `edge_sim`: `0.933313252629451`
- media `layout_sim`: `0.9868957708104751`
- media `visual_specific_score`: `0.8708325268149875`
- media `region_score`: `0.8195584358419716`
- media `heuristic_score`: `0.6838414537735071`
- numero de entradas `pareto`: `5` em `20`

Interpretacao:

- o top 20 esta relativamente compacto, com scores todos acima de `0.876`;
- a run tem boa consistencia estrutural: `layout_sim` medio muito alto (`0.9869`);
- a fidelidade perceptual tambem esta forte: `LPIPS` medio relativamente baixo e `SSIM` medio alto;
- ha menos diversidade pareto do que na Ronda 14, o que sugere uma exploracao mais concentrada numa familia de prompts vencedora.

## Comparacao com a Ronda 14

Referencia usada:

```text
TP2-students/students/outputs/ronda_14_.../runs_from_dataset/20260531-172613_pt_1159_7
```

### Melhor Resultado

Melhor Ronda 14:

- `selection_score`: `0.9546455018460696`
- `combined_score`: `0.9246455018460695`
- `clip_iisim`: `0.8268659710884094`
- `lpips_alex`: `0.34956350922584534`
- `pixel_rmse_01`: `0.08370593121876724`
- `pixel_ssim_01`: `0.8253483201417292`
- `color_hist_sim`: `0.7759280734592013`
- `layout_sim`: `0.9809516539880089`
- `region_score`: `0.841001820286125`
- `heuristic_score`: `0.8535297284039158`

Melhor Ronda_15:

- `selection_score`: `0.98340812840169`
- `combined_score`: `0.95340812840169`
- `clip_iisim`: `0.7930729389190674`
- `lpips_alex`: `0.3118388056755066`
- `pixel_rmse_01`: `0.07226004127890961`
- `pixel_ssim_01`: `0.8715078363258614`
- `color_hist_sim`: `0.8030124240451388`
- `layout_sim`: `0.9897301229614253`
- `region_score`: `0.828005016586915`
- `heuristic_score`: `0.6550654089481847`

Leitura:

- a Ronda_15 melhora claramente o score final e a fidelidade estrutural/perceptual;
- a Ronda 14 continua melhor em `clip_iisim`, `region_score` e `heuristic_score`;
- a Ronda_15 ganha nas metricas que mais se aproximam de semelhanca visual direta do render com o target.

### Media do Top 20

Comparacao de medias do top 20:

| Metrica | Ronda 14 Top20 | Ronda_15 Top20 | Leitura |
| --- | ---: | ---: | --- |
| `selection_score` | 0.8921 | 0.9050 | melhorou |
| `combined_score` | 0.8726 | 0.8975 | melhorou |
| `clip_iisim` | 0.7918 | 0.7993 | melhorou ligeiramente |
| `lpips_alex` | 0.3601 | 0.3535 | melhorou |
| `pixel_rmse_01` | 0.0882 | 0.0784 | melhorou |
| `pixel_ssim_01` | 0.8201 | 0.8516 | melhorou |
| `color_hist_sim` | 0.7484 | 0.7707 | melhorou |
| `edge_sim` | 0.9338 | 0.9333 | desceu muito ligeiramente |
| `layout_sim` | 0.9848 | 0.9869 | melhorou |
| `visual_specific_score` | 0.8606 | 0.8708 | melhorou |
| `region_score` | 0.8279 | 0.8196 | desceu ligeiramente |
| `heuristic_score` | 0.7782 | 0.6838 | desceu de forma visivel |

Numero de entradas `pareto` no top 20:

- Ronda 14: `13`
- Ronda_15: `5`

Interpretacao:

- a Ronda_15 melhorou a qualidade media do top 20 em quase todas as metricas diretamente ligadas a semelhanca visual;
- a descida no `heuristic_score` e no numero de pontos `pareto` sugere que o novo dataset ficou mais focado e menos diverso;
- isso nao foi mau para `selection_score`, porque a familia de prompts vencedora ficou mais coerente e mais proxima do target na pratica.

## Conclusoes Para o Relatorio

### Conclusao desta run

Para `1159_7`, a Ronda_15 foi bem sucedida.

Podemos afirmar no relatorio:

- a estrategia de especializacao por classe funcionou para `1159_7`;
- aumentar o numero de prompts para `10000` e refinar os blocos semanticos produziu melhoria real;
- a nova formulacao compacta dos prompts nao prejudicou os resultados; pelo contrario, evitou truncagem do text encoder e ajudou a estabilizar a qualidade;
- a run atual supera a melhor run da Ronda 14 em `selection_score` e tambem supera a media do top 20 da Ronda 14.

### Conclusao global provisoria da Ronda_15

Globalmente, a leitura ainda e parcial, porque nesta fase so temos a categoria `1159_7` concluida. Mesmo assim, ja ha sinais fortes de que a Ronda_15 esta a ir na direcao certa:

- a geracao focada por classe parece melhor do que uma exploracao mais generalista;
- o uso de blocos mais especificos ao target ajuda a convergir para uma familia visual mais forte;
- a compactacao dos prompts para respeitar o limite do CLIP foi uma correcao importante e deve ser mantida;
- o metodo parece especialmente bom quando o target tem estrutura visual clara e repetivel, como o cubo de madeira com hedgehog no topo.

### O que ainda falta para uma conclusao global final

Para fechar a leitura global da Ronda_15, ainda falta executar e avaliar:

- `9338`

So depois disso sera possivel concluir com seguranca se a Ronda_15 melhora o conjunto das classes piores, ou se a melhoria foi sobretudo forte em `1159_7`.

## Formula de conclusao curta para o relatorio

Uma formulacao curta que pode entrar no relatorio:

```text
Na Ronda_15 adotou-se uma estrategia focada nas classes mais fracas da geracao em massa anterior, reduzindo o numero de targets e aumentando a profundidade da exploracao por classe. Para o target 1159_7, esta abordagem melhorou o melhor selection_score e tambem a media do top 20 face a Ronda 14, com ganhos claros em SSIM, RMSE, LPIPS, color similarity e layout similarity. Os resultados sugerem que prompts mais curtos, sem truncagem pelo CLIP, e blocos semanticos mais alinhados com a estrutura visual do target produzem uma geracao mais fiel e consistente.
```
