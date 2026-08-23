# 生物信息学绘图 0动手路由配置

> 本文件定义生物信息学**全部热门领域**的绘图工具路由规则
> 用户只需提供数据和图型需求，系统自动路由到正确的工具，无需跳转任何外部网站
> 更新日期：2026-08-23（覆盖 15 大领域 + 40+ 图型）

---

## 路由规则总表

| 领域 | 子领域 | 图型需求 | 推荐工具 | 本地路径 | 依赖 |
|------|--------|----------|----------|----------|------|
| **单细胞** | scRNA-seq | UMAP/tSNE | scanpy/FeatureMAP | `assets/featuremap/` | Python: scanpy |
| | | 热图/特征表达 | ComplexHeatmap | `assets/ComplexHeatmap/` | R: ComplexHeatmap |
| | | 小提琴/点图 | cnsplots | `assets/cnsplots/` | Python: matplotlib |
| | | 聚类/marker | PLOSC² | `assets/plosc2/` | R: Seurat |
| | | 轨迹/拟时序 | scVelo/Monocle3 | `assets/plosc2/` | Python/R |
| | | 细胞通讯 | CellChat | `assets/CellChat/` | R: CellChat |
| **空间转录组** | Visium/ST/Slide-seq | 空间分布 | SpatialVista | `assets/spatial-vista-py/` | Python: anndata |
| | | 斑点/区域标注 | SpatialVista | `assets/spatial-vista-py/` | Python |
| | | 空间热图 | Squidpy | `assets/spatial-vista-py/` | Python |
| **基因组** | WGS/WES | 基因组浏览器 | GW/kcleal | `assets/kcleal/` | Python |
| | | 轨道图 | pyGenomeTracks | `assets/pyGenomeTracks/` | Python: pysam |
| | | 变异位点 | IGV | `assets/gw-gw/` | Java |
| | | CNV 分析 | CNVkit | `assets/cnvkit/` | Python: cnvkit |
| | | 断点/结构变异圈图 | circlize | `assets/circlize/` | R: circlize |
| **表观** | ChIP-seq/ATAC | 峰图 | deepTools | `assets/pyGenomeTracks/` | Python |
| | | 峰注释可视化 | ChIPseeker | `assets/ChIPseeker/` | R: ChIPseeker |
| | | 富集热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R |
| | | 甲基化 | pyGenomeTracks | `assets/pyGenomeTracks/` | Python |
| **宏基因组** | 16S/ITS/宏基因组 | Alpha多样性 | animalcules | `assets/animalcules/` | R: animalcules |
| | | Beta多样性 | animalcules/phyloseq | `assets/animalcules/` | R |
| | | 物种组成堆叠图 | phyloseq | `assets/phyloseq/` | R: phyloseq |
| | | 热图/树状图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R |
| | | LEfSe/差异 | animalcules | `assets/animalcules/` | R |
| **系统发育** | 进化树 | 系统发育树 | ggtree | `assets/ggtree/` | R: ggtree |
| | | 树+热图/圈图 | ggtree+circlize | `assets/ggtree/` | R |
| | | 比较基因组 | gggenomes | `assets/ggtree/` | R |
| **蛋白组** | LC-MS | 火山图 | EnhancedVolcano | `assets/EnhancedVolcano/` | R: EnhancedVolcano |
| | | 热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R |
| | | 蛋白互作网络 | Cytoscape | `assets/cnsplots/` | Python |
| **代谢组** | 靶向/非靶向 | 火山图 | EnhancedVolcano | `assets/EnhancedVolcano/` | R |
| | | 通路图 | MetaboAnalystR | `assets/MetaboAnalystR/` | R: MetaboAnalystR |
| | | PLS-DA/OPLS-DA | MetaboAnalystR | `assets/MetaboAnalystR/` | R |
| **富集分析** | GO/KEGG/GSEA | 富集柱状/气泡图 | clusterProfiler | `assets/clusterProfiler/` | R: clusterProfiler |
| | | 富集网络图 | enrichplot | `assets/clusterProfiler/` | R |
| | | GSEA 曲线 | clusterProfiler | `assets/clusterProfiler/` | R |
| **多组学** | 多组学整合 | 因子分析 | MOFA2 | `assets/MOFA2/` | R: MOFA2 |
| | | 多组学关联 | mixOmics | `assets/mixOmics/` | R: mixOmics |
| | | DIABLO 网络 | mixOmics | `assets/mixOmics/` | R |
| **生存分析** | 预后 | KM 生存曲线 | survminer | `assets/survminer/` | R: survminer |
| | | 森林图 | survminer | `assets/survminer/` | R |
| **流式细胞术** | FACS/CyTOF | 流式散点/密度 | flowCore | `assets/flowCore/` | R: flowCore |
| | | 门控可视化 | flowCore | `assets/flowCore/` | R |
| **细胞成像** | 高内涵 | 形态图 | JUMP Cell Painting | `assets/jump-cellpainting-morphmap/` | Python |
| | | 单细胞成像 | CellProfiler | `assets/jump-cellpainting-morphmap/` | Python |
| **通用** | 任何 | 柱状图/箱线图 | cnsplots | `assets/cnsplots/` | Python |
| | | 复杂热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R |
| | | 桑基图/Alluvium | cnsplots | `assets/cnsplots/` | Python |
| | | 和弦图/圈图 | circlize | `assets/circlize/` | R |
| | | 火山图 | EnhancedVolcano/cnsplots | `assets/EnhancedVolcano/` | R/Python |
| | | PCA/降维 | FeatureMAP | `assets/featuremap/` | Python |

