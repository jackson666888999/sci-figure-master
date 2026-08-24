---
name: sci-figure-master
description: >-
  超越竞品的科研绘图整合Skill。覆盖数据驱动出版级图表、AI配图提示词、Nature家族期刊流程、神经网络架构图、单细胞/多组学可视化、科研卡通机制图（代码画不了的图）。
  整合 120+ GitHub 科研绘图仓库 + K-Dense 163 科研技能中的绘图/可视化/插图模块。
  核心差异化：中文提示词优先、强制证据分级标注(*实验 †数据库 ‡预测 §文献)、反AI感控制(禁蓝紫渐变/霓虹发光/圆角卡片)、矢量SVG可编辑输出。
  触发词：画图、作图、出图、可视化、示意图、机制图、卡通图、架构图、流程图、热图、UMAP、PCA、volcano、Nature、投稿、cell、science、顶刊图、evidence、证据分级。
---

# Sci Figure Master — 科研绘图超级整合 Skill

> 目标：做一个**超越 BioRender / EZFigure / PaperBanana** 的科研绘图能力层。
> 传统工具痛点 → 本 skill 解法：
> - BioRender/EZFigure 手动拖拽 → 提示词驱动 + 模板库自动组装
> - AI绘图(MJ/DALL-E) 一眼AI感、不可编辑 → 矢量SVG输出 + 风格约束系统
> - 通用工具无证据分级 → 强制标注实验/数据库/预测来源
> - 代码绘图只能画数据图 → 机制图+数据图混合布局

## 整合来源总览

### A. 已深度整合的核心仓库（完整能力内置）
| 来源 | 仓库 | 核心能力 |
|------|------|----------|
| academic-figure-skill | TingxiYu/academic-figure-skill | 数据驱动出版级图表（29种图型，4轮QA） |
| academic-figure-generator | LigphiDonk/academic-figure-generator | AI论文配图提示词（50+配色） |
| nature-skills | Yuan1z0825/nature-skills | Nature家族期刊完整流程 |
| PaperBanana | dwzhu-pku/PaperBanana | 多智能体学术配图自动生成 |
| PlotNeuralNet | HarisIqbal88/PlotNeuralNet | LaTeX神经网络架构图 |

### B. 2025-2026 顶刊绘图代码（assets/ 本地克隆）
**从 Cell/Nature/Science 顶刊论文中克隆的公开绘图代码和工具**：

| 仓库 | GitHub | 年份 | 期刊覆盖 | 核心能力 | 本地路径 |
|------|--------|------|----------|----------|----------|
| cnsplots | faridrashidi/cnsplots | 2026 | Cell/Nature/Science | 25+图表类型、像素控制、统计检验、SVG导出 | `assets/cnsplots/` |
| figures4papers | ChenLiu-1996/figures4papers | 2025-2026 | Nature MI/ICML/NeurIPS | Nature Machine Intelligence 论文绘图脚本、LLM skill框架 | `assets/figures4papers/` |
| SciencePlots | garrettj403/SciencePlots | 2025-2026 | Nature/IEEE | matplotlib样式库、多语言支持、色盲友好配色 | `assets/SciencePlots/` |
| journal-figure-studio | Muhtasim-Munif-Fahim/journal-figure-studio | 2026 | 多期刊 | 可复现出版包生成、版本化配置、自动验证 | `assets/journal-figure-studio/` |
| Awesome-Scientific-Charts | petemeng/Awesome-Scientific-Charts | 2025-2026 | Nature系列 | R语言复现顶级期刊图表、中文注释 | `assets/Awesome-Scientific-Charts/` |
| SciVizKit | Yang1Bai/SciVizKit | 2026 | 多期刊 | 80+图表类型、Web UI交互、智能推荐决策树 | `assets/SciVizKit/` |
| PubPlotLib | pier-astro/PubPlotLib | 2025-2026 | A&A/ApJ | 天体物理学专用样式、自动列宽处理 | `assets/PubPlotLib/` |

### C. 生物信息学专用绘图工具（assets/ 本地克隆）
**覆盖全部生物信息学热门领域（15 领域 × 40+ 图型），全部本地可用，0动手开箱即用**：

