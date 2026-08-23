# Bioinformatics Figure Generation - 0-touch Automation（零动手）

> 全自动生物信息学绘图：用户只需提供数据+图型需求，无需跳转任何外部网站。
> 覆盖 15 大热门领域 × 40+ 图型。更新日期：2026-08-23

## Features

- **Zero-touch（零动手）**: 无需手动访问任何绘图网站
- **Multi-domain**: 单细胞/空间/基因组/表观/宏基因组/系统发育/蛋白组/代谢组/富集/多组学/生存/流式/成像/通用
- **Top-journal ready**: Cell/Nature/Science 出版质量
- **Multiple outputs**: SVG, PDF, TIFF 600dpi, PNG 300dpi

---

## 支持的领域与图型

| 领域 | 图型 | 工具 | 本地路径 |
|------|------|------|----------|
| scRNA | UMAP, tSNE, Heatmap, Violin, DotPlot, Trajectory, CellChat | scanpy/FeatureMAP/ComplexHeatmap/CellChat | `assets/featuremap/`, `assets/CellChat/`, `assets/ComplexHeatmap/` |
| Spatial | Distribution, Annotation, Heatmap | SpatialVista | `assets/spatial-vista-py/` |
| Genome | Browser, Track, CNV, Circos | GW/pyGenomeTracks/CNVkit/circlize | `assets/kcleal/`, `assets/pyGenomeTracks/`, `assets/cnvkit/` |
| Epigenetic | Peaks, Annotation, Methylation | pyGenomeTracks/ChIPseeker | `assets/ChIPseeker/` |
| Microbiome | Alpha/Beta Diversity, Composition, LEfSe | animalcules/phyloseq | `assets/animalcules/`, `assets/phyloseq/` |
| Phylogeny | Tree, Tree+Heatmap, Circos | ggtree | `assets/ggtree/` |
| Proteomics | Volcano, Heatmap | EnhancedVolcano/ComplexHeatmap | `assets/EnhancedVolcano/` |
| Metabolomics | Volcano, Pathway, PLS-DA | EnhancedVolcano/MetaboAnalystR | `assets/MetaboAnalystR/` |
| Enrichment | Bar, Dotplot, Network, GSEA | clusterProfiler | `assets/clusterProfiler/` |
| Multi-omics | Factor, Correlation, DIABLO | MOFA2/mixOmics | `assets/MOFA2/`, `assets/mixOmics/` |
| Survival | KM curve, Forest plot | survminer | `assets/survminer/` |
| Flow | Scatter, Density | flowCore | `assets/flowCore/` |
| CellPainting | Morphmap | JUMP | `assets/jump-cellpainting-morphmap/` |
| General | Bar, Box, Sankey, Circos, Volcano | cnsplots/circlize | `assets/cnsplots/` |

---

## 零动手使用示例

### 场景 1：单细胞 UMAP（Python）
```python
import scanpy as sc
from sci_figure_master.bioinfo import generate_figure

# 1. 加载数据
adata = sc.read_h5ad("data.h5ad")

# 2. 标准流程
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.tl.pca(adata)
sc.tl.umap(adata)

# 3. 零动手出图
generate_figure(domain="scRNA", plot_type="UMAP",
                data=adata, output_path="UMAP.svg")
```

### 场景 2：宏基因组 Alpha 多样性（R）
```r
library(animalcules)

# 加载数据
data_dir <- system.file("extdata/MAE.rds", package = "animalcules")
toy_data <- readRDS(data_dir)

# 零动手出图
p <- alpha_div_boxplot(toy_data, tax_level = "genus",
                       condition = "DISEASE",
                       alpha_metric = "shannon")
ggsave("alpha_diversity.pdf", p)
```

### 场景 3：富集分析气泡图（R）
```r
library(clusterProfiler)

# 假设已运行 enrichGO / enrichKEGG
p <- dotplot(ego, showCategory = 20)
ggsave("enrichment_dotplot.pdf", p, width = 8, height = 6)
```

### 场景 4：系统发育树（R）
```r
library(ggtree)

tree <- read.tree("phylogeny.nwk")
p <- ggtree(tree) + geom_tiplab() +
     geom_nodelab(aes(label = node), hjust = -0.2)
ggsave("phylogeny_tree.svg", p, width = 8, height = 10)
```

### 场景 5：细胞通讯网络（R）
```r
library(CellChat)

# 加载 CellChat 对象
cellchat <- readRDS("cellchat.rds")
netVisual_circle(cellchat@net$count,
                 vertex.weight = table(cellchat@idents),
                 weight.scale = TRUE)
```

### 场景 6：KM 生存曲线（R）
```r
library(survminer)
library(survival)

fit <- survfit(Surv(time, status) ~ group, data = clinical)
p <- ggsurvplot(fit, data = clinical, pval = TRUE,
                risk.table = TRUE, palette = "jco")
ggsave("KM_curve.pdf", p, width = 8, height = 6)
```

### 场景 7：CNV 全景图（Python）
```python
import cnvkit

# CNVkit 命令行（bam 文件已比对）
# cnvkit.py batch tumor.bam -n normal.bam --fasta ref.fa -o cnv_output/
# 可视化
# cnvkit.py scatter cnv_output/tumor.cns
```

---

## CLI

```bash
# 生成热图
python -m sci_figure_master.bioinfo generate \
    --domain scRNA \
    --plot heatmap \
    --input data.h5ad \
    --output heatmap.pdf

# 生成 UMAP
python -m sci_figure_master.bioinfo generate \
    --domain scRNA \
    --plot UMAP \
    --input data.h5ad \
    --output umap.svg

# 生成火山图
python -m sci_figure_master.bioinfo generate \
    --domain proteomics \
    --plot volcano \
    --input DE_results.csv \
    --output volcano.svg
```

---

## 常见坑（已实测修复）

### SciencePlots usetex 报错
`science/nature` 样式默认 `text.usetex=True`，**无 LaTeX 环境会报 `latex could not be found`**。
修复：**先应用样式，再禁用 usetex（顺序不能反，style.use 会覆盖 rcParams）**：
```python
import scienceplots
plt.style.use(['science', 'nature'])   # 先应用
plt.rcParams['text.usetex'] = False    # 再禁用（顺序关键！）
```
已实测通过：matplotlib 3.11.1 + scienceplots 无 LaTeX 环境出图正常。

---

## 安装依赖（一键）

### Python 依赖
```bash
pip install scanpy anndata matplotlib numpy pandas seaborn scienceplots
pip install -e assets/cnsplots
pip install -e assets/pyGenomeTracks
pip install -e assets/cnvkit
```

### R 依赖（BiocManager）
```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("ComplexHeatmap", "ChIPseeker", "clusterProfiler",
                       "phyloseq", "flowCore"))
install.packages(c("ggtree", "circlize", "survminer", "EnhancedVolcano"))
# CellChat / MetaboAnalystR / MOFA2 / mixOmics / animalcules 按官方文档安装
```

---

## References（本地路径）

- assets/cnsplots/
- assets/featuremap/
- assets/plosc2/
- assets/spatial-vista-py/
- assets/kcleal/ (GW)
- assets/pyGenomeTracks/
- assets/ChIPseeker/
- assets/animalcules/
- assets/phyloseq/
- assets/ggtree/
- assets/circlize/
- assets/EnhancedVolcano/
- assets/MetaboAnalystR/
- assets/clusterProfiler/
- assets/MOFA2/
- assets/mixOmics/
- assets/survminer/
- assets/flowCore/
- assets/ComplexHeatmap/
- assets/cnvkit/
