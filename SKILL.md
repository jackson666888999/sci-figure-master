---
name: sci-figure-master
description: >-
  整合三个顶级科研绘图仓库的通用科研绘图Skill。支持：数据驱动出版级图表、AI配图提示词生成、Nature家族期刊完整流程、神经网络架构图、单细胞分析可视化。
  触发词：画图、作图、出图、可视化、图、Figure、提示词、prompt、示意图、架构图、流程图、单细胞、热图、PCA、volcano、Nature、投稿、cell、science。
  整合来源：academic-figure-skill、academic-figure-generator、nature-skills、PaperBanana。
---

# Sci Figure Master — 科研绘图整合Skill

本Skill整合了以下四个顶级科研绘图开源仓库的核心能力：

| 来源 | 仓库 | 核心能力 |
|------|------|----------|
| academic-figure-skill | TingxiYu/academic-figure-skill | 数据驱动的出版级科学图表生成（29种图型，4轮QA） |
| academic-figure-generator | LigphiDonk/academic-figure-generator | AI学术论文配图提示词生成（50+配色方案） |
| nature-skills | Yuan1z0825/nature-skills | Nature家族期刊图表演示与完整论文工作流 |
| PaperBanana | dwzhu-pku/PaperBanana | 多智能体学术配图自动生成 |

## 路由协议

当用户请求科研绘图时，按以下步骤路由：

### Step 0: 识别任务类型

| 用户意图 | 信号 | 路由目标 |
|----------|------|----------|
| **数据驱动图表** | "画个热图"、"PCA图"、"volcano plot"、"柱状图"、"提供数据+科学问题" | `skills/data-figure/` |
| **AI配图提示词** | "生成提示词"、"AI生图"、"架构图"、"流程图"、"示意图"、"论文配图prompt" | `skills/ai-prompt/` |
| **Nature投稿流程** | "投稿"、"manuscript"、"Nature/Cell/Science"、"审稿意见" | `skills/nature-figure/` |
| **神经网络图** | "神经网络图"、"架构图"、"Deep Learning"、"Transformer"、"CNN" | `skills/neural-network/` |
| **单细胞分析** | "单细胞"、"scRNA-seq"、"UMAP"、"t-SNE"、"CellChat" | `skills/single-cell/` |

---

## 核心能力概览

### 1. 数据驱动出版级图表 (`skills/data-figure/`)

**来源**: academic-figure-skill

- **29种图型**: 热图、火山图、柱状图、散点图、箱线图、PCA、RDA、雷达图、桑基图、AUROC、山脊图、小提琴图、边际密度、核密度、Mantel相关、UpSet、森林图、混淆矩阵、流形、堆叠柱散、配对箱线、标记基因点图、趋势线、3D热图、频率热图、密度热图、相关矩阵、分组相关矩阵、分组小提琴
- **8步闭环工作流**: 用户意图解析 → 原型分类 → 图型论证 → 环境探测 → 风格注入 → 资产检索 → 渲染生成 → 质量验证
- **4轮QA协议**: 反模式扫描 → 代码级合规 → 视觉逻辑检查 → 渲染输出验证
- **矢量优先**: PDF/SVG输出，300dpi PNG预览
- **CNS期刊标准**: Nature/Cell/Science风格配色、字体、布局

**工作流**:
```
用户请求 → 科学问题澄清 → 数据解析 → 图型推荐 → 用户确认 → 环境检测 → 风格注入 → 脚本执行 → QA验证 → 输出
```

### 2. AI配图提示词生成 (`skills/ai-prompt/`)

**来源**: academic-figure-generator

- **两种风格**: 
  - 传统学术风格 (academic-figure-prompt): Nature/Science/CVPR风格，信息密度高
  - 现代ML柔彩风格 (academic-figure-prompt-pastel): ICLR/NeurIPS/ICML 2024-2025风格，圆角友好字体
- **8种配色方案**: Okabe-Ito学术标准、Blue单色系、Teal+Amber、Navy+Coral、Slate+Violet、Forest+Gold、Minimal Grey、自定义
- **四层次提示词结构**: 全局描述 → 分区详细 → 全局标注 → 风格规格
- **支持工具**: NanoBanana、Gemini、DALL-E、Midjourney

**工作流**:
```
论文内容理解 → 配色方案选择 → 提示词生成 → 迭代优化
```

### 3. Nature家族期刊完整流程 (`skills/nature-figure/`)

**来源**: nature-skills

- **双路由架构**: 
  - 数据驱动图表 (Python matplotlib/seaborn 或 R ggplot2/ComplexHeatmap)
  - AI生成示意图 (OpenRouter GPT Image 2)
- **证据分级标注**: *实验验证、†公开数据、‡数据库预测、§文献支持
- **反AI感控制**: 禁止蓝紫渐变、霓虹发光、圆角卡片
- **顶刊标准**: Nature/Cell/Science投稿要求、字数限制、源数据合同

**工作流**:
```
任务识别 → 路由选择 → 后端选择 → 契约编写 → 图表生成 → QA检查 → 输出
```

### 4. 神经网络架构图 (`skills/neural-network/`)

**来源**: PlotNeuralNet、neural-network-tools

- **LaTeX TikZ引擎**: 生产级神经网络架构图
- **预置模板**: AlexNet、VGG16、LeNet、U-Net、HED、FCN等
- **Python API**: 可编程生成复杂网络结构
- **输出格式**: PDF（矢量）、PNG（光栅）

