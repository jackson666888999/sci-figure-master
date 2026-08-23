# 生物信息学绘图 0动手路由配置（全面覆盖版）

> 本文件定义生物信息学**全部热门领域**的绘图工具路由规则
> 用户只需提供数据和图型需求，系统自动路由到正确的工具，无需跳转任何外部网站
> 更新日期：2026-08-23（覆盖 20+ 大领域 + 60+ 图型，含最新补录仓库）

---

## 路由规则总表（按领域分类）

### 一、单细胞 scRNA-seq（9 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 降维/可视化 | UMAP/tSNE | scanpy | `assets/scanpy/` | Python | anndata, umap-learn |
| 降维/可视化 | PCA/扩散图 | FeatureMAP | `assets/featuremap/` | Python | numpy |
| 特征表达 | 热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R | ComplexHeatmap |
| 特征表达 | 小提琴图 | SCpubr | `assets/SCpubr/` | R | SCpubr |
| 特征表达 | 点图/气泡图 | cnsplots | `assets/cnsplots/` | Python | matplotlib |
| 聚类/分群 | Clustree 聚类树 | scplotter | `assets/scplotter/` | R | scplotter |
| 差异表达 | Marker 列表 | cnsplots | `assets/cnsplots/` | Python | |
| 细胞通讯 | 配受体网络 | CellChat | `assets/CellChat/` | R | CellChat |
| 轨迹/拟时序 | RNA velocity | scVelo | `assets/scVelo/` | Python | scVelo |
| 轨迹/拟时序 | Monocle3 轨迹 | monocle3 | `assets/monocle3/` | R | monocle3 |

### 二、空间转录组（4 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| Visium/ST | 空间表达图 | SpatialVista | `assets/spatial-vista-py/` | Python | anndata |
| Visium/ST | 空间热图 | Squidpy | `assets/squidpy/` | Python | squidpy |
| 区域标注 | Spot/Region 标注 | SpatialVista | `assets/spatial-vista-py/` | Python | |
| 空间差异 | 差异区域检测 | Squidpy | `assets/squidpy/` | Python | |

### 三、基因组/CNV（5 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 基因组浏览 | 轨道图 | GW/kcleal | `assets/kcleal/` | Python | |
| 基因组浏览 | 轨道图（高配） | pyGenomeTracks | `assets/pyGenomeTracks/` | Python | pysam |
| 变异分析 | CNV 热图 | CNVkit | `assets/cnvkit/` | Python | cnvkit |
| 结构变异 | 断点圈图 | circlize | `assets/circlize/` | R | circlize |
| 变异展示 | Lollipop 图 | maftools | `assets/maftools/` | R | maftools |

### 四、表观遗传/ChIP-seq（4 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| ChIP-seq | 峰图/轨道 | pyGenomeTracks | `assets/pyGenomeTracks/` | Python | |
| ChIP-seq | 峰注释 | ChIPseeker | `assets/ChIPseeker/` | R | ChIPseeker |
| ATAC-seq | 峰注释 | ChIPseeker | `assets/ChIPseeker/` | R | |
| 甲基化 | 轨道图 | pyGenomeTracks | `assets/pyGenomeTracks/` | Python | |

### 五、宏基因组/16S（4 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| Alpha 多样性 | 多样性指数 | animalcules | `assets/animalcules/` | R | animalcules |
| Beta 多样性 | PCoA/NMDS | animalcules/phyloseq | `assets/animalcules/` | R | |
| 物种组成 | 堆叠图/条形图 | phyloseq | `assets/phyloseq/` | R | phyloseq |
| 差异分析 | LEfSe 差异 | animalcules | `assets/animalcules/` | R | |
| 热图 | 物种/OTU 热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R | |

### 六、系统发育（3 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 进化树 | 系统发育树 | ggtree | `assets/ggtree/` | R | ggtree |
| 比较基因组 | 基因排列 | gggenomes | `assets/gggenomes/` | R | gggenomes |
| 圈图 | 基因组圈图 | circlize | `assets/circlize/` | R | |

### 七、蛋白组/LC-MS（3 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 差异表达 | 火山图 | EnhancedVolcano | `assets/EnhancedVolcano/` | R | EnhancedVolcano |
| 差异表达 | 热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R | |
| 蛋白互作 | PPI 网络 | cnsplots | `assets/cnsplots/` | Python | |

