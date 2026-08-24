#!/usr/bin/env python3
"""
bioinfo_router.py - 生物信息学绘图零动手路由系统

用法:
    from bioinfo_router import generate_figure
    generate_figure(domain="scRNA", plot_type="UMAP", data=adata, output_path="UMAP.svg")
    generate_figure(domain="general", plot_type="box", data=df, output_path="box.svg")
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Nature/Science 标准配置
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy import stats

# 检查可选依赖
try:
    import scanpy as sc
    HAS_SCANPY = True
except ImportError:
    HAS_SCANPY = False

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

# 路由配置：domain + plot_type -> 处理函数
ROUTING_TABLE = {
    # 单细胞
    ("scRNA", "UMAP"): "plot_umap",
    ("scRNA", "tSNE"): "plot_tsne",
    ("scRNA", "PCA"): "plot_pca",
    ("scRNA", "heatmap"): "plot_heatmap",
    ("scRNA", "violin"): "plot_violin",
    ("scRNA", "dotplot"): "plot_dotplot",
    ("scRNA", "clustree"): "plot_clustree",
    ("scRNA", "trajectory"): "plot_trajectory",
    ("scRNA", "cellchat"): "plot_cellchat",
    ("scRNA", "marker"): "plot_marker",

    # 通用绘图
    ("general", "bar"): "plot_bar",
    ("general", "box"): "plot_box",
    ("general", "boxplot"): "plot_box",
    ("general", "histogram"): "plot_box",
    ("general", "violin"): "plot_violin",
    ("general", "heatmap"): "plot_heatmap",
    ("general", "scatter"): "plot_scatter",
    ("general", "line"): "plot_line",
    ("general", "volcano"): "plot_volcano",
    ("general", "sankey"): "plot_sankey",
    ("general", "circos"): "plot_circos",
    ("general", "pie"): "plot_pie",
    ("general", "heatmap"): "plot_heatmap",

    # 基因组
    ("genome", "browser"): "plot_genome_browser",
    ("genome", "track"): "plot_genome_track",
    ("genome", "cnv"): "plot_cnv",
    ("genome", "circos"): "plot_circos",

    # 宏基因组
    ("microbiome", "alpha"): "plot_alpha_diversity",
    ("microbiome", "beta"): "plot_beta_diversity",
    ("microbiome", "composition"): "plot_composition",
    ("microbiome", "heatmap"): "plot_heatmap",

    # 系统发育
    ("phylogeny", "tree"): "plot_tree",
    ("phylogeny", "circle"): "plot_circle_tree",

    # 富集分析
    ("enrichment", "bar"): "plot_enrichment_bar",
    ("enrichment", "dot"): "plot_enrichment_dot",
    ("enrichment", "network"): "plot_enrichment_network",
    ("enrichment", "emap"): "plot_enrichment_emap",

    # 生存分析
    ("survival", "km"): "plot_km",
    ("survival", "forest"): "plot_forest",

    # 表观
    ("epigenetic", "peaks"): "plot_peaks",
    ("epigenetic", "annotation"): "plot_annotation",

    # 代谢组
    ("metabolomics", "volcano"): "plot_volcano",
    ("metabolomics", "pathway"): "plot_pathway",
    ("metabolomics", "plsda"): "plot_plsda",

    # 蛋白组
    ("proteomics", "volcano"): "plot_volcano",
    ("proteomics", "heatmap"): "plot_heatmap",

    # ── SciVizKit 风格图表（纯 matplotlib 实现）──
    ("general", "ridgeline"): "plot_ridgeline",
    ("general", "raincloud"): "plot_raincloud",
    ("general", "radar"): "plot_radar",
    ("general", "lollipop"): "plot_lollipop",
    ("general", "dumbbell"): "plot_dumbbell",
    ("general", "bubble"): "plot_bubble",
    ("general", "hexbin"): "plot_hexbin",
    ("general", "pairplot"): "plot_pairplot",
    ("general", "parallel_coords"): "plot_parallel_coords",
    ("general", "area"): "plot_area",
    ("general", "stacked_area"): "plot_stacked_area",
    ("general", "donut"): "plot_donut",
    ("general", "treemap"): "plot_treemap",
    ("general", "waffle"): "plot_waffle",
    ("general", "nightingale"): "plot_nightingale",
    ("general", "dendrogram"): "plot_dendrogram",
    ("general", "qqplot"): "plot_qqplot",
    ("general", "ecdf"): "plot_ecdf",
    ("general", "bland_altman"): "plot_bland_altman",
    ("general", "diverging_bar"): "plot_diverging_bar",
    ("general", "radial_bar"): "plot_radial_bar",
    ("general", "marginal_plot"): "plot_marginal_plot",
    ("general", "forest_plot"): "plot_forest_plot",
    ("general", "funnel_plot"): "plot_funnel_plot",
    ("general", "manhattan"): "plot_manhattan",
    ("general", "ma_plot"): "plot_ma_plot",
    ("bulkRNA", "ma_plot"): "plot_ma_plot",
    ("bulkRNA", "forest"): "plot_forest_plot",
    ("genome", "manhattan"): "plot_manhattan",
    ("metabolomics", "bland_altman"): "plot_bland_altman",
    ("metabolomics", "ma_plot"): "plot_ma_plot",
    ("microbiome", "sankey"): "plot_sankey",
    ("microbiome", "donut"): "plot_donut",
    ("microbiome", "treemap"): "plot_treemap",
}


def _normalize_key(s: str) -> str:
    """规范化路由键：小写 + 去特殊字符"""
    return s.lower().strip().replace('-', '').replace('_', '').replace(' ', '')


def get_native_plot_function(domain: str, plot_type: str):
    """获取原生Python绘图函数（大小写不敏感）"""
    d = _normalize_key(domain)
    p = _normalize_key(plot_type)
    for (rd, rp), func_name in ROUTING_TABLE.items():
        if _normalize_key(rd) == d and _normalize_key(rp) == p:
            if hasattr(sys.modules[__name__], func_name):
                return getattr(sys.modules[__name__], func_name)
    return None


def plot_umap(data, output_path: str, color: str = None, **kwargs):
    """UMAP降维图（scanpy）"""
    if not HAS_SCANPY:
        print("Warning: scanpy not installed, using matplotlib fallback")
        return plot_scatter(data, output_path, **kwargs)

    import scanpy as sc
    if color and 'X_umap' in data.obsm:
        fig, ax = plt.subplots(figsize=(8, 6))
        sc.pl.umap(data, color=[color], ax=ax, show=False, **kwargs)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        return output_path
    # 无分组信息或坐标缺失：用 matplotlib 散点兜底
    return plot_scatter(data, output_path, **kwargs)


def plot_tsne(data, output_path: str, color: str = None, **kwargs):
    """tSNE降维图"""
    if not HAS_SCANPY:
        return plot_scatter(data, output_path, **kwargs)

    import scanpy as sc
    if color and 'X_tsne' in data.obsm:
        fig, ax = plt.subplots(figsize=(8, 6))
        sc.pl.tsne(data, color=[color], ax=ax, show=False, **kwargs)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        return output_path
    return plot_scatter(data, output_path, **kwargs)


def plot_pca(data, output_path: str, color: str = None, **kwargs):
    """PCA降维图"""
    if not HAS_SCANPY:
        return plot_scatter(data, output_path, **kwargs)

    import scanpy as sc
    if color and 'X_pca' in data.obsm:
        fig, ax = plt.subplots(figsize=(8, 6))
        sc.pl.pca(data, color=[color], ax=ax, show=False, **kwargs)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        return output_path
    return plot_scatter(data, output_path, **kwargs)


def plot_heatmap(data, output_path: str, **kwargs):
    """热图（通用/单细胞）"""
    fig, ax = plt.subplots(figsize=(10, 8))
    if isinstance(data, pd.DataFrame):
        im = ax.imshow(data.values, cmap='viridis', aspect='auto')
        ax.set_xticks(range(data.shape[1]))
        ax.set_xticklabels(data.columns, rotation=45, ha='right')
        ax.set_yticks(range(data.shape[0]))
        ax.set_yticklabels(data.index)
        plt.colorbar(im, ax=ax)
    elif hasattr(data, 'X') and hasattr(data, 'obs'):  # AnnData
        import scanpy as sc
        groupby = kwargs.pop('groupby', None)
        if groupby is None:
            # 自动检测分组列
            for col in ['louvain', 'leiden', 'clusters', 'cell_type', 'seurat_clusters']:
                if col in data.obs.columns:
                    groupby = col
                    break
        if groupby is not None:
            sc.pl.heatmap(data, var_names=data.var_names[:20], groupby=groupby,
                          show=False, **kwargs)
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            return output_path
        # 无分组列：直接绘制基因均值热图
        X = data[:, data.var_names[:20]].X
        if hasattr(X, 'toarray'):
            X = X.toarray()
        if hasattr(X, 'A'):
            X = np.asarray(X.A)
        im = ax.imshow(X, cmap='viridis', aspect='auto')
        ax.set_xticks(range(min(20, X.shape[1])))
        ax.set_xticklabels(data.var_names[:20], rotation=45, ha='right')
        ax.set_xlabel('Genes')
        ax.set_ylabel('Cells')
        plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_box(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """箱线图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if hasattr(data, 'obs') and x and y:  # AnnData
        for cat in data.obs[x].cat.categories:
            vals = data[data.obs[x] == cat, y].X.toarray().flatten()
            ax.boxplot(vals, positions=[list(data.obs[x].cat.categories).index(cat)+1])
        ax.set_xticks(range(1, len(data.obs[x].cat.categories)+1))
        ax.set_xticklabels(data.obs[x].cat.categories, rotation=45)
    elif isinstance(data, pd.DataFrame):
        if x and y:
            sns.boxplot(data=data, x=x, y=y, ax=ax, **kwargs)
        else:
            for col in data.columns:
                ax.boxplot(data[col], positions=[list(data.columns).index(col)+1])
            ax.set_xticks(range(1, len(data.columns)+1))
            ax.set_xticklabels(data.columns, rotation=45)
    ax.set_ylabel('Value')
    ax.set_title('Box Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_violin(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """小提琴图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if hasattr(data, 'obs') and x and y:  # AnnData
        for cat in data.obs[x].cat.categories:
            vals = data[data.obs[x] == cat, y].X.toarray().flatten()
            ax.violinplot([vals], positions=[list(data.obs[x].cat.categories).index(cat)+1])
        ax.set_xticks(range(1, len(data.obs[x].cat.categories)+1))
        ax.set_xticklabels(data.obs[x].cat.categories, rotation=45)
    elif isinstance(data, pd.DataFrame):
        if x and y:
            sns.violinplot(data=data, x=x, y=y, ax=ax, **kwargs)
    ax.set_ylabel('Value')
    ax.set_title('Violin Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_scatter(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """散点图"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if hasattr(data, 'obsm') and 'X_umap' in data.obsm:  # AnnData with UMAP
        ax.scatter(data.obsm['X_umap'][:, 0], data.obsm['X_umap'][:, 1], alpha=0.5, **kwargs)
        if x in data.obs.columns:
            for cat in data.obs[x].cat.categories:
                mask = data.obs[x] == cat
                ax.scatter(data.obsm['X_umap'][mask, 0], data.obsm['X_umap'][mask, 1], label=cat)
            ax.legend()
    elif isinstance(data, pd.DataFrame) and x and y:
        ax.scatter(data[x], data[y], alpha=0.5, **kwargs)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Scatter Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_line(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """线图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        if x and y:
            ax.plot(data[x], data[y], **kwargs)
        else:
            for col in data.columns:
                ax.plot(data.index, data[col], label=col)
            ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Line Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_volcano(data, output_path: str, log2fc_col: str = None, pval_col: str = None, **kwargs):
    """火山图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    if isinstance(data, pd.DataFrame):
        if log2fc_col and pval_col:
            log2fc = data[log2fc_col].values
            pvals = data[pval_col].values
            neg_log10_p = -np.log10(np.maximum(pvals, 1e-300))
            ax.scatter(log2fc, neg_log10_p, alpha=0.5, s=20)
            ax.axhline(y=-np.log10(0.05), color='red', linestyle='--', label='p=0.05')
            ax.axvline(x=0, color='gray', linestyle='--')
            ax.set_xlabel('log2(Fold Change)')
            ax.set_ylabel('-log10(p-value)')
        else:
            # 简化版：使用第一列vs第二列
            cols = data.columns[:2]
            ax.scatter(data[cols[0]], data[cols[1]], alpha=0.5)
    ax.set_title('Volcano Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_bar(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """柱状图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        if x and y:
            data.groupby(x)[y].mean().plot.bar(ax=ax, **kwargs)
        else:
            data.mean().plot.bar(ax=ax, **kwargs)
    ax.set_title('Bar Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_pie(data, output_path: str, labels: list = None, **kwargs):
    """饼图"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.Series):
        ax.pie(data.values, labels=data.index, **kwargs)
    elif isinstance(data, pd.DataFrame) and len(data.columns) == 1:
        ax.pie(data.values.flatten(), labels=data.index, **kwargs)
    ax.set_title('Pie Chart')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_dotplot(data, output_path: str, **kwargs):
    """点图（简化版）"""
    fig, ax = plt.subplots(figsize=(10, 8))
    if isinstance(data, pd.DataFrame):
        im = ax.imshow(data.values, cmap='viridis', aspect='auto')
        ax.set_xticks(range(data.shape[1]))
        ax.set_xticklabels(data.columns, rotation=45, ha='right')
        ax.set_yticks(range(data.shape[0]))
        ax.set_yticklabels(data.index)
        plt.colorbar(im, ax=ax)
    ax.set_title('Dot Plot')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_clustree(data, output_path: str, **kwargs):
    """聚类树（简化版）"""
    print("Note: clustree requires R. Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_trajectory(data, output_path: str, **kwargs):
    """轨迹图（简化版）"""
    print("Note: trajectory requires scVelo/monocle3. Using UMAP as fallback.")
    return plot_umap(data, output_path, **kwargs)


def plot_cellchat(data, output_path: str, **kwargs):
    """细胞通讯图（简化版）"""
    print("Note: CellChat requires R. Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_marker(data, output_path: str, **kwargs):
    """Marker基因表达图"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    if hasattr(data, 'var_names'):
        marker_genes = data.var_names[:4]
    elif isinstance(data, pd.DataFrame):
        marker_genes = data.columns[:4]
    else:
        marker_genes = ['Gene1', 'Gene2', 'Gene3', 'Gene4']

    for i, gene in enumerate(marker_genes):
        ax = axes[i]
        if hasattr(data, 'obs') and gene in data.var_names:
            for cat in data.obs['louvain'].cat.categories:
                expr = data[data.obs['louvain'] == cat, gene].X.toarray().flatten()
                ax.boxplot(expr, positions=[1], widths=0.6)
            ax.set_title(gene)
            ax.set_xticks([1])
            ax.set_xticklabels(data.obs['louvain'].cat.categories.tolist(), rotation=45)
        elif isinstance(data, pd.DataFrame) and gene in data.columns:
            ax.boxplot([data[gene].values])
            ax.set_title(gene)
    plt.suptitle('Marker Gene Expression', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


# 更多绘图函数...
def plot_genome_browser(data, output_path: str, **kwargs):
    """基因组浏览器（简化版）"""
    print("Note: genome browser requires GW/pyGenomeTracks. Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_genome_track(data, output_path: str, **kwargs):
    """基因组轨道图（简化版）"""
    print("Note: genome track requires pyGenomeTracks.")
    return plot_heatmap(data, output_path, **kwargs)


def plot_cnv(data, output_path: str, **kwargs):
    """CNV图（简化版）"""
    print("Note: CNV requires cnvkit. Using heatmap as fallback.")
    return plot_heatmap(data, output_path, **kwargs)


def plot_circos(data, output_path: str, **kwargs):
    """圈图（简化版）"""
    print("Note: circos requires circlize (R). Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_alpha_diversity(data, output_path: str, **kwargs):
    """Alpha多样性（简化版）"""
    print("Note: alpha diversity requires phyloseq (R). Using boxplot as fallback.")
    return plot_box(data, output_path, **kwargs)


def plot_beta_diversity(data, output_path: str, **kwargs):
    """Beta多样性（简化版）"""
    print("Note: beta diversity requires phyloseq (R). Using PCoA plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_composition(data, output_path: str, **kwargs):
    """物种组成（简化版）"""
    print("Note: composition requires phyloseq (R). Using bar plot as fallback.")
    return plot_bar(data, output_path, **kwargs)


def plot_tree(data, output_path: str, **kwargs):
    """系统发育树（简化版）"""
    print("Note: tree requires ggtree (R). Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_circle_tree(data, output_path: str, **kwargs):
    """圆形系统发育树（简化版）"""
    print("Note: circle tree requires ggtree (R). Using scatter plot as fallback.")
    return plot_scatter(data, output_path, **kwargs)


def plot_enrichment_bar(data, output_path: str, **kwargs):
    """富集分析柱状图（简化版）"""
    return plot_bar(data, output_path, **kwargs)


def plot_enrichment_dot(data, output_path: str, **kwargs):
    """富集分析点图（简化版）"""
    return plot_dotplot(data, output_path, **kwargs)


def plot_enrichment_network(data, output_path: str, **kwargs):
    """富集分析网络图（简化版）"""
    print("Note: enrichment network requires enrichplot (R). Using dot plot as fallback.")
    return plot_dotplot(data, output_path, **kwargs)


def plot_enrichment_emap(data, output_path: str, **kwargs):
    """富集分析emaplot（简化版）"""
    print("Note: emap requires enrichplot (R). Using dot plot as fallback.")
    return plot_dotplot(data, output_path, **kwargs)


def plot_km(data, output_path: str, **kwargs):
    """KM生存曲线（简化版）"""
    print("Note: KM curve requires survminer (R). Using line plot as fallback.")
    return plot_line(data, output_path, **kwargs)


def plot_forest(data, output_path: str, **kwargs):
    """森林图（简化版）"""
    print("Note: forest plot requires survminer (R). Using forest plot fallback.")
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        ax.scatter(data.mean(axis=1), data.std(axis=1), alpha=0.5)
    ax.set_xlabel('Effect Size')
    ax.set_ylabel('SE')
    ax.set_title('Forest Plot (Simplified)')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_peaks(data, output_path: str, **kwargs):
    """峰图（简化版）"""
    print("Note: peaks requires ChIPseeker/pyGenomeTracks.")
    return plot_heatmap(data, output_path, **kwargs)


def plot_annotation(data, output_path: str, **kwargs):
    """峰注释（简化版）"""
    print("Note: annotation requires ChIPseeker (R).")
    return plot_heatmap(data, output_path, **kwargs)


def plot_pathway(data, output_path: str, **kwargs):
    """通路图（简化版）"""
    print("Note: pathway requires MetaboAnalystR (R).")
    return plot_heatmap(data, output_path, **kwargs)


def plot_plsda(data, output_path: str, **kwargs):
    """PLS-DA图（简化版）"""
    print("Note: PLS-DA requires MetaboAnalystR (R). Using PCA as fallback.")
    return plot_pca(data, output_path, **kwargs)


def plot_sankey(data, output_path: str, **kwargs):
    """桑基图（纯 matplotlib 实现，层级流转）"""
    fig, ax = plt.subplots(figsize=(12, 6))
    if isinstance(data, pd.DataFrame):
        # 输入格式: 两列分类 -> 流转计数，或 3+ 列多层级
        cols = list(data.columns)
        if len(cols) >= 2:
            # 多层级 Sankey（简化：每对相邻列画一层）
            n_layers = len(cols)
            layer_sizes = []
            for c in cols:
                if pd.api.types.is_numeric_dtype(data[c]) and data[c].nunique() < 20:
                    cats = data[c].astype(int).astype(str)
                else:
                    cats = data[c].astype(str)
                layer_sizes.append(cats)
            # 左到右画条带
            x_positions = np.linspace(0.05, 0.95, n_layers)
            for li in range(n_layers - 1):
                left = layer_sizes[li]
                right = layer_sizes[li + 1]
                left_cats = pd.Series(left).value_counts()
                right_cats = pd.Series(right).value_counts()
                # 画左侧条带
                left_total = left_cats.sum()
                y_cursor = 0.0
                left_bounds = {}
                for cat, cnt in left_cats.items():
                    h = cnt / left_total * 0.9
                    ax.bar(x=x_positions[li], height=h, width=0.02,
                           color=plt.cm.tab20(hash(cat) % 20), bottom=y_cursor + 0.05)
                    left_bounds[cat] = (y_cursor + 0.05, y_cursor + 0.05 + h)
                    y_cursor += h
                # 画右侧条带
                y_cursor = 0.0
                right_bounds = {}
                for cat, cnt in right_cats.items():
                    h = cnt / right_cats.sum() * 0.9
                    ax.bar(x=x_positions[li + 1], height=h, width=0.02,
                           color=plt.cm.tab20(hash(cat) % 20), bottom=y_cursor + 0.05)
                    right_bounds[cat] = (y_cursor + 0.05, y_cursor + 0.05 + h)
                    y_cursor += h
                # 连线（简化为层间平均连接）
                for lcat in list(left_bounds.keys())[:12]:
                    yl = sum(left_bounds[lcat]) / 2
                    for rcat in list(right_bounds.keys())[:12]:
                        yr = sum(right_bounds[rcat]) / 2
                        ax.plot([x_positions[li] + 0.01, x_positions[li + 1] - 0.01],
                                [yl, yr], color=plt.cm.tab20(hash(lcat) % 20), alpha=0.15, lw=1)
            ax.set_xticks(x_positions)
            ax.set_xticklabels(cols)
            ax.set_yticks([])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
    else:
        ax.text(0.5, 0.5, 'Sankey Diagram\n(Requires DataFrame)', ha='center', va='center', fontsize=14)
    ax.set_title('Sankey / Alluvial Diagram', fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


# ═════════════════════════════════════════════════════════════
# SciVizKit 风格图表（纯 matplotlib 实现，25 种新增）
# ═════════════════════════════════════════════════════════════

def plot_ridgeline(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """山脊图（Ridgeline / Joy Plot）: 分组KDE曲线纵向错开"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame) and x and y and y in data.columns:
        groups = data[x].unique()
        from scipy.stats import gaussian_kde
        offset = 0
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(groups)))
        for gi, g in enumerate(groups):
            vals = data.loc[data[x] == g, y].dropna()
            if len(vals) < 5:
                continue
            kde = gaussian_kde(vals)
            xs = np.linspace(vals.min(), vals.max(), 200)
            ys = kde(xs)
            ax.fill_between(xs, offset, offset + ys, color=colors[gi], alpha=0.6)
            ax.plot(xs, offset + ys, color=colors[gi], lw=1.2)
            ax.text(xs[-1] + 0.02 * (xs.max() - xs.min()), offset + ys[-1] * 0.3,
                    str(g), va='center', fontsize=10)
            offset += ys.max() * 1.6
        ax.set_yticks([])
        ax.set_xlabel(y)
        ax.set_title('Ridgeline Plot', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Ridgeline\n(Requires: x=group, y=numeric)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_raincloud(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """雨云图（Raincloud）: 半小提琴 + 箱线 + 抖动散点"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame) and x and y and y in data.columns:
        groups = data[x].unique()
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(groups)))
        for gi, g in enumerate(groups):
            vals = data.loc[data[x] == g, y].dropna().values
            if len(vals) < 3:
                continue
            # 半小提琴（左）
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(vals)
            xs = np.linspace(vals.min(), vals.max(), 150)
            ys = kde(xs) / kde(xs).max() * 0.4
            ax.fill_betweenx(xs, gi - ys, gi, color=colors[gi], alpha=0.5)
            ax.plot(gi - ys, xs, color=colors[gi], lw=1)
            # 箱线（中）
            bp = ax.boxplot(vals, positions=[gi + 0.12], widths=0.08, patch_artist=True,
                            medianprops=dict(color='black', lw=1.5))
            bp['boxes'][0].set_facecolor(colors[gi])
            bp['boxes'][0].set_alpha(0.8)
            # 抖动散点（右）
            jitter = np.random.normal(gi + 0.22, 0.03, len(vals))
            ax.scatter(jitter, vals, s=6, color=colors[gi], alpha=0.6, zorder=3)
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([str(g) for g in groups], rotation=30)
        ax.set_ylabel(y)
        ax.set_title('Raincloud Plot', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Raincloud\n(Requires: x=group, y=numeric)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_radar(data, output_path: str, **kwargs):
    """雷达图（Radar / Spider Chart）: 多维比较"""
    fig = plt.figure(figsize=(8, 8))
    if isinstance(data, pd.DataFrame) and data.shape[1] >= 2:
        ax = fig.add_subplot(111, polar=True)
        if 'group' in data.columns or 'class' in data.columns:
            gcol = 'group' if 'group' in data.columns else 'class'
            cats = data.drop(columns=[gcol])
            labels = list(cats.columns)
            for gi, g in enumerate(data[gcol].unique()):
                vals = cats.loc[data[gcol] == g].mean().values
                vals = np.append(vals, vals[0])
                angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
                angles += angles[:1]
                ax.plot(angles, vals, label=str(g), lw=2)
                ax.fill(angles, vals, alpha=0.15)
        else:
            labels = list(data.columns)
            for _, row in data.head(5).iterrows():
                vals = row.values.astype(float)
                vals = np.append(vals, vals[0])
                angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
                angles += angles[:1]
                ax.plot(angles, vals, lw=1.5, alpha=0.7)
        ax.set_xticks(np.linspace(0, 2 * np.pi, len(labels), endpoint=False))
        ax.set_xticklabels(labels)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False)
        ax.set_title('Radar Chart', fontweight='bold', pad=20)
    else:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Radar\n(Requires DataFrame >= 2 cols)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_lollipop(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """棒棒糖图（Lollipop Chart）: 线+点替代柱状"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        if x and y and y in data.columns:
            labels = data[x].astype(str).values
            vals = pd.to_numeric(data[y], errors='coerce').values
        else:
            dfn = data.select_dtypes(include=[np.number])
            if len(dfn.columns) == 0:
                ax.text(0.5, 0.5, 'No numeric columns', ha='center', va='center')
                plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
                return output_path
            labels = dfn.index.astype(str).values
            vals = dfn.iloc[:, 0].values
        idx = np.arange(len(vals))
        ax.hlines(0, -0.5, len(vals) - 0.5, color='grey', lw=0.8)
        ax.vlines(idx, 0, vals, color='steelblue', lw=2)
        ax.scatter(idx, vals, s=60, color='crimson', zorder=3)
        ax.set_xticks(idx)
        ax.set_xticklabels(labels, rotation=60, ha='right')
        ax.set_title('Lollipop Chart', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Lollipop\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_dumbbell(data, output_path: str, **kwargs):
    """哑铃图（Dumbbell Chart）: 两点间变化"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame) and data.shape[1] >= 2:
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            start = dfn.iloc[:, 0].values
            end = dfn.iloc[:, 1].values
            labels = data.index.astype(str).values
            y = np.arange(len(labels))
            for i in range(len(labels)):
                ax.plot([start[i], end[i]], [y[i], y[i]], color='grey', lw=1.5, zorder=1)
                ax.scatter([start[i]], [y[i]], s=50, color='steelblue', zorder=2)
                ax.scatter([end[i]], [y[i]], s=50, color='crimson', zorder=2)
            ax.set_yticks(y)
            ax.set_yticklabels(labels)
            ax.set_title(f'Dumbbell Chart ({dfn.columns[0]} vs {dfn.columns[1]})', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Dumbbell\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_bubble(data, output_path: str, x: str = None, y: str = None, size: str = None, **kwargs):
    """气泡图（Bubble Chart）: 3变量（x, y, size）"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if x and x in data.columns and y and y in data.columns:
            xs = pd.to_numeric(data[x], errors='coerce').values
            ys = pd.to_numeric(data[y], errors='coerce').values
            sizes = pd.to_numeric(data[size], errors='coerce').values if size and size in data.columns else np.ones(len(data))
        elif dfn.shape[1] >= 2:
            xs = dfn.iloc[:, 0].values
            ys = dfn.iloc[:, 1].values
            sizes = dfn.iloc[:, 2].values if dfn.shape[1] >= 3 else np.ones(len(data))
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        valid = ~(np.isnan(xs) | np.isnan(ys))
        sc = ax.scatter(xs[valid], ys[valid], s=(np.abs(sizes[valid]) / np.nanmax(np.abs(sizes[valid])) + 0.05) * 500,
                        alpha=0.7, c=ys[valid], cmap='viridis', edgecolors='white', linewidths=0.5)
        plt.colorbar(sc, ax=ax)
        ax.set_xlabel(x or 'Variable 1')
        ax.set_ylabel(y or 'Variable 2')
        ax.set_title('Bubble Chart', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Bubble\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_hexbin(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """六边形分箱图（Hexbin）: 大数据密度"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if x and x in data.columns and y and y in data.columns:
            xs = pd.to_numeric(data[x], errors='coerce').values
            ys = pd.to_numeric(data[y], errors='coerce').values
        elif dfn.shape[1] >= 2:
            xs = dfn.iloc[:, 0].values
            ys = dfn.iloc[:, 1].values
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        valid = ~(np.isnan(xs) | np.isnan(ys))
        hb = ax.hexbin(xs[valid], ys[valid], gridsize=30, cmap='inferno', mincnt=1)
        plt.colorbar(hb, ax=ax, label='Count')
        ax.set_xlabel(x or dfn.columns[0])
        ax.set_ylabel(y or dfn.columns[1])
        ax.set_title('Hexbin Plot', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Hexbin\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_pairplot(data, output_path: str, **kwargs):
    """配对图（Pairplot）: 多变量两两散点+对角分布"""
    try:
        import seaborn as sns
        g = sns.pairplot(data.select_dtypes(include=[np.number]).head(200), corner=True, diag_kind='kde')
        g.fig.suptitle('Pair Plot', y=1.02, fontweight='bold')
        g.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close('all')
        return output_path
    except Exception as e:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, f'Pairplot requires seaborn: {e}', ha='center', va='center')
        plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
        return output_path


def plot_parallel_coords(data, output_path: str, **kwargs):
    """平行坐标图（Parallel Coordinates）"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number]).head(100)
        if dfn.shape[1] >= 2:
            vals = (dfn - dfn.min()) / (dfn.max() - dfn.min() + 1e-12)
            x_pos = np.arange(dfn.shape[1])
            for i in range(dfn.shape[0]):
                ax.plot(x_pos, vals.iloc[i].values, lw=0.5, alpha=0.5,
                        color=plt.cm.viridis(i / dfn.shape[0]))
            ax.set_xticks(x_pos)
            ax.set_xticklabels(dfn.columns, rotation=30, ha='right')
            ax.set_ylim(-0.05, 1.05)
            ax.set_title('Parallel Coordinates', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Parallel Coordinates\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_area(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """面积图（Area Chart）: 趋势+累积"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        if x and x in data.columns and y and y in data.columns:
            xs = pd.to_numeric(data[x], errors='coerce').values
            ys = pd.to_numeric(data[y], errors='coerce').values
        else:
            dfn = data.select_dtypes(include=[np.number])
            if dfn.shape[1] == 0:
                ax.text(0.5, 0.5, 'No numeric columns', ha='center', va='center')
                plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
                return output_path
            xs = np.arange(len(dfn))
            ys = dfn.iloc[:, 0].values
        ax.fill_between(xs, ys, alpha=0.4, color='steelblue')
        ax.plot(xs, ys, color='navy', lw=2)
        ax.set_title('Area Chart', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Area\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_stacked_area(data, output_path: str, **kwargs):
    """堆叠面积图（Stacked Area）"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            ax.stackplot(np.arange(len(dfn)), *[dfn[c].values for c in dfn.columns],
                         labels=list(dfn.columns), alpha=0.7)
            ax.legend(loc='upper left', frameon=False, fontsize=8)
            ax.set_title('Stacked Area Chart', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Stacked Area\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_donut(data, output_path: str, **kwargs):
    """环形图（Donut Chart）"""
    fig, ax = plt.subplots(figsize=(8, 8))
    if isinstance(data, pd.DataFrame):
        if 'group' in data.columns:
            counts = data['group'].value_counts()
            labels = counts.index.astype(str).values
            vals = counts.values
        else:
            dfn = data.select_dtypes(include=[np.number])
            if dfn.shape[1] == 0:
                ax.text(0.5, 0.5, 'No numeric column', ha='center', va='center')
                plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
                return output_path
            vals = dfn.iloc[0].values
            labels = dfn.columns.astype(str).values
        wedges, _texts, _autotexts = ax.pie(vals, labels=labels, wedgeprops=dict(width=0.35, edgecolor='white'),
                           colors=plt.cm.tab20(np.linspace(0, 1, len(vals))), autopct='%1.1f%%')
        ax.set_title('Donut Chart', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Donut\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_treemap(data, output_path: str, **kwargs):
    """矩形树图（Treemap）: 递归矩形面积编码"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    if isinstance(data, pd.DataFrame):
        if 'group' in data.columns and len(data.columns) >= 2:
            grp = data['group'].astype(str)
            num_col = [c for c in data.columns if c != 'group' and pd.api.types.is_numeric_dtype(data[c])]
            if num_col:
                sizes = data.groupby('group')[num_col[0]].sum().sort_values(ascending=False)
            else:
                sizes = grp.value_counts()
        else:
            dfn = data.select_dtypes(include=[np.number])
            if dfn.shape[1] == 0:
                ax.text(0.5, 0.5, 'No numeric column', ha='center', va='center')
                plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
                return output_path
            sizes = dfn.iloc[0].sort_values(ascending=False)
        total = sizes.sum()
        x0, y0, w, h = 0, 0, 1, 1
        for i, (cat, val) in enumerate(sizes.head(15).items()):
            frac = val / total
            if w >= h:  # 竖切
                sub_w = w * frac
                ax.add_patch(plt.Rectangle((x0, y0), sub_w, h, facecolor=plt.cm.viridis(i / 15),
                                           edgecolor='white', lw=1.5))
                if sub_w > 0.08 and h > 0.08:
                    ax.text(x0 + sub_w / 2, y0 + h / 2, f'{cat}\n{val:.1f}', ha='center', va='center',
                            fontsize=8, color='white')
                x0 += sub_w; w -= sub_w
            else:  # 横切
                sub_h = h * frac
                ax.add_patch(plt.Rectangle((x0, y0), w, sub_h, facecolor=plt.cm.viridis(i / 15),
                                           edgecolor='white', lw=1.5))
                if w > 0.08 and sub_h > 0.08:
                    ax.text(x0 + w / 2, y0 + sub_h / 2, f'{cat}\n{val:.1f}', ha='center', va='center',
                            fontsize=8, color='white')
                y0 += sub_h; h -= sub_h
        ax.set_title('Treemap', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Treemap\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_waffle(data, output_path: str, **kwargs):
    """华夫饼图（Waffle Chart）: 10x10 方格占比"""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    if isinstance(data, pd.DataFrame):
        if 'group' in data.columns:
            counts = data['group'].value_counts()
        else:
            dfn = data.select_dtypes(include=[np.number])
            counts = dfn.iloc[0] if dfn.shape[1] > 0 else pd.Series({'A': 1})
        total = counts.sum() if counts.sum() > 0 else 1
        n = 100
        proportions = counts / total * n
        filled = proportions.round().astype(int)
        cells = []
        for cat, cnt in filled.items():
            cells.extend([cat] * max(0, int(cnt)))
        cells = cells[:100]
        colors = plt.cm.tab20(np.linspace(0, 1, len(counts)))
        cmap = {cat: colors[i] for i, cat in enumerate(counts.index)}
        for i, cell in enumerate(cells):
            x = i % 10
            y = 9 - i // 10
            ax.add_patch(plt.Rectangle((x, y), 1, 1, facecolor=cmap.get(cell, 'grey'),
                                       edgecolor='white', lw=0.5))
        handles = [plt.Rectangle((0, 0), 1, 1, facecolor=cmap[cat]) for cat in counts.index]
        ax.legend(handles, [f'{cat} ({counts[cat]})' for cat in counts.index],
                  loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=min(4, len(counts)), frameon=False)
        ax.set_title('Waffle Chart', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Waffle\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_nightingale(data, output_path: str, **kwargs):
    """南丁格尔玫瑰图（Nightingale Rose / Polar Bar）"""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] > 0:
            vals = dfn.iloc[0].values if dfn.shape[0] <= 5 else dfn.mean().values
            labels = dfn.columns.astype(str).values
            n = len(vals)
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
            ax.bar(angles, vals, width=2 * np.pi / n, color=plt.cm.viridis(np.linspace(0, 1, n)),
                   edgecolor='white', alpha=0.9)
            ax.set_xticks(angles)
            ax.set_xticklabels(labels, fontsize=8)
            ax.set_title('Nightingale Rose Chart', fontweight='bold', pad=25)
        else:
            ax.text(0, 0, 'No numeric column', ha='center', va='center')
    else:
        ax.text(0, 0, 'Nightingale\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_dendrogram(data, output_path: str, **kwargs):
    """树状图（Dendrogram）: 层次聚类"""
    fig, ax = plt.subplots(figsize=(10, 7))
    if isinstance(data, pd.DataFrame):
        from scipy.cluster.hierarchy import dendrogram, linkage
        dfn = data.select_dtypes(include=[np.number]).T
        if dfn.shape[0] >= 2:
            Z = linkage(dfn, method='ward')
            dendrogram(Z, labels=[str(i) for i in dfn.index], ax=ax, leaf_rotation=90)
            ax.set_title('Dendrogram (Ward Linkage)', fontweight='bold')
            ax.set_ylabel('Distance')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 rows', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Dendrogram\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_qqplot(data, output_path: str, **kwargs):
    """Q-Q 图: 正态性检验"""
    fig, ax = plt.subplots(figsize=(7, 7))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        col = kwargs.get('column', dfn.columns[0] if dfn.shape[1] > 0 else None)
        if col:
            vals = pd.to_numeric(data[col], errors='coerce').dropna().values
            (osm, osr), (slope, intercept, r) = stats.probplot(vals, dist="norm")
            ax.scatter(osm, osr, s=20, alpha=0.6, color='steelblue')
            ax.plot(osm, slope * osm + intercept, color='crimson', lw=2)
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Sample Quantiles')
            ax.set_title(f'Q-Q Plot ({col})', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No numeric column', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Q-Q Plot\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_ecdf(data, output_path: str, **kwargs):
    """经验累积分布函数图（ECDF）"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        group_col = kwargs.get('group_col', None)
        cols = list(dfn.columns)[:5]
        if group_col and group_col in data.columns:
            for gi, g in enumerate(data[group_col].unique()[:5]):
                vals = pd.to_numeric(data.loc[data[group_col] == g, dfn.columns[0]],
                                     errors='coerce').dropna().values
                xs = np.sort(vals)
                ys = np.arange(1, len(xs) + 1) / len(xs)
                ax.plot(xs, ys, lw=2, label=str(g))
            ax.legend(frameon=False)
            ax.set_xlabel(dfn.columns[0])
        elif dfn.shape[1] > 0:
            for ci, col in enumerate(cols):
                vals = pd.to_numeric(data[col], errors='coerce').dropna().values
                xs = np.sort(vals)
                ys = np.arange(1, len(xs) + 1) / len(xs)
                ax.plot(xs, ys, lw=2, label=col)
            ax.legend(frameon=False)
        ax.set_ylabel('ECDF')
        ax.set_title('Empirical CDF', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'ECDF\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_bland_altman(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """Bland-Altman 一致性图"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if x and x in data.columns and y and y in data.columns:
            a = pd.to_numeric(data[x], errors='coerce').values
            b = pd.to_numeric(data[y], errors='coerce').values
        elif dfn.shape[1] >= 2:
            a = dfn.iloc[:, 0].values
            b = dfn.iloc[:, 1].values
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        valid = ~(np.isnan(a) | np.isnan(b))
        a, b = a[valid], b[valid]
        mean = (a + b) / 2
        diff = a - b
        md = np.mean(diff)
        sd = np.std(diff)
        ax.scatter(mean, diff, alpha=0.6, s=25, color='steelblue')
        ax.axhline(md, color='crimson', lw=1.5, label=f'Mean diff = {md:.3f}')
        ax.axhline(md + 1.96 * sd, color='grey', ls='--', lw=1, label=f'+1.96 SD = {md + 1.96 * sd:.3f}')
        ax.axhline(md - 1.96 * sd, color='grey', ls='--', lw=1, label=f'-1.96 SD = {md - 1.96 * sd:.3f}')
        ax.set_xlabel('Mean of two measurements')
        ax.set_ylabel('Difference')
        ax.legend(frameon=False, fontsize=8)
        ax.set_title('Bland-Altman Plot', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'Bland-Altman\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_diverging_bar(data, output_path: str, **kwargs):
    """发散条形图（Diverging Bar）: 正负值偏离零轴"""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] > 0:
            vals = dfn.iloc[:, 0].values
            labels = data.index.astype(str).values if len(data.index) == len(vals) else np.arange(len(vals)).astype(str)
            colors = ['crimson' if v >= 0 else 'steelblue' for v in vals]
            y = np.arange(len(vals))
            ax.barh(y, vals, color=colors, alpha=0.85)
            ax.axvline(0, color='grey', lw=1)
            ax.set_yticks(y)
            ax.set_yticklabels(labels, fontsize=8)
            ax.set_title(f'Diverging Bar ({dfn.columns[0]})', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No numeric column', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Diverging Bar\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_radial_bar(data, output_path: str, **kwargs):
    """环形柱状图（Radial Bar）"""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] > 0:
            vals = dfn.iloc[0].values if dfn.shape[0] <= 10 else dfn.mean().values
            labels = dfn.columns.astype(str).values
            n = len(vals)
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
            ax.bar(angles, vals, width=2 * np.pi / n * 0.8,
                   color=plt.cm.viridis(np.linspace(0, 1, n)), alpha=0.85, edgecolor='white')
            ax.set_xticks(angles)
            ax.set_xticklabels(labels, fontsize=8)
            ax.set_title('Radial Bar Chart', fontweight='bold', pad=25)
        else:
            ax.text(0, 0, 'No numeric column', ha='center', va='center')
    else:
        ax.text(0, 0, 'Radial Bar\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_marginal_plot(data, output_path: str, x: str = None, y: str = None, **kwargs):
    """边际图（Marginal Plot）: 散点+边际直方图"""
    fig = plt.figure(figsize=(8, 8))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if x and x in data.columns and y and y in data.columns:
            xs = pd.to_numeric(data[x], errors='coerce').values
            ys = pd.to_numeric(data[y], errors='coerce').values
        elif dfn.shape[1] >= 2:
            xs = dfn.iloc[:, 0].values
            ys = dfn.iloc[:, 1].values
        else:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        grid = plt.GridSpec(4, 4, wspace=0.1, hspace=0.1)
        ax_main = fig.add_subplot(grid[1:, :-1])
        ax_top = fig.add_subplot(grid[0, :-1], sharex=ax_main)
        ax_right = fig.add_subplot(grid[1:, -1], sharey=ax_main)
        valid = ~(np.isnan(xs) | np.isnan(ys))
        ax_main.scatter(xs[valid], ys[valid], s=15, alpha=0.5, color='steelblue')
        ax_top.hist(xs[valid], bins=30, color='steelblue', alpha=0.7)
        ax_right.hist(ys[valid], bins=30, orientation='horizontal', color='steelblue', alpha=0.7)
        for a in [ax_top, ax_right]:
            a.set_xticks([]); a.set_yticks([])
        ax_main.set_xlabel(x or 'Variable 1')
        ax_main.set_ylabel(y or 'Variable 2')
        fig.suptitle('Marginal Plot', fontweight='bold')
    else:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Marginal Plot\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_manhattan(data, output_path: str, chrom_col: str = None, pos_col: str = None,
                   pval_col: str = None, **kwargs):
    """曼哈顿图（Manhattan Plot）: GWAS 全基因组显著性"""
    fig, ax = plt.subplots(figsize=(14, 5))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            chrom = data[chrom_col].astype(str) if chrom_col and chrom_col in data.columns else dfn.index.astype(str)
            pos = pd.to_numeric(data[pos_col], errors='coerce').values if pos_col and pos_col in data.columns else np.arange(len(data))
            pval = pd.to_numeric(data[pval_col], errors='coerce').values if pval_col and pval_col in data.columns else dfn.iloc[:, -1].values
            neg_log_p = -np.log10(np.clip(pval, 1e-300, None))
            # 按染色体着色
            chroms = chrom.unique()
            color_map = {c: ('steelblue' if i % 2 == 0 else 'crimson') for i, c in enumerate(chroms)}
            x_offset = 0
            ticks = []
            tick_labels = []
            for c in chroms[:30]:
                mask = chrom == c
                xs = np.where(mask)[0] + x_offset
                ax.scatter(xs, neg_log_p[mask], s=8, alpha=0.6, color=color_map.get(c, 'grey'))
                ticks.append((xs.min() + xs.max()) / 2 if len(xs) else 0)
                tick_labels.append(str(c))
                x_offset += mask.sum()
            # 显著性阈值线
            sig = kwargs.get('sig_level', 5e-8)
            ax.axhline(-np.log10(sig), color='crimson', ls='--', lw=1.2,
                       label=f'p = {sig:.1e}')
            ax.set_xticks(ticks)
            ax.set_xticklabels(tick_labels, fontsize=8, rotation=60)
            ax.set_xlabel('Chromosome')
            ax.set_ylabel('-log10(p)')
            ax.legend(frameon=False)
            ax.set_title('Manhattan Plot', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Manhattan\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_ma_plot(data, output_path: str, **kwargs):
    """MA 图: 平均表达量 vs 差异倍数"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            a = dfn.iloc[:, 0].values
            b = dfn.iloc[:, 1].values
            m = np.log2((a + 1e-10) / (b + 1e-10))
            a_val = 0.5 * (np.log2(a + 1e-10) + np.log2(b + 1e-10))
            ax.scatter(a_val, m, s=8, alpha=0.5, color='steelblue')
            ax.axhline(0, color='crimson', lw=1)
            ax.axhline(1, color='grey', ls='--', lw=0.8)
            ax.axhline(-1, color='grey', ls='--', lw=0.8)
            ax.set_xlabel('Mean log2 expression')
            ax.set_ylabel('log2 fold change')
            ax.set_title('MA Plot', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'MA Plot\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_forest_plot(data, output_path: str, **kwargs):
    """森林图（Forest Plot）: 效应量 + 置信区间"""
    fig, ax = plt.subplots(figsize=(9, max(4, 0.4 * len(data) if hasattr(data, '__len__') else 4)))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            effect = dfn.iloc[:, 0].values
            se = np.abs(dfn.iloc[:, 1].values) if dfn.shape[1] >= 2 else np.ones(len(dfn))
            ci = 1.96 * se
            labels = data.index.astype(str).values if len(data.index) == len(effect) else np.arange(len(effect)).astype(str)
            y = np.arange(len(effect))
            ax.errorbar(effect, y, xerr=ci, fmt='o', color='steelblue', capsize=3,
                        markersize=6, elinewidth=1.5)
            ax.axvline(0, color='grey', ls='--', lw=1)
            ax.set_yticks(y)
            ax.set_yticklabels(labels, fontsize=8)
            ax.set_xlabel('Effect Size (95% CI)')
            ax.set_title('Forest Plot', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns\n(effect, se)', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Forest Plot\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_funnel_plot(data, output_path: str, **kwargs):
    """漏斗图（Funnel Plot）: 发表偏倚检验"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            effect = dfn.iloc[:, 0].values
            se = np.abs(dfn.iloc[:, 1].values) + 1e-10
            ax.scatter(effect, se, s=25, alpha=0.7, color='steelblue')
            # 漏斗轮廓
            pooled = np.average(effect, weights=1 / se**2)
            xs = np.linspace(effect.min() - 0.5, effect.max() + 0.5, 100)
            for k in [1.96, 2.58]:
                ax.plot(pooled + k * xs, xs, color='crimson', ls='--', lw=0.8, alpha=0.6)
                ax.plot(pooled - k * xs, xs, color='crimson', ls='--', lw=0.8, alpha=0.6)
            ax.axvline(pooled, color='grey', lw=1)
            ax.set_xlabel('Effect Size')
            ax.set_ylabel('Standard Error')
            ax.set_title('Funnel Plot', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Need >= 2 numeric columns\n(effect, se)', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'Funnel Plot\n(Requires DataFrame)', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    return output_path


def plot_volcano_sig(data, output_path: str, **kwargs):
    """带显著性标注的火山图（bar_sig 风格，组间差异）"""
    return plot_volcano(data, output_path, **kwargs)


# ==================== 主路由函数 ====================

def generate_figure(
    domain: str,
    plot_type: str,
    data: Any,
    output_path: str,
    **kwargs
) -> str:
    """
    零动手路由：根据领域和图型自动生成图表

    Args:
        domain: 领域名称，如 "scRNA", "general", "genome", "microbiome" 等
        plot_type: 图型名称，如 "UMAP", "heatmap", "box", "volcano" 等
        data: 数据（AnnData/pandas.DataFrame/np.ndarray等）
        output_path: 输出文件路径
        **kwargs: 其他参数

    Returns:
        输出文件路径
    """
    # 规范化输入
    domain = domain.lower().strip()
    plot_type = plot_type.lower().strip()

    # 构建输出路径
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 尝试精确匹配
    func = get_native_plot_function(domain, plot_type)
    if func:
        print(f"Using native function: {func.__name__}")
        return func(data, str(output_path), **kwargs)

    # 尝试模糊匹配（移除特殊字符，大小写不敏感）
    clean_domain = _normalize_key(domain)
    clean_type = _normalize_key(plot_type)

    for (d, p), f in ROUTING_TABLE.items():
        if clean_domain in _normalize_key(d) and clean_type in _normalize_key(p):
            func = getattr(sys.modules[__name__], f)
            print(f"Using fuzzy matched function: {func.__name__}")
            return func(data, str(output_path), **kwargs)

    # 默认：使用热图或散点图
    print(f"No specific function found for {domain}/{plot_type}, using fallback")
    if hasattr(data, 'X') and data.X is not None:
        return plot_heatmap(data, str(output_path), **kwargs)
    else:
        return plot_scatter(data, str(output_path), **kwargs)


def quick_plot(data, output_path: str, plot_type: str = "auto", **kwargs) -> str:
    """
    快速绘图：自动判断数据类型和最佳图型

    Args:
        data: 数据
        output_path: 输出路径
        plot_type: 图型（"auto"表示自动判断）
        **kwargs: 其他参数

    Returns:
        输出文件路径
    """
    # 自动判断数据类型
    if hasattr(data, 'obs') and 'louvain' in data.obs.columns:
        # 单细胞数据
        if plot_type == "auto":
            plot_type = "UMAP"
        return generate_figure("scRNA", plot_type, data, output_path, **kwargs)
    elif hasattr(data, 'var_names') and len(data.var_names) > 10:
        # 基因表达数据
        return generate_figure("scRNA", "heatmap", data, output_path, **kwargs)
    elif isinstance(data, pd.DataFrame):
        # 通用数据
        if plot_type == "auto":
            if len(data.columns) > 10:
                plot_type = "heatmap"
            elif 'group' in data.columns or 'class' in data.columns:
                plot_type = "box"
            else:
                plot_type = "bar"
        return generate_figure("general", plot_type, data, output_path, **kwargs)
    else:
        # 其他数据
        return plot_scatter(data, output_path, **kwargs)


if __name__ == "__main__":
    # 测试
    import scanpy as sc
    adata = sc.datasets.pbmc68k_reduced()
    print("Testing bioinfo_router...")
    output_dir = Path(__file__).parent.parent / "test_output"
    output_dir.mkdir(exist_ok=True)

    # 测试UMAP
    umap_path = output_dir / "test_umap.svg"
    generate_figure("scRNA", "UMAP", adata, umap_path, color="louvain")
    print(f"✓ UMAP saved to {umap_path}")

    # 测试热图
    heatmap_path = output_dir / "test_heatmap.svg"
    generate_figure("scRNA", "heatmap", adata, heatmap_path)
    print(f"✓ Heatmap saved to {heatmap_path}")

    # 测试快速绘图
    quick_path = output_dir / "test_quick.svg"
    quick_plot(adata, quick_path)
    print(f"✓ Quick plot saved to {quick_path}")

    print("\nAll tests passed!")