**使用**:
```python
from pycore.tikzeng import *
def architecture():
    return [
        to_head('..'),
        to_cor(),
        to_input('input.png'),
        to_block('conv1', 'conv32x3'),
        to_connection('input', 'conv1'),
        to_end()
    ]
```

### 5. 单细胞分析可视化 (`skills/single-cell/`)

**来源**: scanpy、ComplexHeatmap、CellChat、pyCirclize

- **核心工具**: Scanpy (Python)、Seurat (R)
- **可视化**: UMAP/t-SNE、热图、小提琴图、桑基图、网络图
- **细胞通讯**: CellChat、NicheNet
- **多组学整合**: MOFA2、mixOmics

---

## 使用示例

### 示例1: 数据驱动的热图

```
用户: "我有表达矩阵数据，想画一个热图展示差异基因表达"

系统:
1. 路由到 skills/data-figure/
2. 解析数据格式
3. 推荐图型: 密度热图 + 聚类
4. 执行脚本: plot_DensityHeatmap.R
5. 输出: PDF矢量图 + 300dpi PNG
```

### 示例2: AI生成架构图提示词

```
用户: "帮我生成一个Transformer架构的论文配图提示词"

系统:
1. 路由到 skills/ai-prompt/
2. 展示8种配色方案供选择
3. 生成四层次提示词:
   - Global: "A highly detailed transformer architecture diagram..."
   - Sections: Encoder, Decoder, Attention Mechanism...
   - Annotations: Dimensions, formulas...
   - Style: Okabe-Ito palette...
4. 输出: 英文提示词（可直接用于Midjourney/DALL-E）
```

### 示例3: Nature风格多面板图

```
用户: "根据我的单细胞数据，生成一张Nature风格的Figure 1"

系统:
1. 路由到 skills/nature-figure/
2. 选择Python后端
3. 编写Figure契约:
   - Panel (a): UMAP聚类， hero panel
   - Panel (b): 差异基因热图
   - Panel (c): 细胞类型注释柱状图
4. 执行脚本，生成PDF
5. QA检查: 反AI感、配色、字体、统计标注
6. 输出: Nature风格多面板图
```

---

## 证据分级规则

所有图表必须标注证据来源：

| 符号 | 含义 | 示例 |
|------|------|------|
| \* | 实验验证 | Western blot, qPCR, Flow cytometry |
| † | 公开数据库 | GEO, TCGA, GTEx |
| ‡ | 数据库预测 | STRING, STITCH, ChIP-Atlas |
| § | 文献支持 | PubMed引用 |

---

## 反AI感检查清单

生成图表后必须检查：

- [ ] 无蓝紫渐变背景
- [ ] 无霓虹发光效果
- [ ] 无圆角卡片式布局
- [ ] 无装饰性气泡/点缀
- [ ] 白底或极简背景
- [ ] 非对称布局（Nature风格）
- [ ] 色盲友好配色
- [ ] 字体一致（Arial/Helvetica）
- [ ] 坐标轴仅保留bottom/left
- [ ] 图例无黑色背景

---

## 项目结构

```
sci-figure-master/
├── SKILL.md                      # 本文件：主入口
├── README.md                     # 项目说明
├── .gitignore
├── skills/
│   ├── data-figure/              # 数据驱动图表（来自academic-figure-skill）
│   │   ├── SKILL.md
│   │   └── assets/               # 生产脚本和预览图
│   ├── ai-prompt/                # AI配图提示词（来自academic-figure-generator）
│   │   ├── SKILL.md
│   │   └── SKILL-PASTEL.md       # 现代ML柔彩风格
│   ├── nature-figure/            # Nature投稿流程（来自nature-skills）
│   │   └── ...                   # 完整nature-figure技能
│   ├── neural-network/           # 神经网络图（来自PlotNeuralNet）
│   │   └── tikzeng.py            # Python API
│   └── single-cell/              # 单细胞分析（来自scanpy等）
│       └── ...
├── assets/
│   ├── color-palettes/           # 共享配色方案
│   └── figure-atlas/             # 图表类型图例
└── references/
    ├── typography.md             # 字体规范
    ├── journal-specs.md          # 期刊要求
    └── checklist.md              # 质量检查清单
```

---

## 版权说明

本Skill整合了以下开源项目，保留各自许可证：

- academic-figure-skill: Apache-2.0
- academic-figure-generator: MIT
- nature-skills: Apache-2.0
- PaperBanana: MIT-0
- PlotNeuralNet: MIT
- scanpy: BSD-3
- ComplexHeatmap: GPL-3

---

## 快速开始

### 安装依赖

```bash
# Python包
pip install matplotlib seaborn scanpy complexheatmap pyCirclize

# R包（可选）
# install.packages(c("ComplexHeatmap", "ggplot2", "patchwork"))

# 神经网络图（可选）
# 需要TeX Live或MiKTeX
```

### 使用方式

1. 复制本Skill目录到WorkBuddy skills目录
2. 在对话中提及触发词，如"画图"、"提示词"
3. 系统自动路由到对应子Skill
4. 按子Skill指引完成任务

---

**整合完成时间**: 2026-08-23  
**整合者**: WorkBuddy + Senior Developer  
**源仓库**: 
- https://github.com/TingxiYu/academic-figure-skill
- https://github.com/LigphiDonk/academic-figure-generator
- https://github.com/Yuan1z0825/nature-skills
- https://github.com/dwzhu-pku/PaperBanana
