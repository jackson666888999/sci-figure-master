# Sci Figure Master — 科研绘图整合 Skill

本 skill 整合了三个顶级科研绘图开源仓库的核心能力：

| 来源 | 仓库 | 核心能力 |
|------|------|----------|
| academic-figure-skill | TingxiYu/academic-figure-skill | 数据驱动的出版级科学图表生成 |
| academic-figure-generator | LigphiDonk/academic-figure-generator | AI 学术论文配图提示词生成 |
| nature-skills | Yuan1z0825/nature-skills | Nature 家族期刊图表演示与完整论文工作流 |

## 整合后的 Skill 结构

```
sci-figure-master/
├── README.md                  # 本文件：整合说明
├── SKILL.md                   # 主入口：任务分发器
├── .gitignore
├── assets/                    # 共享资源
│   ├── color-palettes/        # 配色方案
│   ├── figure-atlas/          # 图表类型图例
│   └── templates/             # 模板文件
├── skills/                    # 子 skill（从各源仓库提取）
│   ├── data-figure/           # 从 academic-figure-skill 提取
│   ├── ai-prompt/             # 从 academic-figure-generator 提取
│   └── nature-figure/         # 从 nature-skills 提取
├── src/                       # 共享 Python 工具
│   ├── quality_check.py       # 质量检查
│   ├── color_validator.py     # 配色验证
│   └── export_validator.py    # 导出格式验证
└── references/                # 共享参考文档
    ├── typography.md
    ├── journal-specs.md
    ├── export-specs.md
    └── checklist.md
```

## 使用指南

### 场景一：数据驱动的出版级图表
**触发词**：画图、作图、出图、可视化、柱状图、热图、PCA、volcano plot、图、Figure X

→ 使用 `skills/data-figure/` 中的逻辑
→ 输入：数据文件 + 科学问题
→ 输出：符合 Nature/Cell/Science 标准的 PDF/PNG

### 场景二：AI 生图提示词
**触发词**：提示词、prompt、示意图、架构图、流程图、概念图、图提示词

→ 使用 `skills/ai-prompt/` 中的逻辑
→ 输入：论文内容/概念描述
→ 输出：适合 DALL-E/Midjourney/Gemini 的详细英文提示词

### 场景三：Nature 家族期刊完整流程
**触发词**：投稿、manuscript、Nature、Cell、Science、投稿指南、修改回复

→ 使用 `skills/nature-figure/` 中的逻辑
→ 覆盖：数据整理、图表生成、写作润色、投稿材料准备

---

**版权说明**：本整合 skill 保留了各源仓库的 MIT 许可证声明。
