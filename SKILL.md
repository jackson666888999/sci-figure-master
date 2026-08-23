---
name: sci-figure-master
description: >-
  科研绘图统一入口。根据用户请求类型自动分发到三个子 skill：
  1. data-figure — 数据驱动的出版级科学图表（柱状图、热图、PCA、volcano 等）
  2. ai-prompt — AI 生图提示词生成（架构图、流程图、示意图）
  3. nature-figure — Nature 家族期刊图表演示与完整论文工作流
  触发词：画图、作图、出图、可视化、图表、柱状图、热图、PCA、volcano、提示词、
  prompt、示意图、架构图、流程图、概念图、Nature、Cell、Science、投稿、论文配图。
  非触发词：交互式仪表板（Plotly/Bokeh/Altair）、探索性数据分析、数学函数图、
  饼图/3D 图、PPT、Illustrator/Figma 设计、统计分析、数据清洗、文献综述。
---

# Sci Figure Master — 任务分发器

## Step 0: 任务分类

接收用户请求后，首先判断任务类型：

| 用户意图 | 信号 | 分发目标 |
|---------|------|---------|
| 根据数据画图 | "画个热图"、"Make a volcano plot"、"可视化这个数据"、提供 CSV/Excel + 科学问题 | `skills/data-figure/` |
| 生成 AI 提示词 | "生成提示词"、"提示词"、"prompt"、"架构图"、"流程图"、"示意图" | `skills/ai-prompt/` |
| Nature 投稿全流程 | "Nature 投稿"、"Nature 格式"、"投稿材料"、"manuscript figure" | `skills/nature-figure/` |
| 通用科研绘图 | "论文配图"、"学术图表"、"scientific figure" | 根据是否有数据决定 |

## Step 1: 分发逻辑

```
用户请求
    │
    ├── 有数据 + 有科学问题 → data-figure skill
    │
    ├── 无数据 + 要 AI 生图 → ai-prompt skill
    │
    ├── Nature/Cell/Science 投稿 → nature-figure skill
    │
    └── 混合请求 → 先确认优先级，再按顺序执行
```

## Step 2: 执行规则

### 数据驱动图表 (data-figure)

1. 先问：你想从数据中学到什么？（科学问题）
2. 如果没有数据，询问数据格式和位置
3. 根据数据特征和科学问题，推荐图表类型
4. 加载配色和字体模板
5. 生成代码，执行，QA 检查
6. 输出 PDF 主文件 + 300dpi PNG 预览

### AI 提示词 (ai-prompt)

1. 理解论文/概念内容
2. 先展示配色方案供选择
3. 生成详细英文提示词（包含四个层次）
4. 提供质量检查清单

### Nature 投稿 (nature-figure)

1. 确认目标期刊
2. 选择 Python 或 R 后端
3. 加载 figure contract 和 stance
4. 按多面板证据架构组织图表
5. QA 检查后交付

---

**来源仓库**：
- academic-figure-skill: https://github.com/TingxiYu/academic-figure-skill (MIT)
- academic-figure-generator: https://github.com/LigphiDonk/academic-figure-generator (MIT)
- nature-skills: https://github.com/Yuan1z0825/nature-skills (MIT)