| 领域 | 仓库 | 年份 | 期刊 | 语言 | 核心能力 | 本地路径 |
|------|------|------|------|------|----------|----------|
| 基因组 | GW | 2025 | Nature Methods | Python | 基因组浏览器、交互式轨道显示 | `assets/kcleal/` |
| 基因组 | pyGenomeTracks | 2023 | BMC Bioinf | Python | 基因组轨道图、ChIP/ATAC峰图 | `assets/pyGenomeTracks/` |
| 基因组 | CNVkit | 2016 | PLoS Comput Biol | Python | 拷贝数变异分析可视化 | `assets/cnvkit/` |
| 空间转录组 | SpatialVista | 2026 | Nature Methods | Python | 空间转录组可视化、spot/region标注 | `assets/spatial-vista-py/` |
| 单细胞 | PLOSC² | 2024 | PLOS Comput Biol | R | scRNA-seq分析绘图、Seurat集成 | `assets/plosc2/` |
| 单细胞 | FeatureMAP | 2026 | Nature | Python | 特征保留流形可视化、降维 | `assets/featuremap/` |
| 单细胞 | CellChat | 2021 | Nat Commun | R | 细胞通讯网络、配受体分析 | `assets/CellChat/` |
| 宏基因组 | animalcules | 2021 | Microbiome | R | 微生物组可视化、Alpha/Beta多样性 | `assets/animalcules/` |
| 宏基因组 | phyloseq | 2013 | PLoS ONE | R | 微生物组组成分析、多样性 | `assets/phyloseq/` |
| 系统发育 | ggtree | 2017 | Methods Ecol Evol | R | 系统发育树、树+热图组合 | `assets/ggtree/` |
| 表观 | ChIPseeker | 2015 | Bioinformatics | R | ChIP-seq峰注释可视化 | `assets/ChIPseeker/` |
| 代谢组 | MetaboAnalystR | 2020 | NAR | R | 代谢组通路、PLS-DA | `assets/MetaboAnalystR/` |
| 富集分析 | clusterProfiler | 2021 | Innovation | R | GO/KEGG/GSEA富集可视化 | `assets/clusterProfiler/` |
| 多组学 | MOFA2 | 2022 | Genome Biol | R | 多组学因子分析 | `assets/MOFA2/` |
| 多组学 | mixOmics | 2017 | PLoS Comput Biol | R | 多组学整合、DIABLO | `assets/mixOmics/` |
| 生存分析 | survminer | 2017 | CRAN | R | KM曲线、森林图 | `assets/survminer/` |
| 流式 | flowCore | 2009 | BMC Bioinf | R | 流式细胞术数据可视化 | `assets/flowCore/` |
| 通用热图 | ComplexHeatmap | 2016 | Bioinformatics | R | 复杂注释热图（顶刊标准） | `assets/ComplexHeatmap/` |
| 通用圈图 | circlize | 2014 | Bioinformatics | R | 圈图、和弦图、Circos | `assets/circlize/` |
| 通用火山图 | EnhancedVolcano | 2019 | Bioconductor | R | 出版级火山图 | `assets/EnhancedVolcano/` |
| 细胞成像 | JUMP Cell Painting | 2025 | Nature Methods | Python | 高内涵筛选形态图、Morphmap | `assets/jump-cellpainting-morphmap/` |

**详细集成说明**: 见 `assets/INTEGRATION.md`
**生物信息学路由配置**: 见 `assets/bioinfo_routing_config.md`
**零动手使用示例**: 见 `assets/BIOINFO_USAGE.md`
**领域覆盖清单**: 见 `assets/bioinfo_domains_checklist.md`（15 领域 × 20 场景验证矩阵）

### D. 100+ 图表类型注册表 + 无人值守出图 + ARIS 方法论（2026-08-24 新增）

