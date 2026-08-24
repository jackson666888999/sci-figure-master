# ARIS 两阶段工作流：先出顶刊故事，再围绕主线出图

> 版本: 2026-08-24 | 核心文件: `assets/aris_pipeline.py` + `assets/comprehensive_analysis.py`

## 工作流

```
用户只给文件路径
      │
      ▼
┌─ Phase 1: 全面数据分析（comprehensive_analysis.py）─────────┐
│  · StatAutopilot 自动选统计方法（决策树）                    │
│  · 按领域跑完 ALL 标准分析（10 模块，多领域自动叠加）        │
│  · 产出: analysis_summary.json + results/*.csv               │
└───────────────────────────────────────────────────────────────┘
      │
      ▼
┌─ Phase 1: 顶刊级故事生成（ARIS）─────────────────────────────┐
│  · Acquire: 真实顶刊文献调研（Crossref/arXiv，绝不虚构）     │
│  · Review: 提炼研究方法/范式/写作/创新/画图代码/数据来源      │
│  · Integrate: 9 阶段故事闭环，每阶段绑定证据链               │
│     （分析模块 → 图形 → 统计支撑 → 结果文件）                │
│  · Score: 严格评审（100 分制）                               │
│  产出: story.md + story.json  ←── 用户审查/修改              │
└───────────────────────────────────────────────────────────────┘
      │  用户确认故事
      ▼
┌─ Phase 2: 故事驱动证据链出图 ────────────────────────────────┐
│  · 只取故事证据链命中的分析结果（筛选）                      │
│  · 图形紧紧围绕文章主线，每张图对应故事阶段+分析模块         │
│  产出: figures/*.svg（如 S6_differential_volcano.svg）        │
│        evidence_chain.md                                     │
└───────────────────────────────────────────────────────────────┘
```

## 用法

```bash
# 完整流程（故事 + 出图）
python assets/aris_pipeline.py --data 你的数据.csv --topic "主题" --phase full --output run1

# 分阶段（推荐）：先出故事给用户审查
python assets/aris_pipeline.py --data 你的数据.csv --topic "主题" --phase story --output run1
#  → 打开 run1/story.md 审查 9 阶段故事与证据链
#  → 用户修改 story.json 后可重新出图

# 审查后：围绕故事主线出图
python assets/aris_pipeline.py --data 你的数据.csv --phase figures --story run1/story.json --output run1
```

## StatAutopilot 统计方法自动选择（决策树）

| 条件 | 自动选择 |
|------|----------|
| 1 组 连续 + 正态 | one-sample t |
| 1 组 连续 + 非正态 | Wilcoxon signed-rank |
| 2 组 连续 + 双正态 + 方差齐 | Student t |
| 2 组 连续 + 双正态 + 方差不齐 | Welch t |
| 2 组 连续 + 非正态 | Mann-Whitney U |
| 2 组 配对 + 正态 | paired t |
| 2 组 配对 + 非正态 | Wilcoxon signed-rank |
| ≥3 组 + 全正态 + 方差齐 | ANOVA (+ η²) |
| ≥3 组 + 全正态 + 方差不齐 | Welch ANOVA |
| ≥3 组 + 非正态 | Kruskal-Wallis (+ ε²) |
| 分类结局 | χ² / Fisher exact |
| 相关分析 | 双正态 → Pearson；否则 Spearman |
| 多重比较 | Benjamini-Hochberg FDR |

同款逻辑来源（真实工具）: R `compareGroups`（JSS 2014）、Python `scitex-stats`（recommend_tests）、R `automatedtests`。

## 证据链设计（故事阶段 → 图形）

| 阶段 | 分析模块 | 图形 |
|------|----------|------|
| S1 Background | descriptive | histogram, boxplot |
| S2 Gap | normality, correlation | qqplot, corr_heatmap, scatter |
| S3 Hypothesis | dim_reduction, clustering | pca, dendrogram |
| S5 Results-Layer1 | descriptive, dim_reduction, clustering | boxplot, pca, dendrogram |
| S6 Results-Layer2 | group_comparison, differential | boxplot, violin, volcano, ma_plot |
| S7 Results-Layer3 | correlation, composition, alpha | corr_heatmap, scatter, stacked_bar |
| S8 Validation | differential | volcano, ma_plot |

## 数据红线
- 文献 API 不可用时**绝不编造**文献，明确提示
- 画图**仅使用用户提供的真实数据文件**
- 全面分析结果全部可复现（代码 + 数据路径 + 随机种子）