### 八、代谢组（3 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 差异代谢 | 火山图 | EnhancedVolcano | `assets/EnhancedVolcano/` | R | |
| 通路分析 | 通路图 | MetaboAnalystR | `assets/MetaboAnalystR/` | R | MetaboAnalystR |
| 降维 | PLS-DA/OPLS-DA | MetaboAnalystR | `assets/MetaboAnalystR/` | R | |

### 九、富集分析（4 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| GO/KEGG | 气泡图/柱状图 | clusterProfiler | `assets/clusterProfiler/` | R | clusterProfiler |
| GO/KEGG | 网络图 | enrichplot | `assets/clusterProfiler/` | R | enrichplot |
| GSEA | GSEA 曲线 | clusterProfiler | `assets/clusterProfiler/` | R | |
| 通路富集 | 通路图 | MetaboAnalystR | `assets/MetaboAnalystR/` | R | |

### 十、多组学整合（3 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 因子分析 | 多组学因子 | MOFA2 | `assets/MOFA2/` | R | MOFA2 |
| 关联分析 | DIABLO 网络 | mixOmics | `assets/mixOmics/` | R | mixOmics |
| 批次校正 | 批次效应图 | BatchQC | `assets/BatchQC/` | Python | BatchQC |

### 十一、生存分析（2 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 预后 | KM 曲线 | survminer | `assets/survminer/` | R | survminer |
| 预后 | 森林图 | survminer | `assets/survminer/` | R | |

### 十二、流式细胞术（2 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| FACS/CyTOF | 散点图/密度图 | ggcyto | `assets/ggcyto/` | R | ggcyto |
| 门控可视化 | 门图 | flowCore | `assets/flowCore/` | R | flowCore |

### 十三、癌症基因组学（2 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 突变可视化 | Lollipop 图 | maftools | `assets/maftools/` | R | maftools |
| 突变景观 | 瀑布图 | maftools | `assets/maftools/` | R | |

### 十四、细胞成像/高内涵（2 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| Cell Painting | 形态图 | JUMP Cell Painting | `assets/jump-cellpainting-morphmap/` | Python | |
| 单细胞成像 | 形态分析 | JUMP Cell Painting | `assets/jump-cellpainting-morphmap/` | Python | |

### 十五、通用绘图（5 个工具）

| 子领域 | 图型需求 | 推荐工具 | 本地路径 | 语言 | 依赖 |
|--------|----------|----------|----------|------|------|
| 柱状图/箱线图 | 比较图 | cnsplots | `assets/cnsplots/` | Python | matplotlib |
| 复杂热图 | 多注释热图 | ComplexHeatmap | `assets/ComplexHeatmap/` | R | |
| 桑基图/Alluvium | 流动图 | cnsplots | `assets/cnsplots/` | Python | |
| 圈图/和弦图 | Circos 图 | circlize | `assets/circlize/` | R | |
| 火山图 | 差异表达 | EnhancedVolcano | `assets/EnhancedVolcano/` | R | |
| Nature/Science 样式 | 标准样式 | SciencePlots | `assets/SciencePlots/` | Python | matplotlib |
| 出版级图表 | 智能推荐 | SciVizKit | `assets/SciVizKit/` | Python | |

---

## 零动手自动化脚本（完整版）

### Python 路由函数

