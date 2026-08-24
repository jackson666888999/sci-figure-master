# 无人值守自动出图系统使用说明

## 概述

**auto_figure.py** 是科研绘图系统的核心自动化模块，支持：

1. **一键出图**：只给文件路径，自动完成分析+画图
2. **智能路由**：自动识别数据类型，选择最佳分析工具和绘图方法
3. **无人值守**：批量处理目录，自动生成所有需要的图表
4. **顶刊标准**：输出 SVG/PDF/TIFF/PNG，符合 Nature/Science 投稿要求

---

## 快速开始

### 命令行用法

```bash
# 单个文件
python auto_figure.py --input data.h5ad

# 指定输出目录
python auto_figure.py --input data.csv --output ./figures

# 批量处理目录
python auto_figure.py --input ./data/ --output ./output/

# 详细输出
python auto_figure.py --input data.h5ad --verbose
```

### Python API 用法

```python
from auto_figure import AutoFigureSystem

# 创建系统
system = AutoFigureSystem(output_dir="./output")

# 处理单个文件
results = system.process_file("data.h5ad")

# 处理目录
results = system.process_directory("./data/")

# 运行（推荐）
results = system.run("data.h5ad", "./output/")
```

---

## 支持的数据类型

| 文件类型 | 扩展名 | 自动检测 | 推荐分析 |
|----------|--------|----------|----------|
| 单细胞 | .h5ad, .h5, .loom | UMAP/PCA/tSNE, 聚类 | scRNA-seq |
| 通用表格 | .csv, .tsv, .txt | 列名特征检测 | 描述统计/相关性 |
| Excel | .xlsx, .xls | - | 描述统计/可视化 |
| 宏基因组 | .mt, .biom | OTU/ASV检测 | 多样性分析 |
| 代谢组 | .mpk, .mzML | 代谢物检测 | 差异分析 |

---

## 自动分析流程

### 1. 数据识别
```python
# 自动检测文件类型
file_type = system.identify_file_type(Path("data.h5ad"))
# 输出: 'scRNA'
```

### 2. 数据加载
```python
# 自动选择加载器
data = system.load_data(Path("data.h5ad"), 'scRNA')
# 返回: AnnData 对象
```

### 3. 自动分析
```python
# 自动选择统计方法
analysis = system.auto_analysis(data, 'scRNA')
# 输出: {
#   'methods': ['UMAP', 'PCA', 'clustering', 'marker_genes'],
#   'plots': ['UMAP', 'heatmap', 'violin', 'dotplot'],
#   'cluster_col': 'louvain',
#   'top_genes': ['Gene1', 'Gene2', ...]
# }
```

### 4. 自动出图
```python
# 自动生成所有图表
files = system.generate_auto_figure(data, 'scRNA', analysis, output_path)
# 输出: ['UMAP.svg', 'PCA.svg', 'heatmap.svg', 'violin.svg', ...]
```

---

## 输出文件说明

### 单细胞数据 (scRNA)
| 文件 | 说明 |
|------|------|
| `xxx.umap.svg` | UMAP降维聚类图 |
| `xxx.pca.svg` | PCA降维图 |
| `xxx.heatmap.svg` | 高变基因热图 |
| `xxx.violin.svg` | 标记基因表达图 |
| `xxx.dotplot.svg` | 基因表达点图 |

### 通用数据
| 文件 | 说明 |
|------|------|
| `xxx.heatmap.svg` | 相关性热图 |
| `xxx.box.svg` | 分组箱线图 |
| `xxx.bar.svg` | 统计柱状图 |
| `xxx.scatter.svg` | 散点图 |

---

## 完整工作流示例

### 示例1: 单细胞数据
```python
from auto_figure import AutoFigureSystem

# 创建系统
system = AutoFigureSystem(output_dir="./output")

# 处理单细胞数据
results = system.run(
    input_path="XNP_snRNA.h5ad",
    output_dir="./figures/scRNA/"
)

# 查看结果
for r in results:
    print(f"Input: {r['input']}")
    print(f"Type: {r['file_type']}")
    print(f"Files: {r['generated_files']}")
```

### 示例2: 批量处理
```python
# 处理整个目录
results = system.run(
    input_path="./data/",
    output_dir="./output/all_figures/"
)
```

### 示例3: 自定义分析参数
```python
from auto_figure import AutoFigureSystem

system = AutoFigureSystem(output_dir="./output")

# 自定义处理
result = system.process_file(
    filepath="data.h5ad",
    output_dir="./custom_output/"
)
```

---

## 依赖要求

### 必需
- Python 3.8+
- matplotlib >= 3.5
- numpy >= 1.20
- pandas >= 1.3

### 可选（增强功能）
- scanpy >= 1.9 (单细胞)
- anndata >= 0.8 (单细胞)
- seaborn >= 0.11 (增强可视化)
- scipy >= 1.7 (统计方法)
- scikit-learn >= 0.24 (降维/聚类)

---

## 与路由系统集成

```python
from auto_figure import AutoFigureSystem
from bioinfo_router import generate_figure, quick_plot

# 方式1: 使用自动系统
system = AutoFigureSystem()
system.run("data.h5ad")

# 方式2: 使用路由系统（更灵活）
from bioinfo_router import generate_figure
generate_figure("scRNA", "UMAP", adata, "UMAP.svg")

# 方式3: 混合使用
from auto_figure import AutoFigureSystem
system = AutoFigureSystem()
# 自动处理
system.process_file("data.csv")
# 手动定制
generate_figure("general", "volcano", df, "volcano.svg")
```

---

## 常见问题

### Q: 如何只生成特定类型的图？
```python
from bioinfo_router import generate_figure

# 只生成UMAP
generate_figure("scRNA", "UMAP", adata, "UMAP.svg")

# 只生成热图
generate_figure("scRNA", "heatmap", adata, "heatmap.svg")
```

### Q: 如何添加自定义分析？
```python
# 修改 auto_analysis 方法
def custom_analysis(data, file_type):
    analysis = system.auto_analysis(data, file_type)
    analysis['methods'].append('custom_method')
    analysis['plots'].append('custom_plot')
    return analysis
```

### Q: 如何批量处理数百个文件？
```python
import glob

system = AutoFigureSystem(output_dir="./batch_output")
for filepath in glob.glob("./data/*.h5ad"):
    system.process_file(filepath)
```

---

## 更新日志

- 2026-08-24: 初始版本，支持单细胞和通用数据自动出图
