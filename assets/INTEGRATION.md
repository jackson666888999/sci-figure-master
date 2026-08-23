# 2025-2026 顶刊绘图代码克隆集成

> 集成日期：2026-08-23
> 用途：将 Cell/Nature/Science 等顶刊的公开绘图代码和工具克隆到此 assets 目录，供 sci-figure-master skill 使用

---

## 已克隆仓库清单

### 1. cnsplots (2025-2026)
- **仓库**: https://github.com/faridrashidi/cnsplots
- **作者**: Farid Rashidi
- **许可证**: BSD 3-Clause
- **核心能力**: 
  - 专为 Cell/Nature/Science 期刊设计的出版级绘图库
  - 25+ 图表类型（箱线图、小提琴图、火山图、桑基图、UpSet图等）
  - 像素级尺寸控制（完美适配期刊投稿要求）
  - SVG/PDF 矢量导出，Adobe Illustrator 友好
  - 内置统计检验（Mann-Whitney U、Welch's t-test等）
  - 多面板自动标签（A, B, C...）
- **关键特性**:
  ```python
  import cnsplots as cns
  
  # Nature 风格配色
  cns.figure(width=200, height=150, color_cycle="Nature")
  cns.boxplot(data=df, x="group", y="value", pairs=[("A", "B")])
  cns.savefig("figure.svg")
  ```
- **依赖**: Python ≥3.10, matplotlib, numpy, pandas, seaborn
- **文档**: https://cnsplots.farid.one/
- **本地路径**: `assets/cnsplots/`

---

### 2. figures4papers (2025-2026)
- **仓库**: https://github.com/ChenLiu-1996/figures4papers
- **作者**: Chen Liu (Yale CS PhD)
- **许可证**: MIT
- **核心能力**:
  - 已发表在 Nature Machine Intelligence、ICML、NeurIPS、ECCV 的实际绘图脚本
  - 完整的 LLM skill 集成框架
  - 模块化绘图函数（bar plot、radar plot、trend plot等）
  - 可复用的设计理论和 API 约定
- **关键特性**:
  - 提供完整的 scientific-figure-making skill 框架
  - 每个 figure_* 文件夹包含独立项目脚本
  - 内置设计理论文档（design-theory.md）
- **集成方式**:
  ```bash
  # 作为 skill 链接到 WorkBuddy
  ln -s "E:/git/sci-figure-master/assets/figures4papers/scientific-figure-making" ~/.workbuddy/skills/
  ```
- **本地路径**: `assets/figures4papers/`

---

### 3. SciencePlots (活跃维护)
- **仓库**: https://github.com/garrettj403/SciencePlots
- **作者**: John D. Garrett
- **许可证**: MIT
- **核心能力**:
  - matplotlib 样式库，专为科学论文设计
  - 内置 Nature、IEEE 等期刊专用样式
  - 支持多种语言（中、日、韩、俄、土耳其）
  - 色盲友好配色方案
- **关键特性**:
  ```python
  import matplotlib.pyplot as plt
  import scienceplots
  
  # Nature 风格
  plt.style.use(['science', 'nature'])
  
  # IEEE 风格
  plt.style.use(['science', 'ieee'])
  
  # 色盲友好配色
  plt.style.use(['science', 'bright'])
  ```
- **依赖**: matplotlib ≥3.3, LaTeX（可选）
- **本地路径**: `assets/SciencePlots/`

---

### 4. journal-figure-studio (2025-2026)
- **仓库**: https://github.com/Muhtasim-Munif-Fahim/journal-figure-studio
- **作者**: Muhtasim-Munif-Fahim
- **许可证**: MIT
- **核心能力**:
  - 可复现的出版级图表包生成工具
  - 版本化配置文件注册表
  - 自动生成完整的出版包（数据+代码+元数据+验证）
  - 支持多种期刊风格配置
- **关键特性**:
  - 每个图表生成自包含的 publication package
  - 包含 figure_metadata.json（SHA-256、尺寸、软件版本）
  - 自动导出 PDF + PNG + TIFF
  - 可复现的渲染配方
- **依赖**: Python ≥3.10
- **本地路径**: `assets/journal-figure-studio/`

---

### 5. Awesome-Scientific-Charts (2025-2026)
- **仓库**: https://github.com/petemeng/Awesome-Scientific-Charts
- **作者**: petemeng
- **许可证**: MIT
- **核心能力**:
  - 复现顶级期刊（Nature、Science、Cell等）出版级图表
  - 每个项目包含完整可运行代码和数据
  - 详细的中文注释和说明