---

## 零动手自动化脚本

### Python 路由函数（完整版）

```python
def route_bioinfo_plot(domain, plot_type, data, output_path):
    """
    根据领域和图型自动路由到正确的绘图工具
    支持 15 大领域、40+ 图型，未匹配时默认回退 cnsplots
    
    Args:
        domain: 领域 (scRNA, spatial, genome, epigenetic, microbiome,
                 phylogeny, proteomics, metabolomics, enrichment,
                 multiomics, survival, flow, cellpainting, general)
        plot_type: 图型 (UMAP, heatmap, volcano, tree, ...)
        data: 数据对象
        output_path: 输出路径
    """
    routing = {
        # 单细胞
        ("scRNA", "UMAP"): ("featuremap", "assets/featuremap/"),
        ("scRNA", "tsne"): ("scanpy", "assets/featuremap/"),
        ("scRNA", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        ("scRNA", "violin"): ("cnsplots", "assets/cnsplots/"),
        ("scRNA", "dotplot"): ("cnsplots", "assets/cnsplots/"),
        ("scRNA", "trajectory"): ("scvelo", "assets/plosc2/"),
        ("scRNA", "cellchat"): ("CellChat", "assets/CellChat/"),
        
        # 空间转录组
        ("spatial", "distribution"): ("SpatialVista", "assets/spatial-vista-py/"),
        ("spatial", "annotation"): ("SpatialVista", "assets/spatial-vista-py/"),
        ("spatial", "heatmap"): ("Squidpy", "assets/spatial-vista-py/"),
        
        # 基因组
        ("genome", "browser"): ("GW", "assets/kcleal/"),
        ("genome", "track"): ("pyGenomeTracks", "assets/pyGenomeTracks/"),
        ("genome", "cnv"): ("CNVkit", "assets/cnvkit/"),
        ("genome", "circos"): ("circlize", "assets/circlize/"),
        
        # 表观
        ("epigenetic", "peaks"): ("pyGenomeTracks", "assets/pyGenomeTracks/"),
        ("epigenetic", "annotation"): ("ChIPseeker", "assets/ChIPseeker/"),
        ("epigenetic", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        
        # 宏基因组
        ("microbiome", "alpha"): ("animalcules", "assets/animalcules/"),
        ("microbiome", "beta"): ("animalcules", "assets/animalcules/"),
        ("microbiome", "composition"): ("phyloseq", "assets/phyloseq/"),
        ("microbiome", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        ("microbiome", "lefse"): ("animalcules", "assets/animalcules/"),
        
        # 系统发育
        ("phylogeny", "tree"): ("ggtree", "assets/ggtree/"),
        ("phylogeny", "tree_heatmap"): ("ggtree", "assets/ggtree/"),
        ("phylogeny", "tree_circos"): ("ggtree", "assets/ggtree/"),
        
        # 蛋白组
        ("proteomics", "volcano"): ("EnhancedVolcano", "assets/EnhancedVolcano/"),
        ("proteomics", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        
        # 代谢组
        ("metabolomics", "volcano"): ("EnhancedVolcano", "assets/EnhancedVolcano/"),
        ("metabolomics", "pathway"): ("MetaboAnalystR", "assets/MetaboAnalystR/"),
        ("metabolomics", "plsda"): ("MetaboAnalystR", "assets/MetaboAnalystR/"),
        
        # 富集分析
        ("enrichment", "bar"): ("clusterProfiler", "assets/clusterProfiler/"),
        ("enrichment", "dotplot"): ("clusterProfiler", "assets/clusterProfiler/"),
        ("enrichment", "network"): ("enrichplot", "assets/clusterProfiler/"),
        ("enrichment", "gsea"): ("clusterProfiler", "assets/clusterProfiler/"),
        
        # 多组学
        ("multiomics", "factor"): ("MOFA2", "assets/MOFA2/"),
        ("multiomics", "correlation"): ("mixOmics", "assets/mixOmics/"),
        ("multiomics", "diablo"): ("mixOmics", "assets/mixOmics/"),
        
        # 生存分析
        ("survival", "km"): ("survminer", "assets/survminer/"),
        ("survival", "forest"): ("survminer", "assets/survminer/"),
        
        # 流式细胞术
        ("flow", "scatter"): ("flowCore", "assets/flowCore/"),
        ("flow", "density"): ("flowCore", "assets/flowCore/"),
        
        # 细胞成像
        ("cellpainting", "morphmap"): ("JUMP", "assets/jump-cellpainting-morphmap/"),
        
        # 通用
        ("general", "bar"): ("cnsplots", "assets/cnsplots/"),
        ("general", "box"): ("cnsplots", "assets/cnsplots/"),
        ("general", "sankey"): ("cnsplots", "assets/cnsplots/"),
        ("general", "circos"): ("circlize", "assets/circlize/"),
        ("general", "volcano"): ("cnsplots", "assets/cnsplots/"),
    }
    
    key = (domain, plot_type)
    if key in routing:
        tool, path = routing[key]
        return use_tool(tool, path, data, output_path)
    else:
        # 默认使用 cnsplots
        return use_tool("cnsplots", "assets/cnsplots/", data, output_path)
```

