# Resultados Ronda_15 - 9338

## Contexto

Este documento resume os resultados da run:

```text
TP2-students/students/outputs/ronda_15_gerracaoclasses_piores/runs_from_dataset/20260603-133402_pt_9338
```

Nesta execucao foram avaliados:

- `10000` prompts para a categoria `9338`
- `top_k = 20`
- `render_device = cuda`
- `metric_device = cuda`

O objetivo aqui e o mesmo do documento anterior:

1. apresentar o top 20 da run;
2. comparar com a Ronda 14 para `9338`;
3. retirar conclusoes para o relatorio desta run e da estrategia global da Ronda_15.

## Resumo Executivo

O resultado para `9338` tambem e positivo, embora a melhoria seja mais moderada do que em `1159_7`.

Melhor score:

- Ronda 14 best selection score: `0.9067756362418452`
- Ronda_15 best selection score: `0.9072480942534976`
- melhoria absoluta: `+0.0004724580116524`

Media do top 20:

- Ronda 14 media `selection_score`: `0.821685789353306`
- Ronda_15 media `selection_score`: `0.8411681247290287`
- melhoria absoluta: `+0.0194823353757227`

Isto sugere uma leitura importante: a Ronda_15 quase nao alterou o melhor caso absoluto de `9338`, mas melhorou bastante a qualidade media do top 20. Em outras palavras, a exploracao ficou mais consistente e menos dependente de um ou dois prompts muito bons isolados.

## Melhor Prompt Encontrado

Melhor prompt da Ronda_15 para `9338`:

```text
colorful fantasy hamster dragon, orange snout glossy black eye, cream chest teal oval belly, luminous mosaic scale spots, pink horn blue magenta spines, small clawed forepaws, warm yellow green arcs, detailed fantasy character painting
```

Principais metricas do melhor resultado:

- `selection_score`: `0.9072480942534976`
- `combined_score`: `0.8772480942534976`
- `clip_iisim`: `0.818747878074646`
- `lpips_alex`: `0.5514023303985596`
- `pixel_rmse_01`: `0.12437936442711217`
- `pixel_ssim_01`: `0.661913513015188`
- `color_hist_sim`: `0.8775216561776621`
- `edge_sim`: `0.9436691798565245`
- `layout_sim`: `0.9762186470682565`
- `visual_specific_score`: `0.9204126876433828`
- `region_score`: `0.9023417579979239`
- `heuristic_score`: `0.6316392305985468`

## Top 20 Detalhado

### Tabela Resumida

| Rank | ID | Selection | Combined | CLIP | LPIPS | RMSE | SSIM | Color | Edge | Layout | Visual | Region | Pareto |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 09585 | 0.9072 | 0.8772 | 0.8187 | 0.5514 | 0.1244 | 0.6619 | 0.8775 | 0.9437 | 0.9762 | 0.9204 | 0.9023 | True |
| 2 | 09182 | 0.8903 | 0.8603 | 0.8543 | 0.5201 | 0.1538 | 0.6193 | 0.7237 | 0.9505 | 0.9616 | 0.8506 | 0.8238 | True |
| 3 | 08497 | 0.8714 | 0.8414 | 0.8144 | 0.5481 | 0.1252 | 0.6384 | 0.8638 | 0.9332 | 0.9597 | 0.9073 | 0.8799 | True |
| 4 | 09600 | 0.8681 | 0.8381 | 0.8276 | 0.5629 | 0.1303 | 0.6561 | 0.7951 | 0.9425 | 0.9612 | 0.8799 | 0.8734 | True |
| 5 | 00961 | 0.8637 | 0.8337 | 0.7701 | 0.5507 | 0.1190 | 0.6516 | 0.8756 | 0.9368 | 0.9787 | 0.9176 | 0.8824 | True |
| 6 | 03243 | 0.8630 | 0.8330 | 0.8499 | 0.5842 | 0.1221 | 0.6473 | 0.8450 | 0.9299 | 0.9635 | 0.8984 | 0.8884 | True |
| 7 | 09850 | 0.8614 | 0.8314 | 0.8507 | 0.5625 | 0.1520 | 0.6236 | 0.7914 | 0.9404 | 0.9761 | 0.8805 | 0.8600 | True |
| 8 | 04800 | 0.8511 | 0.8211 | 0.7733 | 0.5756 | 0.1212 | 0.6640 | 0.8436 | 0.9440 | 0.9802 | 0.9061 | 0.8865 | True |
| 9 | 02891 | 0.8457 | 0.8157 | 0.8291 | 0.5560 | 0.1478 | 0.5332 | 0.7968 | 0.9520 | 0.9638 | 0.8845 | 0.8852 | True |
| 10 | 06109 | 0.8364 | 0.8064 | 0.8373 | 0.5424 | 0.1535 | 0.5235 | 0.7744 | 0.9474 | 0.9502 | 0.8701 | 0.8689 | True |
| 11 | 02216 | 0.8297 | 0.8297 | 0.8076 | 0.5588 | 0.1286 | 0.5663 | 0.8846 | 0.9413 | 0.9708 | 0.9217 | 0.9088 | False |
| 12 | 05304 | 0.8248 | 0.7948 | 0.7994 | 0.5404 | 0.1396 | 0.6147 | 0.7556 | 0.9297 | 0.9772 | 0.8609 | 0.8320 | True |
| 13 | 07827 | 0.8212 | 0.7912 | 0.8847 | 0.6291 | 0.1503 | 0.5572 | 0.8206 | 0.9426 | 0.9695 | 0.8931 | 0.8713 | True |
| 14 | 05243 | 0.8208 | 0.8208 | 0.8250 | 0.5854 | 0.1367 | 0.5870 | 0.8245 | 0.9479 | 0.9841 | 0.8996 | 0.8704 | False |
| 15 | 09596 | 0.8198 | 0.7898 | 0.8576 | 0.5963 | 0.1483 | 0.6185 | 0.7703 | 0.9332 | 0.9712 | 0.8675 | 0.8444 | True |
| 16 | 03026 | 0.8155 | 0.7855 | 0.8582 | 0.5896 | 0.1565 | 0.4596 | 0.8277 | 0.9450 | 0.9800 | 0.8992 | 0.8700 | True |
| 17 | 06232 | 0.8146 | 0.7846 | 0.8673 | 0.6011 | 0.1654 | 0.5368 | 0.7459 | 0.9531 | 0.9717 | 0.8636 | 0.8396 | True |
| 18 | 09586 | 0.8084 | 0.8084 | 0.7906 | 0.5606 | 0.1402 | 0.6069 | 0.8525 | 0.9400 | 0.9742 | 0.9075 | 0.8919 | False |
| 19 | 03822 | 0.8062 | 0.8062 | 0.8424 | 0.6010 | 0.1304 | 0.6157 | 0.8354 | 0.9354 | 0.9661 | 0.8965 | 0.8844 | False |
| 20 | 07832 | 0.8040 | 0.7740 | 0.8662 | 0.6560 | 0.1425 | 0.6057 | 0.7978 | 0.9478 | 0.9627 | 0.8833 | 0.8511 | True |