| 模块 | 文件 | 能力 |
|------|------|------|
| 图表注册表 | `assets/chart_catalog.py` | **141 种图表类型**统一注册（SciVizKit 79 + bioinfo 41 + R 工具链 21），领域推荐决策树 |
| 可执行路由 | `assets/bioinfo_router.py` | 零动手路由：`generate_figure(domain, plot_type, data, path)`。**覆盖 23 领域 × 487 路由条目**（多组学/空间/流式/甲基化/免疫/癌症/WGS/蛋白/临床/药物等），新增 15 个领域 Python 函数（spatial/oncoplot/ppi/roc/calibration/dose_response 等），五级回退链（精确→模糊→跨域→图表目录→兜底），任意组合不报错 |
| 无人值守出图 | `auto_figure.py` | 用户只给文件路径 → 自动识别数据类型 → 规划统计方法/分析工具/画图工具 → 批量出图 |
| 全面数据分析 | `assets/comprehensive_analysis.py` | **StatAutopilot 统计方法自动选择器**（集成 compareGroups/scitex-stats 决策树：正态性→参数/非参数→分组数→配对性）+ 按领域跑完 ALL 标准分析模块（10 模块），产出完整分析结果库 |
| ARIS 两阶段 | `assets/aris_pipeline.py` | **Phase1 先出顶刊故事**（文献调研→提炼→9阶段故事闭环，每阶段绑定证据链）→ **用户审查** → **Phase2 围绕故事主线筛选结果+证据链出图** |
| 100+ 图表清单 | `assets/CHART_CATALOG_100.md` | 图表目录与领域推荐速查 |

**无人值守出图 + ARIS 两阶段（用户只给文件路径）**:
```bash
# 方式1: 快速出图
python auto_figure.py --input data.csv --output ./figures/

# 方式2: ARIS 两阶段（推荐）——先出故事，审查后再围绕主线出图
python aris_pipeline.py --data data.csv --topic "研究主题" --phase story --output run1
#  → 审查 run1/story.md（9 阶段故事 + 证据链设计）
python aris_pipeline.py --data data.csv --phase figures --story run1/story.json --output run1

# 方式3: 全面数据分析（StatAutopilot 自动选统计方法）
python comprehensive_analysis.py --input data.csv --output ./analysis_out/
```

**快速使用示例**:
```python
# 方式1: cnsplots（推荐）
import cnsplots as cns
cns.figure(width=200, height=150, color_cycle="Nature")
cns.boxplot(data=df, x="group", y="value", pairs=[("A", "B")])
cns.savefig("figure.svg")

# 方式2: SciencePlots（无 LaTeX 环境请先禁 usetex）
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'nature'])
plt.rcParams['text.usetex'] = False   # ← 无 LaTeX 时必加（顺序：先 style.use 后禁用）
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(x, y)
plt.savefig('figure.pdf')

# 方式3: figures4papers skill
# 见 assets/figures4papers/scientific-figure-making/SKILL.md

# 方式4: 生物信息学零动手（15 领域全自动路由）
from sci_figure_master.bioinfo import generate_figure
generate_figure(domain="scRNA", plot_type="UMAP", data=adata, output_path="UMAP.svg")
generate_figure(domain="enrichment", plot_type="dotplot", data=ego, output_path="GO.svg")
generate_figure(domain="phylogeny", plot_type="tree", data=tree, output_path="tree.svg")
generate_figure(domain="survival", plot_type="km", data=fit, output_path="KM.pdf")
# 见 assets/BIOINFO_USAGE.md（含 7 个场景完整示例）
```

### B. K-Dense 163 技能中的绘图/可视化/插图模块（按需调用）
本 skill 运行时可直接调用已安装的 K-Dense 技能（见 `references/kdense-skills.md`）：
- 可视化：`scientific-visualization`、`matplotlib`、`seaborn`
- 科研插图/幻灯片：`scientific-schematics`、`scientific-slides`、`scientific-visualization`
- 文档/海报：`pptx-posters`、`latex-posters`、`docx`、`pdf`、`xlsx`、`infographics`
- AI生图：`generate-image`（FLUX.2 Pro + Gemini）
- 图标/素材：`Figpad` 风格 SVG 编辑器思路、`bioicons` 素材库
- 领域绘图：scanpy/anndata（单细胞）、rdkit/deepchem（分子）、pyCirclize（和弦图）、ComplexHeatmap（热图）