### R 路由函数（完整版）

```r
route_bioinfo_plot_r <- function(domain, plot_type, data, output_path) {
  # 单细胞热图
  if (domain == "scRNA" && plot_type == "heatmap") {
    library(ComplexHeatmap)
    draw(data, filename = output_path)
  }
  # 系统发育树
  if (domain == "phylogeny" && plot_type == "tree") {
    library(ggtree)
    p <- ggtree(data) + geom_tiplab()
    ggsave(output_path, p, width = 8, height = 6)
  }
  # 细胞通讯
  if (domain == "scRNA" && plot_type == "cellchat") {
    library(CellChat)
    netVisual_circle(data$net, vertex.weight = data$weight)
  }
  # 富集分析
  if (domain == "enrichment" && plot_type == "dotplot") {
    library(clusterProfiler)
    dotplot(data, showCategory = 20)
  }
  # 生存分析
  if (domain == "survival" && plot_type == "km") {
    library(survminer)
    ggsurvplot(data, pval = TRUE)
  }
  # 代谢组
  if (domain == "metabolomics" && plot_type == "plsda") {
    library(MetaboAnalystR)
    # PLS-DA score plot
  }
  # 宏基因组
  if (domain == "microbiome" && plot_type == "alpha") {
    library(animalcules)
    alpha_div_boxplot(data, tax_level = "genus",
                      condition = "DISEASE",
                      alpha_metric = "shannon")
  }
}
```