### Leitura do Top 20

Observacoes principais:

- O top 20 de `9338` e bastante mais distribuido do que o de `1159_7`; nao ha uma separacao tao forte entre top 1 e o resto.
- Os melhores prompts convergem para uma familia visual muito clara:
  - `colorful fantasy hamster dragon` ou `rainbow dragon hamster profile`
  - `orange snout glossy black eye`
  - `cream chest teal oval belly`
  - `luminous mosaic scale spots` ou `tiny LED bead scales`
  - `pink horn blue magenta spines`
  - `warm yellow green arcs` ou fundos painterly de cor
- A Ronda_15 parece ter captado melhor os aspetos de cor, pontos luminosos e perfil geral da criatura.

## Estatisticas Agregadas do Top 20

### Ronda_15 - Top 20

- media `selection_score`: `0.8411681247290287`
- mediana `selection_score`: `0.8330349737852494`
- minimo `selection_score`: `0.8039882912918527`
- maximo `selection_score`: `0.9072480942534976`
- media `combined_score`: `0.8171681247290287`
- media `clip_iisim`: `0.8312229305505753`
- media `lpips_alex`: `0.57361498773098`
- media `pixel_rmse_01`: `0.1393819123504522`
- media `pixel_ssim_01`: `0.5993824224594542`
- media `color_hist_sim`: `0.8150928638599537`
- media `edge_sim`: `0.9418302161416962`
- media `layout_sim`: `0.9699357968032645`
- media `visual_specific_score`: `0.8904195237472258`
- media `region_score`: `0.8707358596915659`
- media `heuristic_score`: `0.6095151017840961`
- numero de entradas `pareto`: `16` em `20`

Interpretacao:

- ha boa diversidade no top 20, com muitos pontos ainda pertencentes ao fronteiro Pareto;
- o comportamento sugere que para `9338` a exploracao ainda esta mais aberta, sem uma familia unica tao dominante como aconteceu em `1159_7`;
- as metricas de cor, contorno e aspeto visual especifico do target estao globalmente fortes.

## Comparacao com a Ronda 14

Referencia usada:

```text
TP2-students/students/outputs/ronda_14_.../runs_from_dataset/20260531-182043_pt_9338
```

### Melhor Resultado

Melhor Ronda 14:

- `selection_score`: `0.9067756362418452`
- `combined_score`: `0.8767756362418452`
- `clip_iisim`: `0.8416189551353455`
- `lpips_alex`: `0.5463301539421082`
- `pixel_rmse_01`: `0.14104452735186984`
- `pixel_ssim_01`: `0.6180169091143896`
- `color_hist_sim`: `0.8075307210286459`
- `edge_sim`: `0.9494870492380221`
- `layout_sim`: `0.9696207388381558`
- `visual_specific_score`: `0.8896334394638297`
- `region_score`: `0.8860312954394193`
- `heuristic_score`: `0.6202219068075935`

Melhor Ronda_15:

- `selection_score`: `0.9072480942534976`
- `combined_score`: `0.8772480942534976`
- `clip_iisim`: `0.818747878074646`
- `lpips_alex`: `0.5514023303985596`
- `pixel_rmse_01`: `0.12437936442711217`
- `pixel_ssim_01`: `0.661913513015188`
- `color_hist_sim`: `0.8775216561776621`
- `edge_sim`: `0.9436691798565245`
- `layout_sim`: `0.9762186470682565`
- `visual_specific_score`: `0.9204126876433828`
- `region_score`: `0.9023417579979239`
- `heuristic_score`: `0.6316392305985468`

Leitura:

- o melhor caso absoluto da Ronda_15 ganha por pouco no `selection_score`;
- a Ronda_15 melhora claramente em `RMSE`, `SSIM`, `color_hist_sim`, `layout_sim`, `visual_specific_score`, `region_score` e `heuristic_score`;
- a Ronda 14 continua melhor em `clip_iisim`, `lpips_alex` e `edge_sim`;
- o melhor caso da Ronda_15 parece mais alinhado com a identidade visual global do target, sobretudo cor e organizacao espacial.

### Media do Top 20

Comparacao de medias do top 20:

| Metrica | Ronda 14 Top20 | Ronda_15 Top20 | Leitura |
| --- | ---: | ---: | --- |
| `selection_score` | 0.8217 | 0.8412 | melhorou |
| `combined_score` | 0.8037 | 0.8172 | melhorou |
| `clip_iisim` | 0.8277 | 0.8312 | melhorou ligeiramente |
| `lpips_alex` | 0.5729 | 0.5736 | piorou ligeiramente |
| `pixel_rmse_01` | 0.1365 | 0.1394 | piorou ligeiramente |
| `pixel_ssim_01` | 0.6263 | 0.5994 | piorou |
| `color_hist_sim` | 0.7913 | 0.8151 | melhorou |
| `edge_sim` | 0.9439 | 0.9418 | desceu ligeiramente |
| `layout_sim` | 0.9738 | 0.9699 | desceu ligeiramente |
| `visual_specific_score` | 0.8812 | 0.8904 | melhorou |
| `region_score` | 0.8784 | 0.8707 | desceu ligeiramente |
| `heuristic_score` | 0.6242 | 0.6095 | desceu |

Numero de entradas `pareto` no top 20:

- Ronda 14: `12`
- Ronda_15: `16`

Interpretacao:

- a Ronda_15 melhora a media do score final, o que mostra progresso real;
- os ganhos mais claros aparecem em `color_hist_sim`, `visual_specific_score` e um pequeno ganho em `clip_iisim`;
- por outro lado, a media de `SSIM`, `RMSE`, `layout_sim` e `region_score` nao melhora;
- isto sugere que a Ronda_15 conseguiu capturar melhor o estilo geral, a cor e a identidade do target `9338`, mas ainda nao estabilizou totalmente a estrutura local e a correspondencia fina.

## Conclusoes Para o Relatorio

### Conclusao desta run

Para `9338`, a Ronda_15 tambem trouxe melhoria, mas com um perfil diferente do observado em `1159_7`.

Podemos afirmar no relatorio:

- a Ronda_15 conseguiu superar marginalmente o melhor resultado absoluto da Ronda 14;
- a media do top 20 melhorou de forma mais clara do que o melhor caso individual;
- os novos prompts parecem particularmente fortes a capturar a paleta, o brilho das escamas/pontos e a identidade fantastica da criatura;
- a estrutura mais fina da imagem ainda mostra margem para refinamento, porque algumas metricas de semelhanca local e perceptual nao melhoraram na mesma proporcao.

### Conclusao global da Ronda_15

Com `1159_7` e `9338` avaliados, ja podemos tirar uma conclusao mais global da estrategia.

A leitura geral e:

- a Ronda_15 funcionou;
- a estrategia de focar apenas as classes piores e aumentar a profundidade por classe foi valida;
- os resultados melhoraram nos dois targets analisados, embora com intensidades diferentes;
- `1159_7` mostrou uma melhoria mais limpa e mais forte;
- `9338` melhorou mais na consistencia media, cor e identidade visual do que na geometria/perceptual similarity mais fina.

Isto significa que a abordagem da Ronda_15 foi boa como estrategia de recuperacao dirigida, especialmente quando o target tem elementos visuais bem nomeaveis e facilmente decomponiveis em blocos semanticos.

### Formula de conclusao curta para o relatorio

Uma formulacao curta que pode entrar no relatorio:

```text
Na Ronda_15, a exploracao foi restringida aos targets com pior desempenho anterior e os prompts foram reconstruidos com blocos semanticos mais especificos e sem truncagem pelo encoder CLIP. Para 1159_7, esta estrategia produziu melhoria clara tanto no melhor resultado como na media do top 20. Para 9338, o melhor resultado melhorou apenas marginalmente, mas a media do top 20 subiu de forma relevante, indicando uma geracao mais consistente e mais alinhada com a identidade visual do target. Globalmente, a Ronda_15 valida a estrategia de refinamento focado por classe como uma extensao eficaz da geracao em massa anterior.
```