### C. 生物信息学领域→画图工具路由（零动手）
用户只需提供领域和图型，系统自动路由（15 大领域 × 40+ 图型）：
```
用户输入: "帮我画单细胞UMAP图"
系统自动: domain="scRNA" → plot_type="UMAP" → 使用scanpy/FeatureMAP → 输出SVG/PDF

用户输入: "画微生物组Alpha多样性"
系统自动: domain="microbiome" → plot_type="alpha" → 使用animalcules → 输出SVG

用户输入: "画空间转录组可视化"
系统自动: domain="spatial" → plot_type="distribution" → 使用SpatialVista → 输出SVG

用户输入: "画GO富集气泡图"
系统自动: domain="enrichment" → plot_type="dotplot" → 使用clusterProfiler → 输出SVG

用户输入: "画系统发育树"
系统自动: domain="phylogeny" → plot_type="tree" → 使用ggtree → 输出SVG

用户输入: "画KM生存曲线"
系统自动: domain="survival" → plot_type="km" → 使用survminer → 输出PDF

用户输入: "画CNV拷贝数变异图"
系统自动: domain="genome" → plot_type="cnv" → 使用CNVkit → 输出SVG

用户输入: "画细胞通讯网络图"
系统自动: domain="scRNA" → plot_type="cellchat" → 使用CellChat → 输出SVG

用户输入: "画代谢组PLS-DA"
系统自动: domain="metabolomics" → plot_type="plsda" → 使用MetaboAnalystR → 输出SVG
```
详细路由规则见 `assets/bioinfo_routing_config.md`

### C. 120+ 科研绘图 GitHub 仓库索引（按需 clone / 参考）
完整清单见 `references/REPO_DRAWING_FULL.md`（按 16 类 + **附录：对话提及的全部 GitHub 仓库去重全量 212 个**，确保不遗漏）、`references/bioinfo_drawing_tools.md`（生信 100+ 工具深度调研，45 领域）、`references/bioinfo_70_domains.md`（**70 领域 × 完整研究过程 × 5–10 核心工具 × 画图工具**总表，含顶刊主图可视化工具速查表）、`references/bioinfo_70_domains_process.md`（**70 领域完整版**：每领域研究过程/核心工具/画图工具全量，含顶刊主图优先可视化工具总表 + 投稿/项目使用建议，不加精炼）与 `references/bioinfo_70_domains_full.md`（**完整 15 字段版**：一级领域/二级任务/推荐等级A·B·C/工具名/GitHub/官方文档/代表论文/输入/输出/主图工具/补图工具/是否适合主图/是否适合临床机制/是否适合单细胞多组学网络药理知识图谱/注意事项，覆盖全部 70 领域，不加精炼，GitHub/文档链接已全补全）。

### 领域→画图工具路由（速查）
- 领域→画图工具路由：先查 `bioinfo_70_domains_process.md` 取"画图工具"列（权威完整版）；如需快速速查看 `bioinfo_70_domains.md`。
当用户说某领域（如"单细胞"、"ChIP-seq"、"网络药理学"、"癌症基因组"），取"画图工具"列直接调用：
- 单细胞/轨迹/通讯 → Seurat/Scanpy/Monocle3/scVelo/CellChat + circlize
- 基因组浏览/表观 → IGV/JBrowse2/pyGenomeTracks/Gviz + deepTools
- 富集/通路 → clusterProfiler/enrichplot/pathview
- 网络/药理学 → Cytoscape/ggraph/igraph + PyMOL(对接)
- 蛋白结构 → PyMOL/ChimeraX/Mol*
- 系统发育 → ggtree/ETE
- 宏基因组 → phyloseq/vegan/anvi'o
- 生存/预后 → survminer/pROC
- 跨领域基础设施（任何图都可调用）：ggplot2, ComplexHeatmap, matplotlib, seaborn, SHAP, UMAP

---

## 路由协议

