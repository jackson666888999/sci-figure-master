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

### B. K-Dense 163 技能中的绘图/可视化/插图模块（按需调用）
本 skill 运行时可直接调用已安装的 K-Dense 技能（见 `references/kdense-skills.md`）：
- 可视化：`scientific-visualization`、`matplotlib`、`seaborn`
- 科研插图/幻灯片：`scientific-schematics`、`scientific-slides`、`scientific-visualization`
- 文档/海报：`pptx-posters`、`latex-posters`、`docx`、`pdf`、`xlsx`、`infographics`
- AI生图：`generate-image`（FLUX.2 Pro + Gemini）
- 图标/素材：`Figpad` 风格 SVG 编辑器思路、`bioicons` 素材库
- 领域绘图：scanpy/anndata（单细胞）、rdkit/deepchem（分子）、pyCirclize（和弦图）、ComplexHeatmap（热图）

### C. 120+ 科研绘图 GitHub 仓库索引（按需 clone / 参考）
完整清单见 `references/REPO_DRAWING_FULL.md`（按 16 类：综合平台、神经网络、单细胞、基因组、表观、蛋白、微生物、系统生物、癌症、进化、R库、Python库、AI配图、图标素材、3D动画、其他）。

---

## 路由协议

### Step 0: 识别任务类型
| 用户意图 | 信号 | 路由目标 |
|----------|------|----------|
| **数据驱动图表** | 提供数据+科学问题、"热图/PCA/volcano/柱状图/箱线/小提琴" | `skills/data-figure/` |
| **AI配图提示词** | "生成提示词"、"AI生图"、"架构图/流程图/示意图 prompt" | `skills/ai-prompt/` |
| **Nature投稿流程** | "投稿"、"manuscript"、"Nature/Cell/Science"、"审稿意见" | `skills/nature-figure/` |
| **神经网络图** | "神经网络"、"Transformer/CNN/U-Net 架构图" | `skills/neural-network/` |
| **单细胞/多组学** | "单细胞"、"scRNA-seq"、"UMAP"、"CellChat"、"多组学" | 调 K-Dense `scanpy`/`pyCirclize` |
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
├── assets/color-palettes/        # 共享配色
└── references/
    ├── REPO_DRAWING_FULL.md      # 120+仓库全量索引
    ├── kdense-skills.md           # K-Dense绘图技能路由
    └── checklist.md              # QA清单
```

## 版权
整合项目保留各自许可证（academic-figure-skill Apache-2.0 / nature-skills Apache-2.0 / PaperBanana MIT-0 / PlotNeuralNet MIT / scanpy BSD-3 / ComplexHeatmap GPL-3 / K-Dense MIT）。K-Dense 技能商用须保留其 LICENSE 版权声明。

## 实时同步
本仓库实时推送到私有 GitHub: jackson666888999/sci-figure-master
