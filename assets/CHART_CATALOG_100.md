# Chart Catalog — 100+ 图表类型注册表

> 版本: 2026-08-24 | 总数: **141 种**（SciVizKit 79 + bioinfo-router 41 + R 工具链 21）

统一注册表文件: `assets/chart_catalog.py`
查询命令:
```bash
python assets/chart_catalog.py                          # 统计与清单
python -c "from chart_catalog import list_charts; print(list_charts())"
python -c "from chart_catalog import suggest_for_domain; print(suggest_for_domain('scRNA'))"
```

## 统计

| 来源 | 数量 | 说明 |
|------|------|------|
| SciVizKit | 79 | `assets/SciVizKit/`，80+ 图表类型注册表（纯 Python） |
| bioinfo-router | 41 | `assets/bioinfo_router.py`，生信特有图表（UMAP/火山/富集/KM等） |
| R 工具链 | 21 | ComplexHeatmap/circlize/ggtree/survminer 等 Bioconductor 包 |

## 分类分布（by_category）

| 类别 | 数量 | 代表图表 |
|------|------|----------|
| Distribution | 11 | histogram, kde, violin, boxplot, ridgeline, raincloud, ecdf, qqplot |
| Comparison | 16 | bar, grouped_bar, lollipop, dumbbell, diverging_bar, radial_bar, bar_sig |
| Correlation | 9 | scatter, bubble, hexbin, corr_heatmap, pairplot, parallel_coords |
| Time Series | 9 | line, area, stacked_area, streamgraph, bump_chart, candlestick |
| Proportional | 9 | pie, donut, treemap, waffle, nightingale, jade_ring, marimekko |
| Network | 6 | sankey, network_graph, dendrogram, chord_diagram, alluvial |
| Scientific | 16 | volcano, pca, roc_curve, radar, manhattan, forest_plot, kaplan_meier, umap, tsne |
| Single-Cell | 9 | umap, tsne, dotplot, clustree, trajectory, cellchat, rna_velocity |
| Microbiome | 4 | alpha_diversity, beta_diversity, composition, lefse |
| Genomics | 5 | genome_browser, genome_track, cnv, circos, manhattan |
| Enrichment | 4 | gsea, kegg_pathway, enrichment_bar, enrichment_dot |
| Survival | 2 | km, forest |
| R-Toolkit | 21 | r_heatmap, r_circlize, r_ggtree, r_survminer, r_deseq2 ... |
| 其他 | 20 | venn, upset, spatial, wgcna, motif, mofa, 3D, text, geo |

## 领域推荐（决策树一级路由）

| 领域 | 推荐图表 |
|------|----------|
| scRNA | umap, tsne, dotplot, violin, marker, heatmap, trajectory, cellchat |
| bulkRNA | volcano, ma_plot, gsea, kegg_pathway, heatmap, enrichment_bar, wgcna, venn |
| microbiome | alpha_diversity, beta_diversity, composition, lefse, sankey, heatmap |
| metabolomics | plsda, oplsda, volcano, pathway, sankey, heatmap |
| proteomics | volcano, heatmap, venn, upset |
| genome | genome_browser, genome_track, cnv, circos, manhattan |
| phylogeny | tree, circle_tree |
| survival | km, forest |
| enrichment | enrichment_bar, enrichment_dot, gsea, kegg_pathway |
| epigenetic | peaks, motif, chromatin_loop |
| multiomics | mofa, heatmap_complex, circos |
| spatial | spatial, umap, heatmap |

## 新增 SciVizKit 风格图表（纯 matplotlib，25 种）

ridgeline / raincloud / radar / lollipop / dumbbell / bubble / hexbin / pairplot /
parallel_coords / area / stacked_area / donut / treemap / waffle / nightingale /
dendrogram / qqplot / ecdf / bland_altman / diverging_bar / radial_bar /
marginal_plot / manhattan / ma_plot / forest_plot / funnel_plot

## 集成方式

```python
# 1. 直接路由（零动手）
from bioinfo_router import generate_figure
generate_figure("general", "raincloud", df, "out.svg", x="group", y="value")

# 2. 目录查询
from chart_catalog import get_chart, suggest_for_domain
meta = get_chart("volcano")          # 图表规格
recs = suggest_for_domain("microbiome")  # 领域推荐

# 3. 无人值守（ARIS）
python assets/aris_pipeline.py --data data.csv --topic "topic" --output report/
```