```python
def route_bioinfo_plot(domain, plot_type, data, output_path):
    """
    根据领域和图型自动路由到正确的绘图工具
    支持 20+ 领域、60+ 图型
    """
    routing = {
        # 单细胞
        ("scRNA", "UMAP"): ("scanpy", "assets/scanpy/"),
        ("scRNA", "tSNE"): ("scanpy", "assets/scanpy/"),
        ("scRNA", "PCA"): ("featuremap", "assets/featuremap/"),
        ("scRNA", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        ("scRNA", "violin"): ("SCpubr", "assets/SCpubr/"),
        ("scRNA", "dotplot"): ("cnsplots", "assets/cnsplots/"),
        ("scRNA", "clustree"): ("scplotter", "assets/scplotter/"),
        ("scRNA", "trajectory"): ("scVelo", "assets/scVelo/"),
        ("scRNA", "monocle"): ("monocle3", "assets/monocle3/"),
        ("scRNA", "cellchat"): ("CellChat", "assets/CellChat/"),
        
        # 空间转录组
        ("spatial", "distribution"): ("SpatialVista", "assets/spatial-vista-py/"),
        ("spatial", "heatmap"): ("Squidpy", "assets/squidpy/"),
        ("spatial", "annotation"): ("SpatialVista", "assets/spatial-vista-py/"),
        
        # 基因组
        ("genome", "browser"): ("GW", "assets/kcleal/"),
        ("genome", "track"): ("pyGenomeTracks", "assets/pyGenomeTracks/"),
        ("genome", "cnv"): ("CNVkit", "assets/cnvkit/"),
        ("genome", "circos"): ("circlize", "assets/circlize/"),
        
        # 表观
        ("epigenetic", "peaks"): ("pyGenomeTracks", "assets/pyGenomeTracks/"),
        ("epigenetic", "annotation"): ("ChIPseeker", "assets/ChIPseeker/"),
        
        # 宏基因组
        ("microbiome", "alpha"): ("animalcules", "assets/animalcules/"),
        ("microbiome", "beta"): ("animalcules", "assets/animalcules/"),
        ("microbiome", "composition"): ("phyloseq", "assets/phyloseq/"),
        ("microbiome", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        
        # 系统发育
        ("phylogeny", "tree"): ("ggtree", "assets/ggtree/"),
        ("phylogeny", "compare"): ("gggenomes", "assets/gggenomes/"),
        
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
        
        # 多组学
        ("multiomics", "factor"): ("MOFA2", "assets/MOFA2/"),
        ("multiomics", "correlation"): ("mixOmics", "assets/mixOmics/"),
        
        # 生存分析
        ("survival", "km"): ("survminer", "assets/survminer/"),
        ("survival", "forest"): ("survminer", "assets/survminer/"),
        
        # 流式
        ("flow", "scatter"): ("ggcyto", "assets/ggcyto/"),
        ("flow", "density"): ("flowCore", "assets/flowCore/"),
        
        # 癌症基因组
        ("cancer", "lollipop"): ("maftools", "assets/maftools/"),
        ("cancer", "waterfall"): ("maftools", "assets/maftools/"),
        
        # 细胞成像
        ("cellpainting", "morphmap"): ("JUMP", "assets/jump-cellpainting-morphmap/"),
        
        # 批次校正
        ("batch", "qc"): ("BatchQC", "assets/BatchQC/"),
        
        # 通用
        ("general", "bar"): ("cnsplots", "assets/cnsplots/"),
        ("general", "box"): ("cnsplots", "assets/cnsplots/"),
        ("general", "violin"): ("cnsplots", "assets/cnsplots/"),
        ("general", "heatmap"): ("ComplexHeatmap", "assets/ComplexHeatmap/"),
        ("general", "sankey"): ("cnsplots", "assets/cnsplots/"),
        ("general", "circos"): ("circlize", "assets/circlize/"),
        ("general", "volcano"): ("EnhancedVolcano", "assets/EnhancedVolcano/"),
        ("general", "nature"): ("SciencePlots", "assets/SciencePlots/"),
    }
    
    key = (domain, plot_type)
    if key in routing:
        tool, path = routing[key]
        return use_tool(tool, path, data, output_path)
    else:
        return use_tool("cnsplots", "assets/cnsplots/", data, output_path)
```

---

## 领域 → 工具 快速检索

| 用户说（关键词） | 自动路由到 |
|------------------|-----------|
| "单细胞 UMAP / tSNE / 降维" | scanpy / FeatureMAP |
| "单细胞热图 / marker 热图" | ComplexHeatmap / SCpubr |
| "细胞通讯 / CellChat / 配受体" | CellChat |
| "轨迹 / 拟时序 / RNA velocity" | scVelo / monocle3 |
| "空间转录组 / Visium / 空间图" | SpatialVista / Squidpy |
| "基因组浏览器 / 轨道 / Track" | GW / pyGenomeTracks |
| "CNV / 拷贝数变异" | CNVkit |
| "ChIP-seq / ATAC / 峰" | ChIPseeker / pyGenomeTracks |
| "16S / 宏基因组 / Alpha / Beta" | animalcules / phyloseq |
| "进化树 / 系统发育 / ggtree" | ggtree |
| "蛋白组 / 火山图" | EnhancedVolcano |
| "代谢组 / PLS-DA / 通路" | MetaboAnalystR |
| "GO / KEGG / GSEA / 富集" | clusterProfiler / enrichplot |
| "多组学 / MOFA / 整合" | MOFA2 / mixOmics |
| "生存 / KM / 预后" | survminer |
| "流式 / FACS / CyTOF" | ggcyto / flowCore |
| "突变 / Lollipop / 瀑布图" | maftools |
| "热图（任何领域）" | ComplexHeatmap |
| "圈图 / 和弦图 / Circos" | circlize |
| "桑基 / Alluvium" | cnsplots |
| "Nature 风格图表" | SciencePlots |

