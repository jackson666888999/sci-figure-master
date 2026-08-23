# 生物信息学顶刊绘图代码克隆集成

> 集成日期：2026-08-23
> 用途：将生物信息学和医学顶刊的公开绘图代码克隆到此 assets 目录，供 sci-figure-master skill 使用

---

## 已克隆仓库清单

### 通用绘图工具（7个）

| 仓库 | 年份 | 语言 | 核心能力 | 许可证 | 本地路径 |
|------|------|------|----------|--------|----------|
| cnsplots | 2026 | Python | Cell/Nature/Science出版级绘图(25+图表)、像素控制、统计检验、SVG导出 | BSD-3 | `assets/cnsplots/` |
| figures4papers | 2025-2026 | Python | Nature MI/ICML/NeurIPS论文绘图脚本、LLM skill框架 | MIT | `assets/figures4papers/` |
| SciencePlots | 2025-2026 | Python | matplotlib样式库(Nature/IEEE)、多语言支持、色盲友好配色 | MIT | `assets/SciencePlots/` |
| journal-figure-studio | 2026 | Python | 可复现出版包生成、版本化配置、自动验证 | MIT | `assets/journal-figure-studio/` |
| Awesome-Scientific-Charts | 2025-2026 | R | R语言复现顶级期刊图表、中文注释 | MIT | `assets/Awesome-Scientific-Charts/` |
| SciVizKit | 2026 | Python | 80+图表类型、Web UI交互、智能推荐决策树 | MIT | `assets/SciVizKit/` |
| PubPlotLib | 2025-2026 | Python | 天体物理学专用样式、自动列宽处理 | GPL-3 | `assets/PubPlotLib/` |

### 生物信息学专用工具（6个）

| 仓库 | 年份 | 期刊 | 语言 | 核心能力 | 许可证 | 本地路径 |
|------|------|------|------|----------|--------|----------|
| GW | 2025 | Nature Methods | Python | Genome Browser可视化、基因组浏览、交互式轨道显示 | - | `assets/gw-gw/` |
| SpatialVista | 2026 | Nature Methods | Python | 空间转录组可视化、spot/region标注、组织切片 | - | `assets/spatial-vista/` |
| PLOSC² | 2024 | PLOS Computational Biology | R | scRNA-seq分析绘图脚本、Seurat集成、Enhanced Heatmap/DotPlot | - | `assets/plosc2/` |
| FeatureMAP | 2026 | Nature | Python | 特征保留流形可视化、降维、细胞状态追踪 | - | `assets/featuremap/` |
| animalcules | 2021 | Microbiome | Python | 微生物组可视化、Alpha/Beta多样性、丰度热图 | - | `assets/animalcules/` |
| JUMP Cell Painting | 2025 | Nature Methods | Python | Cell Painting形态图、Morphmap、高内涵筛选 | - | `assets/jump-cellpainting-morphmap/` |

---

## 快速使用示例

### 通用绘图

```python
# cnsplots（推荐）
import cnsplots as cns
cns.figure(width=200, height=150, color_cycle="Nature")
cns.boxplot(data=df, x="group", y="value", pairs=[("A", "B")])
cns.savefig("figure.svg")

# SciencePlots
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'nature'])
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(x, y)
plt.savefig('figure.pdf')
```

### 生物信息学绘图

```python
# 单细胞 scRNA-seq (PLOSC²)
# 见 assets/plosc2/README.md

# 空间转录组 (SpatialVista)
# 见 assets/spatial-vista/README.md

# 微生物组 (animalcules)
# 见 assets/animalcules/README.md

# 基因组浏览器 (GW)
# 见 assets/gw-gw/README.rst
```

---

## 依赖安装

### Python 依赖
```bash
pip install matplotlib numpy pandas seaborn scipy plotly
pip install scanpy anndata scikit-learn
pip install cnsplots scienceplots
```

### R 依赖
```r
install.packages(c("ComplexHeatmap", "ggplot2", "pheatmap", "circlize", "patchwork"))
BiocManager::install(c("Seurat", "SingleCellExperiment", "scater"))
```

---

## 版权说明

各仓库保留原有许可证：
- cnsplots: BSD-3
- figures4papers: MIT
- SciencePlots: MIT
- journal-figure-studio: MIT
- Awesome-Scientific-Charts: MIT
- SciVizKit: MIT
- PubPlotLib: GPL-3
- 其他：见各仓库 LICENSE 文件