### Step 0: 识别任务类型
| 用户意图 | 信号 | 路由目标 |
|----------|------|----------|
| **数据驱动图表** | 提供数据+科学问题、"热图/PCA/volcano/柱状图/箱线/小提琴" | `skills/data-figure/` |
| **AI配图提示词** | "生成提示词"、"AI生图"、"架构图/流程图/示意图 prompt" | `skills/ai-prompt/` |
| **Nature投稿流程** | "投稿"、"manuscript"、"Nature/Cell/Science"、"审稿意见" | `skills/nature-figure/` |
| **神经网络图** | "神经网络"、"Transformer/CNN/U-Net 架构图" | `skills/neural-network/` |
| **单细胞/多组学** | "单细胞"、"scRNA-seq"、"UMAP"、"CellChat"、"多组学" | 调 K-Dense `scanpy`/`pyCirclize` 或 `assets/plosc2/`、`assets/CellChat/` |
| **空间转录组** | "空间转录组"、"Visium"、"Stereo-seq" | `assets/spatial-vista-py/` |
| **宏基因组** | "16S"、"微生物组"、"Alpha多样性" | `assets/animalcules/`、`assets/phyloseq/` |
| **基因组浏览器** | "基因组"、"GWAS"、"Track" | `assets/kcleal/`、`assets/pyGenomeTracks/` |
| **系统发育** | "进化树"、"系统发育"、"ggtree" | `assets/ggtree/` |
| **表观遗传** | "ChIP-seq"、"ATAC"、"甲基化"、"峰" | `assets/ChIPseeker/`、`assets/pyGenomeTracks/` |
| **富集分析** | "GO"、"KEGG"、"GSEA"、"富集" | `assets/clusterProfiler/` |
| **代谢组** | "代谢组"、"PLS-DA"、"通路" | `assets/MetaboAnalystR/` |
| **多组学整合** | "MOFA"、"多组学整合"、"DIABLO" | `assets/MOFA2/`、`assets/mixOmics/` |
| **生存分析** | "KM曲线"、"生存"、"预后"、"森林图" | `assets/survminer/` |
| **CNV** | "拷贝数"、"CNV" | `assets/cnvkit/` |
| **流式细胞术** | "流式"、"FACS"、"CyTOF" | `assets/flowCore/` |
| **通用热图/圈图** | "热图"、"圈图"、"Circos"、"和弦图" | `assets/ComplexHeatmap/`、`assets/circlize/` |
| **科研卡通机制图** | "机制图"、"卡通图"、"画不了的代码图"、"肠脑轴示意图"、"信号通路卡通" | `skills/cartoon-mechanism/` |

---

## 核心能力

### 1. 数据驱动出版级图表 (`skills/data-figure/`)
- 29种图型（热图/火山/PCA/桑基/UpSet/森林图等）
- 8步闭环 + 4轮QA，矢量优先(PDF/SVG + 300dpi PNG)
- CNS 风格配色/字体/布局

### 2. AI配图提示词 (`skills/ai-prompt/`)
- 传统学术风格 + 现代ML柔彩风格
- 8种配色（Okabe-Ito 色盲友好优先）
- 四层次提示词结构，支持 NanoBanana/Gemini/DALL-E/MJ

### 3. Nature家族流程 (`skills/nature-figure/`)
- 双路由：数据图(Python/R) + AI示意图
- 证据分级标注 + 反AI感控制 + 顶刊标准

### 4. 神经网络架构图 (`skills/neural-network/`)
- LaTeX TikZ 引擎，预置 AlexNet/VGG/UNet 模板

### 5. 科研卡通机制图 (`skills/cartoon-mechanism/`) ★ 核心差异化
**解决"代码画不了的科研卡通图"**：
- 输入：中文自然语言描述（如"画一个肠脑轴机制图，左肠右脑，中间迷走神经连接"）
- 处理：
  1. 中文提示词解析 → 结构化场景（主体/关系/证据等级）
  2. 调 `generate-image` 或 PaperBanana 生成底图
  3. 叠加 `bioicons` SVG 素材（细胞/器官/分子图标）
  4. 强制证据分级标注（*实验 †数据库 ‡预测 §文献）
  5. 反AI感后处理（去渐变/发光，转 SVG 可编辑）
- 输出：可编辑 SVG + PDF（投稿）+ PPTX（汇报）
- **卖点**：BioRender 要手动拖，这里提示词驱动；MJ 不可编辑，这里出矢量

---

## 证据分级规则（强制）
| 符号 | 含义 | 示例 |
|------|------|------|
| \* | 实验验证 | WB, qPCR, Flow |
| † | 公开数据库 | GEO, TCGA, GTEx |
| ‡ | 数据库预测 | STRING, STITCH |
| § | 文献支持 | PubMed |

## 反AI感检查清单（强制）
- [ ] 无蓝紫渐变背景 / 霓虹发光
- [ ] 无圆角卡片 / 装饰气泡
- [ ] 白底或极简背景、非对称布局
- [ ] 色盲友好配色、字体一致(Arial)
- [ ] 坐标轴仅 bottom/left、图例无黑底