---

## 已克隆仓库清单（截至 2026-08-23）

### Python 仓库（9 个）

| 仓库 | 领域 | 说明 |
|------|------|------|
| scanpy | 单细胞 | scverse 核心，UMAP/tSNE/PCA |
| scVelo | 单细胞 | RNA velocity 轨迹推断 |
| squidpy | 空间转录组 | 空间模式分析/可视化 |
| pyGenomeTracks | 基因组 | 轨道图（64MB 大仓库） |
| cnvkit | 基因组 | CNV 拷贝数变异 |
| spatial-vista-py | 空间转录组 | 空间表达图 |
| kcleal | 基因组 | 基因组浏览 |
| jump-cellpainting-morphmap | 细胞成像 | Cell Painting 形态图 |
| cnsplots | 通用 | Nature/Science 出版级图表 |
| SciVizKit | 通用 | 80+ 图表智能推荐 |
| figures4papers | 通用 | Nature/ICML 论文绘图 |
| SciencePlots | 通用 | matplotlib Nature 样式 |
| jupyter-figure-studio | 通用 | 出版包生成 |
| BatchQC | 多组学 | 批次效应 QC |

### R 仓库（20 个）

| 仓库 | 领域 | 说明 |
|------|------|------|
| ComplexHeatmap | 热图 | 复杂多注释热图（939 文件） |
| circlize | 圈图 | Circos 和弦图 |
| EnhancedVolcano | 火山图 | 出版级火山图 |
| ggtree | 系统发育 | 进化树可视化 |
| phyloseq | 宏基因组 | 微生物组分析 |
| animalcules | 宏基因组 | 微生物组交互分析 |
| CellChat | 单细胞 | 细胞通讯网络 |
| ChIPseeker | 表观 | ChIP-seq 峰注释 |
| clusterProfiler | 富集 | GO/KEGG/GSEA |
| enrichplot | 富集 | 富集网络图 |
| MetaboAnalystR | 代谢组 | 通路分析 |
| MOFA2 | 多组学 | 因子分析 |
| mixOmics | 多组学 | DIABLO 整合 |
| survminer | 生存 | KM 曲线/森林图 |
| flowCore | 流式 | 流式数据基础 |
| ggcyto | 流式 | ggplot2 流式可视化 |
| maftools | 癌症基因组 | 突变 Lollipop/瀑布图 |
| gggenomes | 系统发育 | 比较基因组 |
| SCpubr | 单细胞 | 出版级单细胞图表 |
| monocle3 | 单细胞 | 轨迹推断 |
| scplotter | 单细胞 | Seurat 可视化 |

---

## 输出格式要求（顶刊标准）

- 矢量格式：SVG / PDF（投稿用）
- 位图格式：TIFF 600dpi / PNG 300dpi
- 配色：Nature/Science 标准色盲友好（Okabe-Ito）
- 字体：Arial，最小 8pt
- 坐标轴：仅 bottom/left，无顶/右边框
- 图例：无黑色背景
- 中文标注：必须渲染无乱码

---

## 错误处理

| 错误类型 | 处理策略 |
|----------|----------|
| 数据格式不匹配 | 自动转换 (AnnData ↔ Seurat ↔ MAE ↔ phyloseq) |
| 工具未安装 | 输出安装命令并提示 |
| 内存不足 | 降采样或分块处理 |
| 配色冲突 | 切换到色盲友好配色 |
| R 未安装 | 提示安装 R ≥4.3 + BiocManager |
| 依赖缺失 | 自动检测并给出完整安装脚本 |

---

## 安装命令

### Python 依赖
```bash
pip install scanpy scVelo squidpy pyGenomeTracks cnvkit anndata
pip install cnsplots scienceplots SciVizKit
```

### R 依赖
```r
BiocManager::install(c(
  "ComplexHeatmap", "circlize", "EnhancedVolcano", "ggtree",
  "phyloseq", "animalcules", "CellChat", "ChIPseeker",
  "clusterProfiler", "enrichplot", "MetaboAnalystR",
  "MOFA2", "mixOmics", "survminer", "flowCore", "ggcyto",
  "maftools", "gggenomes", "SCpubr", "monocle3", "scplotter"
))
```
