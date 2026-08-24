"""
scanpy单细胞场景出图测试脚本 - 简化版
生成 Nature/Science 级别可视化
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# Nature/Science 标准配置
matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.linewidth'] = 0.8
matplotlib.rcParams['axes.labelsize'] = 11

# 创建测试数据
print("生成测试数据...")
adata = sc.datasets.pbmc68k_reduced()
print(f"数据加载成功: {adata.n_obs} cells, {adata.n_vars} genes")

# 设置输出目录
output_dir = Path(r"E:\git\sci-figure-master\test_output\scanpy_test")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. UMAP 聚类图 (按 cell type)
print("生成 UMAP 聚类图...")
sc.pl.umap(adata, color=['louvain'], legend_loc='on data', fontsize=9, frameon=False,
           save='_umap_celltypes', show=False)
plt.close()
print("✓ UMAP 图已保存")

# 2. 基因表达分布图 (箱线图)
print("生成基因表达分布图...")
marker_genes = ['LYZ', 'CD14', 'MS4A1', 'NKG7']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for i, gene in enumerate(marker_genes):
    ax = axes[i//2, i%2]
    data_to_plot = []
    for ctype in adata.obs['louvain'].cat.categories:
        expr = adata[adata.obs['louvain'] == ctype, gene].X.toarray().flatten()
        data_to_plot.append(expr)
    bp = ax.boxplot(data_to_plot, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#4C72B0')
        patch.set_alpha(0.7)
    ax.set_title(f'{gene} Expression', fontsize=11, fontweight='bold')
    ax.set_xlabel('Cell Type', fontsize=10)
    ax.set_ylabel('Expression', fontsize=10)
    ax.set_xticklabels(adata.obs['louvain'].cat.categories.tolist(), rotation=45)

plt.tight_layout()
plt.savefig(output_dir / 'boxplot_genes.svg', bbox_inches='tight', dpi=300)
plt.savefig(output_dir / 'boxplot_genes.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ 箱线图已保存")

# 3. 细胞比例饼图
print("生成细胞比例饼图...")
fig, ax = plt.subplots(figsize=(8, 6))
cell_counts = adata.obs['louvain'].value_counts().sort_values(ascending=False)
colors = plt.cm.tab20c(np.linspace(0, 1, len(cell_counts)))

wedges, texts, autotexts = ax.pie(cell_counts.values, labels=cell_counts.index,
                                  autopct='%1.1f%%', colors=colors,
                                  startangle=90, textprops={'fontsize': 10})
ax.set_title('Cell Type Composition', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'pie_chart.svg', bbox_inches='tight', dpi=300)
plt.savefig(output_dir / 'pie_chart.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ 饼图已保存")

print(f"\n所有测试图像已保存到: {output_dir}")
print("测试完成!")