---

## 项目结构
```
sci-figure-master/
├── SKILL.md                      # 本文件
├── README.md
├── skills/
│   ├── data-figure/              # 数据驱动图表
│   ├── ai-prompt/                # AI配图提示词
│   ├── nature-figure/            # Nature投稿流程
│   ├── neural-network/           # 神经网络图
│   └── cartoon-mechanism/        # ★科研卡通机制图(核心差异化)
├── assets/
│   ├── cnsplots/                 # ★2026: Cell/Nature/Science出版级绘图库(25+图表)
│   ├── figures4papers/           # ★2025-2026: Nature MI/ICML论文绘图脚本
│   ├── SciencePlots/             # ★matplotlib样式库(Nature/IEEE)
│   ├── journal-figure-studio/    # ★2026: 可复现出版包生成器
│   ├── Awesome-Scientific-Charts/# ★2025-2026: R语言顶刊图表复现
│   ├── SciVizKit/                # ★2026: 80+图表类型Web交互工具
│   ├── PubPlotLib/               # ★2025-2026: 天体物理专用样式
│   ├── gw-gw/                    # ★2025: Nature Methods 基因组浏览器
│   ├── kcleal/                   # ★GW 基因组浏览器（正式仓库）
│   ├── spatial-vista-py/         # ★2026: Nature Methods 空间转录组
│   ├── plosc2/                   # ★scRNA-seq绘图脚本(Seurat集成)
│   ├── featuremap/               # ★2026: Nature 特征保留流形
│   ├── animalcules/              # ★微生物组可视化(R)
│   ├── phyloseq/                 # ★微生物组组成/多样性(R)
│   ├── ggtree/                   # ★系统发育树(R)
│   ├── ChIPseeker/               # ★ChIP-seq峰注释(R)
│   ├── pyGenomeTracks/           # ★基因组轨道图(Python)
│   ├── cnvkit/                   # ★CNV拷贝数变异(Python)
│   ├── CellChat/                 # ★细胞通讯网络(R)
│   ├── MetaboAnalystR/           # ★代谢组分析(R)
│   ├── clusterProfiler/          # ★GO/KEGG/GSEA富集(R)
│   ├── MOFA2/                    # ★多组学因子分析(R)
│   ├── mixOmics/                 # ★多组学整合(R)
│   ├── survminer/                # ★KM生存曲线(R)
│   ├── flowCore/                 # ★流式细胞术(R)
│   ├── ComplexHeatmap/           # ★复杂注释热图(R)
│   ├── circlize/                 # ★圈图/和弦图(R)
│   ├── EnhancedVolcano/          # ★出版级火山图(R)
│   ├── jump-cellpainting-morphmap/# ★2025: Nature Methods 细胞成像
│   ├── color-palettes/           # 共享配色
│   ├── INTEGRATION.md            # 通用集成指南
│   ├── bioinfo_routing_config.md # ★生物信息学路由配置
│   └── BIOINFO_USAGE.md          # ★零动手使用示例
└── references/
    ├── REPO_DRAWING_FULL.md      # 120+仓库全量索引 + 212个对话提及仓库附录
    ├── bioinfo_drawing_tools.md   # 生信100+工具深度调研(45领域)
    ├── bioinfo_70_domains.md      # 70领域×完整研究过程×工具×画图工具总表(精简版)
    ├── bioinfo_70_domains_process.md  # 70领域×完整研究过程×核心工具×画图工具(权威完整版，含投稿建议)
    ├── bioinfo_70_domains_full.md  # 70领域×15字段完整版(不加精炼，齐全)
    ├── kdense-skills.md           # K-Dense绘图技能路由
    └── checklist.md              # QA清单
```

## 版权
整合项目保留各自许可证（academic-figure-skill Apache-2.0 / nature-skills Apache-2.0 / PaperBanana MIT-0 / PlotNeuralNet MIT / scanpy BSD-3 / ComplexHeatmap GPL-3 / K-Dense MIT）。K-Dense 技能商用须保留其 LICENSE 版权声明。

## 实时同步
本仓库实时推送到私有 GitHub: jackson666888999/sci-figure-master