---

## 领域 → 工具 快速检索（按关键词自动路由）

| 用户说（关键词） | 自动路由到 |
|------------------|-----------|
| "单细胞 UMAP / tSNE / 降维" | scanpy / FeatureMAP |
| "单细胞热图 / marker 热图" | ComplexHeatmap |
| "细胞通讯 / CellChat / 配受体" | CellChat |
| "轨迹 / 拟时序 / Monocle" | scVelo / Monocle3 |
| "空间转录组 / Visium / 空间图" | SpatialVista |
| "基因组浏览器 / 轨道 / Track" | GW / pyGenomeTracks |
| "CNV / 拷贝数变异" | CNVkit |
| "ChIP-seq / ATAC / 峰" | ChIPseeker / pyGenomeTracks |
| "16S / 宏基因组 / Alpha / Beta" | animalcules / phyloseq |
| "进化树 / 系统发育 / ggtree" | ggtree |
| "蛋白组 / 火山图" | EnhancedVolcano |
| "代谢组 / PLS-DA / 通路" | MetaboAnalystR |
| "GO / KEGG / GSEA / 富集" | clusterProfiler |
| "多组学 / MOFA / 整合" | MOFA2 / mixOmics |
| "生存 / KM / 预后" | survminer |
| "流式 / FACS / CyTOF" | flowCore |
| "热图（任何领域）" | ComplexHeatmap |
| "圈图 / 和弦图 / Circos" | circlize |
| "桑基 / Alluvium" | cnsplots |

---

## 输出格式要求

所有输出必须遵循顶刊标准：
- 矢量格式：SVG / PDF（投稿用）
- 位图格式：TIFF 600dpi / PNG 300dpi
- 配色：Nature/Science 标准色盲友好（Okabe-Ito）
- 字体：Arial，最小 8pt
- 坐标轴：仅 bottom/left，无顶/右边框
- 图例：无黑色背景
- 中文标注：必须渲染无乱码（SciencePlots 多语言支持）

---

## 错误处理

| 错误类型 | 处理策略 |
|----------|----------|
| 数据格式不匹配 | 自动转换 (AnnData ↔ Seurat ↔ MAE ↔ phyloseq) |
| 工具未安装 | 输出安装命令并提示（R: BiocManager::install / Python: pip install） |
| 内存不足 | 降采样或分块处理 |
| 配色冲突 | 切换到色盲友好配色 |
| R 未安装 | 提示安装 R ≥4.3 + BiocManager |
| 依赖缺失 | 自动检测并给出完整安装脚本（见 INTEGRATION.md） |

---

## 已克隆仓库清单（本配置引用的本地路径）

```
assets/animalcules/           R: 微生物组交互分析
assets/CellChat/              R: 细胞通讯网络
assets/ChIPseeker/            R: ChIP-seq 峰注释
assets/circlize/              R: 圈图/和弦图
assets/clusterProfiler/       R: GO/KEGG/GSEA 富集
assets/cnvkit/                Python: CNV 分析
assets/ComplexHeatmap/        R: 复杂热图
assets/EnhancedVolcano/       R: 火山图
assets/flowCore/              R: 流式细胞术
assets/ggtree/                R: 系统发育树
assets/MetaboAnalystR/        R: 代谢组分析
assets/mixOmics/              R: 多组学整合
assets/MOFA2/                 R: 多组学因子分析
assets/phyloseq/              R: 微生物组分析
assets/pyGenomeTracks/        Python: 基因组轨道
assets/survminer/             R: 生存分析
```
