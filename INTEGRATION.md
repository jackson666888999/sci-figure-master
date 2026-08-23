# Sci Figure Master — 整合完成

## 任务状态

**已完成**：
- [x] 克隆10个核心科研绘图仓库到 E:\git
- [x] 整合到 sci-figure-master 目录
- [x] 创建主入口 SKILL.md
- [x] 创建 .gitignore 和 README.md
- [x] 初始化 git 并创建初始提交
- [ ] 推送到 GitHub（网络问题，需手动操作）

## 克隆的仓库列表

| 仓库 | GitHub | 状态 | 用途 |
|------|--------|------|------|
| academic-figure-skill | TingxiYu/academic-figure-skill | ✅ | 数据驱动图表（29种图型） |
| academic-figure-generator | LigphiDonk/academic-figure-generator | ✅ | AI配图提示词生成 |
| nature-skills | Yuan1z0825/nature-skills | ✅ | Nature家族期刊流程 |
| PaperBanana | dwzhu-pku/PaperBanana | ✅ | 多智能体学术配图 |
| plotneuralnet | kgruiz/PlotNeuralNet | ✅ | 神经网络架构图（LaTeX） |
| PlotNeuralNet | HarisIqbal88/PlotNeuralNet | ✅ | 原版神经网络图 |
| neural-network-tools | ashishpatel26/Tools-to-Design-or-Visualize-Architecture-of-Neural-Network | ✅ | 神经网络可视化 |
| scanpy | scverse/scanpy | ✅ | 单细胞分析 |
| pyCirclize | moshi4/pyCirclize | ✅ | 环形图/和弦图 |
| ComplexHeatmap | jokergoo/ComplexHeatmap | ✅ | R复杂热图 |
| SciencePlots | garrettj403/SciencePlots | ✅ | matplotlib科学样式 |

**注意**：以下仓库因网络问题克隆失败，需手动重试：
- bioicons (duerrsimon/bioicons)
- CellChat (sqjin/CellChat)
- MOFA2 (bioFAM/MOFA2)
- academic-figure-skills (Azhi-ss/academic-figure-skills)

## 整合后的项目结构

```
E:\git\sci-figure-master\
├── SKILL.md                    # 主入口：任务分发器
├── README.md                   # 项目说明
├── .gitignore
├── requirements.txt
├── skills/
│   ├── data-figure/            # 数据驱动图表（29种图型）
│   │   └── assets/             # 生产脚本和预览图
│   ├── ai-prompt/              # AI配图提示词（8种配色）
│   │   ├── SKILL.md
│   │   └── SKILL-PASTEL.md     # 现代ML柔彩风格
│   ├── nature-figure/          # Nature投稿流程
│   │   └── ...                 # 完整nature-figure技能
│   ├── neural-network/         # 神经网络图（PlotNeuralNet）
│   │   ├── layers/             # LaTeX TikZ层模板
│   │   └── pycore/             # Python API
│   └── paperbanana/            # PaperBanana多智能体
├── assets/
│   ├── color-palettes/         # SciencePlots配色
│   └── figure-atlas/           # 图表类型图例（20张）
└── references/                 # 共享参考文档
```

## 核心能力

### 1. 数据驱动图表
- 29种图型模板（热图、火山图、PCA、AUROC、桑基图等）
- 4轮QA协议（反模式扫描、代码合规、视觉逻辑、渲染验证）
- 矢量PDF/SVG输出
- CNS期刊标准

### 2. AI配图提示词
- 8种学术配色方案（Okabe-Ito、Blue、Teal+Amber等）
- 四层次提示词结构
- 支持DALL-E/Midjourney/Gemini

### 3. Nature投稿流程
- 双路由架构（数据图 vs AI示意图）
- 证据分级标注（*实验 †数据库 ‡预测 §文献）
- 反AI感控制

### 4. 神经网络图
- LaTeX TikZ引擎
- 预置模板（AlexNet、VGG、U-Net等）
- Python API可编程生成

## 使用方法

在WorkBuddy中，使用以下触发词：

| 场景 | 触发词 |
|------|--------|
| 数据图 | 画图、作图、热图、PCA、volcano、柱状图 |
| AI提示词 | 提示词、prompt、架构图、流程图、示意图 |
| Nature投稿 | Nature、投稿、manuscript、审稿意见 |
| 神经网络图 | 神经网络图、架构图、Deep Learning |
| 单细胞分析 | 单细胞、scRNA-seq、UMAP、t-SNE |

## 推送GitHub仓库

**手动推送步骤**（由于网络问题）：

```bash
# 1. 在GitHub创建私有仓库
# 仓库名: sci-figure-master

# 2. 添加远程并推送
cd E:\git\sci-figure-master
git remote add origin https://github.com/jackson666888999/sci-figure-master.git
git push -u origin main

# 或使用gh CLI
gh repo create sci-figure-master --private --source=. --push
```

## 后续任务

1. **补充克隆失败的仓库**：
   - bioicons
   - CellChat
   - MOFA2
   - academic-figure-skills

2. **完善README.md**（当前被锁定，需手动编辑）

3. **添加更多参考文档**到 `references/` 目录

4. **创建示例脚本**展示完整工作流

5. **推送到GitHub**（网络恢复后执行）

## 技术栈

- **Python**: matplotlib, seaborn, scanpy, numpy, pandas
- **R**: ComplexHeatmap, ggplot2, patchwork, circlize
- **LaTeX**: TikZ（神经网络图）
- **AI**: OpenRouter, Gemini, DALL-E

## 版权说明

保留各源仓库的许可证声明：
- academic-figure-skill: Apache-2.0
- academic-figure-generator: MIT
- nature-skills: Apache-2.0
- PaperBanana: MIT-0
- PlotNeuralNet: MIT
- SciencePlots: BSD-3

---

**整合完成时间**: 2026-08-23  
**整合者**: WorkBuddy + Senior Developer  
**源仓库**: https://github.com/TingxiYu/academic-figure-skill, https://github.com/LigphiDonk/academic-figure-generator, https://github.com/Yuan1z0825/nature-skills, https://github.com/dwzhu-pku/PaperBanana
