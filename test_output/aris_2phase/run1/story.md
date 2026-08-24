# gut microbiome treatment study

- 领域: `survival` | 范式: `clinical-survival`
- 文献支撑: 5 篇（仅真实 API 返回）

## 故事主线（层层递进闭环）
### S1 Background: 领域背景与已知
> 领域共识是什么？（需真实文献支撑）

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| descriptive | `descriptive` | histogram, boxplot | results/descriptive.csv |
  - 关键发现: gene_A (p=n/a)
  - 关键发现: gene_B (p=n/a)

### S2 Gap: 未解之谜
> 数据中哪些模式尚未被解释？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| normality | `normality` | qqplot, histogram | results/normality.csv |
  - 关键发现: event (p=1.00e-13)
  - 关键发现: time (p=3.43e-02)
| correlation | `correlation` | corr_heatmap, scatter, bubble | results/correlation.csv |
  - 关键发现: gene_A (p=1.11e-43)
  - 关键发现: gene_B (p=1.01e-01)

### S3 Hypothesis: 研究假设
> 基于数据全局模式的假设？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| dim_reduction | `dim_reduction` | pca, scatter, umap | results/dim_reduction.csv |
  - 关键发现:  (p=n/a)
| clustering | `clustering` | dendrogram, scatter | results/clustering.csv |
  - 关键发现:  (p=n/a)

### S4 Methods: 方法学
> 统计/工具/数据来源？（成对声明）

（本阶段由故事驱动，无直接分析模块）

### S5 Results-Layer1: 数据质量与全局结构
> 数据整体结构如何？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| descriptive | `descriptive` | histogram, boxplot | results/descriptive.csv |
  - 关键发现: gene_A (p=n/a)
  - 关键发现: gene_B (p=n/a)
| dim_reduction | `dim_reduction` | pca, scatter, umap | results/dim_reduction.csv |
  - 关键发现:  (p=n/a)
| clustering | `clustering` | dendrogram, scatter | results/clustering.csv |
  - 关键发现:  (p=n/a)

### S6 Results-Layer2: 组间差异与关键分子
> 哪些变量在组间显著差异？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| group_comparison | `group_comparison` | boxplot, violin, raincloud | results/group_comparison.csv |
  - 关键发现: gene_A (p=6.48e-23)
  - 关键发现: biomarker (p=1.89e-21)
| differential | `differential` | volcano, ma_plot, heatmap, lollipop | results/differential.csv |
  - 关键发现: biomarker (p=2.22e-20)
  - 关键发现: gene_A (p=2.47e-20)

### S7 Results-Layer3: 关联与机制
> 变量间如何关联，形成机制网络？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| correlation | `correlation` | corr_heatmap, scatter, bubble | results/correlation.csv |
  - 关键发现: gene_A (p=1.11e-43)
  - 关键发现: gene_B (p=1.01e-01)

### S8 Validation: 稳健性验证
> 结论是否稳健（校正/验证）？

| 证据链 | 分析模块 | 图形 | 结果文件 |
|--------|----------|------|----------|
| differential | `differential` | volcano, ma_plot, heatmap, lollipop | results/differential.csv |
  - 关键发现: biomarker (p=2.22e-20)
  - 关键发现: gene_A (p=2.47e-20)

### S9 Conclusion: 结论与意义
> 回答缺口，临床/理论意义？

（本阶段由故事驱动，无直接分析模块）

## 评审
- 总分: 57/100