- **关键特性**:
  - R 语言为主（ggplot2 + patchwork + ggtree）
  - 涵盖热图、进化树、火山图、桑基图等
  - 可直接运行复现论文中的图表
- **本地路径**: `assets/Awesome-Scientific-Charts/`

---

### 6. SciVizKit (2026)
- **仓库**: https://github.com/Yang1Bai/SciVizKit
- **作者**: Yang1Bai
- **许可证**: MIT
- **核心能力**:
  - 基于 Streamlit 的交互式科研可视化工具
  - 80+ 图表类型，覆盖 10 大类别
  - 智能图表推荐决策树
  - 一键复制 Python 代码
- **关键特性**:
  - Web UI 交互探索（无需编码）
  - 期刊配色方案（Nature、Science、Cell、ACS）
  - 多面板图组装工具
  - 支持 CSV/Excel 数据上传
- **依赖**: Python ≥3.10, streamlit, matplotlib, seaborn
- **本地路径**: `assets/SciVizKit/`

---

### 7. PubPlotLib (2025-2026)
- **仓库**: https://github.com/pier-astro/PubPlotLib
- **作者**: pier-astro
- **许可证**: GPL-3.0
- **核心能力**:
  - 天体物理学期刊专用样式（A&A、ApJ等）
  - 简化 matplotlib 出版级图表创建
  - 自动处理列宽和字体大小
- **关键特性**:
  ```python
  import pubplotlib as pplt
  
  # A&A 期刊风格
  pplt.style.use('aanda')
  fig, ax = pplt.subplots()
  pplt.set_ticks(ax)
  pplt.set_formatter(ax)
  ```
- **依赖**: matplotlib ≥3.2
- **本地路径**: `assets/PubPlotLib/`

---

## 集成使用指南

### 方式 1：直接调用 Python 脚本
```python
# 使用 cnsplots
import sys
sys.path.insert(0, 'E:/git/sci-figure-master/assets/cnsplots')
import cnsplots as cns

cns.figure(width=200, height=150, color_cycle="Nature")
cns.boxplot(data=df, x="group", y="value")
cns.savefig("output.svg")
```

### 方式 2：导入样式文件
```python
# 使用 SciencePlots
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, 'E:/git/sci-figure-master/assets/SciencePlots')
import scienceplots

plt.style.use(['science', 'nature'])
fig, ax = plt.subplots(figsize=(3.5, 2.5))
# ... 绘图代码 ...
plt.savefig('figure.pdf')
```

### 方式 3：使用 figure4papers skill
```bash
# 链接 skill 到 WorkBuddy
ln -s "E:/git/sci-figure-master/assets/figures4papers/scientific-figure-making" \
      "~/.workbuddy/skills/scientific-figure-making"
```

---

## 仓库对比表

| 仓库 | 语言 | 期刊覆盖 | 特殊功能 | 最佳适用 |
|------|------|----------|----------|----------|
| cnsplots | Python | Cell/Nature/Science | 像素控制、统计检验 | 通用出版级图表 |
| figures4papers | Python | Nature MI/ICML/NeurIPS | LLM skill框架 | AI/ML论文图表 |
| SciencePlots | Python | Nature/IEEE | 多语言支持 | 快速样式应用 |
| journal-figure-studio | Python | 多期刊 | 可复现包生成 | 完整出版流程 |
| Awesome-Scientific-Charts | R | Nature系列 | 中文注释 | R用户复现 |
| SciVizKit | Python | 多期刊 | Web UI交互 | 交互式探索 |
| PubPlotLib | Python | A&A/ApJ | 天体物理专用 | 天文数据可视化 |

---

## 安装依赖

```bash
# 进入 sci-figure-master 目录
cd E:\git\sci-figure-master

# 安装所有 assets 中的 Python 包
cd assets/cnsplots && pip install -e .
cd ../figures4papers && pip install -e .
cd ../SciVizKit && pip install -r requirements.txt
cd ../PubPlotLib && pip install -e .

# 全局安装常用样式库
pip install scienceplots
```

---

## 更新说明

- **2026-08-23**: 初始克隆，集成 7 个顶刊绘图代码仓库
- 所有仓库使用 `--depth=1` 浅克隆，减少磁盘占用
- 保留完整许可证和引用信息

---

## 引用

如果使用了上述工具，请引用原始仓库：

```bibtex
@software{cnsplots,
  author = {Rashidi, Farid},
  title = {cnsplots: Publication-Ready Scientific Plots},
  year = {2026},
  url = {https://github.com/faridrashidi/cnsplots}
}

@software{garrettj403,
  author = {John D. Garrett},
  title = {SciencePlots},
  year = {2021},
  doi = {10.5281/zenodo.4106649}
}
```
