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

    # ═══════════ 全领域扩展路由（70+ 领域） ═══════════
    # 多组学 / 整合
    ("multiomics", "heatmap"): "plot_heatmap",
    ("multiomics", "circos"): "plot_circos",
    ("multiomics", "correlation"): "plot_heatmap",
    ("multiomics", "sankey"): "plot_sankey",
    ("multiomics", "factor"): "plot_heatmap",
    ("multiomics", "network"): "plot_enrichment_network",
    ("multiomics", "complexheatmap"): "plot_heatmap",
    # 空间转录组
    ("spatial", "spot"): "plot_spatial",
    ("spatial", "spatial"): "plot_spatial",
    ("spatial", "umap"): "plot_umap",
    ("spatial", "tsne"): "plot_tsne",
    ("spatial", "heatmap"): "plot_heatmap",
    ("spatial", "marker"): "plot_marker",
    ("spatial", "cluster"): "plot_spatial",
    # 流式细胞术
    ("flow", "histogram"): "plot_flow_hist",
    ("flow", "density"): "plot_flow_hist",
    ("flow", "scatter"): "plot_scatter",
    ("flow", "contour"): "plot_hexbin",
    ("flow", "gating"): "plot_scatter",
    # 甲基化 / 表观
    ("methylation", "beta"): "plot_beta_dist",
    ("methylation", "heatmap"): "plot_heatmap",
    ("methylation", "dmp"): "plot_volcano",
    ("methylation", "differentially"): "plot_volcano",
    # 免疫组库
    ("immunology", "diversity"): "plot_alpha_diversity",
    ("immunology", "clonotype"): "plot_clonotype",
    ("immunology", "vdj"): "plot_clonotype",
    ("immunology", "repertoire"): "plot_clonotype",
    ("immunology", "heatmap"): "plot_heatmap",
    # 癌症基因组
    ("cancer", "oncoplot"): "plot_oncoplot",
    ("cancer", "oncoprint"): "plot_oncoplot",
    ("cancer", "mutation"): "plot_oncoplot",
    ("cancer", "survival"): "plot_km",
    ("cancer", "forest"): "plot_forest_plot",
    ("cancer", "tmb"): "plot_lollipop",
    ("cancer", "heatmap"): "plot_heatmap",
    # WGS / WES / 变异
    ("wgs", "variant"): "plot_variant",
    ("wgs", "cnv"): "plot_cnv",
    ("wgs", "manhattan"): "plot_manhattan",
    ("wgs", "coverage"): "plot_genome_track",
    # 蛋白 / 互作
    ("protein", "interaction"): "plot_ppi",
    ("protein", "ppi"): "plot_ppi",
    ("protein", "heatmap"): "plot_heatmap",
    ("protein", "volcano"): "plot_volcano",
    ("protein", "structure"): "plot_ppi",
    # RNA / 转录
    ("rna", "expression"): "plot_heatmap",
    ("rna", "volcano"): "plot_volcano",
    ("rna", "ma_plot"): "plot_ma_plot",
    ("rna", "alternative_splicing"): "plot_sashimi",
    ("rna", "sashimi"): "plot_sashimi",
    ("rna", "polyA"): "plot_ecdf",
    # 临床 / 队列
    ("clinical", "roc"): "plot_roc",
    ("clinical", "km"): "plot_km",
    ("clinical", "forest"): "plot_forest_plot",
    ("clinical", "nomogram"): "plot_forest_plot",
    ("clinical", "calibration"): "plot_calibration",
    ("clinical", "bland_altman"): "plot_bland_altman",
    # 药物 / 药理
    ("drug", "dose_response"): "plot_dose_response",
    ("drug", "ic50"): "plot_ic50",
    ("drug", "synergy"): "plot_dose_response",
    ("drug", "adme"): "plot_radar",
    # 细胞系 / 功能
    ("cellline", "proliferation"): "plot_line",
    ("cellline", "viability"): "plot_dose_response",
    ("cellline", "migration"): "plot_line",
    # 代谢通路
    ("metabolomics", "pathway_map"): "plot_pathway",
    ("metabolomics", "enrichment"): "plot_enrichment_dot",
    ("metabolomics", "heatmap"): "plot_heatmap",
    ("metabolomics", "oplsda"): "plot_plsda",
    # 微生物组扩展
    ("microbiome", "alpha"): "plot_alpha_diversity",
    ("microbiome", "beta"): "plot_beta_diversity",
    ("microbiome", "pcoa"): "plot_beta_diversity",
    ("microbiome", "nmds"): "plot_beta_diversity",
    ("microbiome", "lefse"): "plot_lollipop",
    ("microbiome", "network"): "plot_enrichment_network",
    ("microbiome", "picrust"): "plot_enrichment_bar",
    # 单细胞扩展
    ("scRNA", "spatial"): "plot_spatial",
    ("scRNA", "rna_velocity"): "plot_trajectory",
    ("scRNA", "pseudotime"): "plot_trajectory",
    ("scRNA", "monocle"): "plot_trajectory",
    ("scRNA", "aucell"): "plot_heatmap",
    ("scRNA", "gsea"): "plot_enrichment_bar",
    ("scRNA", "cell_cycle"): "plot_scatter",
    ("scRNA", "proportion"): "plot_donut",
    ("scRNA", "composition"): "plot_stacked_area",
    ("scRNA", "doublet"): "plot_scatter",
    ("scRNA", "integration"): "plot_umap",
    # bulkRNA 扩展
    ("bulkRNA", "volcano"): "plot_volcano",
    ("bulkRNA", "heatmap"): "plot_heatmap",
    ("bulkRNA", "gsea"): "plot_enrichment_bar",
    ("bulkRNA", "kegg"): "plot_enrichment_dot",
    ("bulkRNA", "go"): "plot_enrichment_dot",
    ("bulkRNA", "wgcna"): "plot_heatmap",
    ("bulkRNA", "timeseries"): "plot_line",
    ("bulkRNA", "correlation"): "plot_heatmap",
    ("bulkRNA", "venn"): "plot_venn_simple",
    ("bulkRNA", "upset"): "plot_upset_simple",
    # 系统发育扩展
    ("phylogeny", "heatmap"): "plot_heatmap",
    ("phylogeny", "timeline"): "plot_line",
    ("phylogeny", "ancestral"): "plot_heatmap",
    # 富集扩展
    ("enrichment", "gsea"): "plot_enrichment_bar",
    ("enrichment", "kegg"): "plot_enrichment_dot",
    ("enrichment", "go"): "plot_enrichment_dot",
    ("enrichment", "ridge"): "plot_ridgeline",
    ("enrichment", "cnet"): "plot_enrichment_network",
    # 表观扩展
    ("epigenetic", "heatmap"): "plot_heatmap",
    ("epigenetic", "motif"): "plot_motif",
    ("epigenetic", "peaks"): "plot_genome_track",
    ("epigenetic", "footprint"): "plot_line",
    ("epigenetic", "nucleosome"): "plot_line",
    # 基因组扩展
    ("genome", "ideogram"): "plot_circos",
    ("genome", "heatmap"): "plot_heatmap",
    ("genome", "variant"): "plot_variant",
    ("genome", "loh"): "plot_cnv",
    # 生存扩展
    ("survival", "km"): "plot_km",
    ("survival", "cox"): "plot_forest_plot",
    ("survival", "roc"): "plot_roc",
    ("survival", "calibration"): "plot_calibration",
    ("survival", "nomogram"): "plot_forest_plot",
    # 代谢组扩展
    ("metabolomics", "volcano"): "plot_volcano",
    ("metabolomics", "plsda"): "plot_plsda",
    ("metabolomics", "pathway"): "plot_pathway",
    # 蛋白组扩展
    ("proteomics", "volcano"): "plot_volcano",
    ("proteomics", "heatmap"): "plot_heatmap",
    ("proteomics", "venn"): "plot_venn_simple",
    ("proteomics", "network"): "plot_ppi",
    ("proteomics", "coverage"): "plot_lollipop",
    # 常规扩展
    ("general", "roc"): "plot_roc",
    ("general", "calibration"): "plot_calibration",
    ("general", "venn"): "plot_venn_simple",
    ("general", "upset"): "plot_upset_simple",
    ("general", "motif"): "plot_motif",
    ("general", "sashimi"): "plot_sashimi",
    ("general", "spatial"): "plot_spatial",
    ("general", "oncoplot"): "plot_oncoplot",
    ("general", "ppi"): "plot_ppi",
    ("general", "dose_response"): "plot_dose_response",
    ("general", "ic50"): "plot_ic50",
    ("general", "clonotype"): "plot_clonotype",
}

# 从 chart_catalog 反向生成的全领域自动路由（领域 → 推荐图型 → 函数）
AUTO_FULL_ROUTING = {}


def _build_auto_routing():
    """从 chart_catalog + 70 领域配置反向生成路由：任何领域+图型都能路由"""
    global AUTO_FULL_ROUTING
    try:
        from chart_catalog import suggest_for_domain
        domain_list = ["scRNA", "bulkRNA", "microbiome", "metabolomics", "proteomics",
                       "genome", "phylogeny", "survival", "enrichment", "epigenetic",
                       "multiomics", "spatial", "flow", "immunology", "cancer",
                       "wgs", "protein", "rna", "clinical", "drug", "cellline", "general"]
        for domain in domain_list:
            for fig in suggest_for_domain(domain, top_n=30):
                key = (domain, fig)
                if key not in ROUTING_TABLE:
                    AUTO_FULL_ROUTING[key] = _resolve_function_name(fig)
    except Exception:
        pass
    # 合并 70 领域路由配置（bioinfo_70_domains_process.md 程序化生成）
    try:
        from domains_70_config import DOMAINS_70_ROUTING, KDENSE_DISCIPLINE_ROUTING
        for domain, figs in DOMAINS_70_ROUTING.items():
            for fig in figs:
                key = (domain, fig)
                if key not in ROUTING_TABLE:
                    AUTO_FULL_ROUTING[key] = _resolve_function_name(fig)
        # 合并 K-Dense 22 学科路由
        for domain, figs in KDENSE_DISCIPLINE_ROUTING.items():
            for fig in figs:
                key = (domain, fig)
                if key not in ROUTING_TABLE:
                    AUTO_FULL_ROUTING[key] = _resolve_function_name(fig)
    except Exception:
        pass


def _resolve_function_name(fig: str) -> str:
    """图型 → 已有绘图函数名（别名映射）"""
    alias = {
        "boxplot": "plot_box", "histogram": "plot_box", "kde": "plot_violin",
        "stripplot": "plot_scatter", "beeswarm": "plot_scatter", "ecdf": "plot_ecdf",
        "qqplot": "plot_qqplot", "bar": "plot_bar", "grouped_bar": "plot_bar",
        "stacked_bar": "plot_bar", "lollipop": "plot_lollipop", "dumbbell": "plot_dumbbell",
        "dotplot": "plot_dotplot", "slope": "plot_line", "waterfall": "plot_diverging_bar",
        "errorbar": "plot_bar", "scatter": "plot_scatter", "bubble": "plot_bubble",
        "hexbin": "plot_hexbin", "corr_heatmap": "plot_heatmap", "pairplot": "plot_pairplot",
        "parallel_coords": "plot_parallel_coords", "line": "plot_line", "area": "plot_area",
        "stacked_area": "plot_stacked_area", "step_line": "plot_line", "pie": "plot_pie",
        "donut": "plot_donut", "treemap": "plot_treemap", "sunburst": "plot_donut",
        "nightingale": "plot_nightingale", "waffle": "plot_waffle", "marimekko": "plot_treemap",
        "circle_packing": "plot_treemap", "sankey": "plot_sankey", "network_graph": "plot_enrichment_network",
        "dendrogram": "plot_dendrogram", "chord_diagram": "plot_circos", "arc_diagram": "plot_circos",
        "alluvial": "plot_sankey", "wordcloud": "plot_bar", "venn": "plot_venn_simple",
        "choropleth": "plot_heatmap", "bubble_map": "plot_bubble", "umap_plot": "plot_umap",
        "tsne_plot": "plot_tsne", "pca_plot": "plot_pca", "manhattan_plot": "plot_manhattan",
        "forest_plot": "plot_forest_plot", "funnel_plot": "plot_funnel_plot",
        "calibration_curve": "plot_calibration", "residual_plot": "plot_scatter",
        "upset_plot": "plot_upset_simple", "scatter_3d": "plot_bubble", "surface_3d": "plot_heatmap",
        "bar_3d": "plot_bar", "jade_ring": "plot_nightingale", "bar_sig": "plot_bar",
        "radial_bar_sig": "plot_radial_bar", "radial_bar": "plot_radial_bar",
        "violin": "plot_violin", "heatmap": "plot_heatmap", "volcano": "plot_volcano",
        "ridgeline": "plot_ridgeline", "raincloud": "plot_raincloud", "radar": "plot_radar",
        "marginal_plot": "plot_marginal_plot", "bland_altman": "plot_bland_altman",
        "diverging_bar": "plot_diverging_bar", "ma_plot": "plot_ma_plot",
        "km": "plot_km", "forest": "plot_forest_plot", "roc_curve": "plot_roc",
        "kaplan_meier": "plot_km", "manhattan": "plot_manhattan", "pca": "plot_pca",
        "umap": "plot_umap", "tsne": "plot_tsne", "gsea": "plot_enrichment_bar",
        "kegg_pathway": "plot_enrichment_dot", "enrichment_bar": "plot_enrichment_bar",
        "enrichment_dot": "plot_enrichment_dot", "alpha_diversity": "plot_alpha_diversity",
        "beta_diversity": "plot_beta_diversity", "composition": "plot_composition",
        "lefse": "plot_lollipop", "marker": "plot_marker", "clustree": "plot_clustree",
        "trajectory": "plot_trajectory", "cellchat": "plot_cellchat",
        "genome_browser": "plot_genome_browser", "genome_track": "plot_genome_track",
        "cnv": "plot_cnv", "circos": "plot_circos", "tree": "plot_tree",
        "circle_tree": "plot_circle_tree", "pathway": "plot_pathway",
        "plsda": "plot_plsda", "oplsda": "plot_plsda", "peaks": "plot_genome_track",
        "motif": "plot_motif", "wgcna": "plot_heatmap", "mofa": "plot_heatmap",
        "spatial": "plot_spatial", "flow_hist": "plot_flow_hist", "beta_dist": "plot_beta_dist",
        "clonotype": "plot_clonotype", "oncoplot": "plot_oncoplot", "variant": "plot_variant",
        "ppi": "plot_ppi", "roc": "plot_roc", "calibration": "plot_calibration",
        "dose_response": "plot_dose_response", "ic50": "plot_ic50", "sashimi": "plot_sashimi",
        # K-Dense 技能图型别名（163 技能映射）
        "3d_scatter": "plot_bubble", "beeswarm": "plot_scatter", "stripplot": "plot_scatter",
        "waterfall": "plot_diverging_bar", "surf": "plot_heatmap", "raster": "plot_heatmap",
        "density": "plot_violin", "plot": "plot_line", "contour": "plot_hexbin",
        "coverage": "plot_genome_track", "grn": "plot_enrichment_network",
        "hic": "plot_heatmap", "annotation": "plot_heatmap", "chromatin": "plot_heatmap",
        "infographics": "plot_bar", "scientific_schematic": "plot_enrichment_network",
        "residual_plot": "plot_scatter", "dendrogram": "plot_dendrogram",
        "parity_plot": "plot_scatter", "kegg_pathway": "plot_enrichment_dot",
        "chord_diagram": "plot_circos", "arc_diagram": "plot_circos",
        "corr_heatmap": "plot_heatmap", "complexheatmap": "plot_heatmap",
        "enrichment_network": "plot_enrichment_network", "gsea": "plot_enrichment_bar",
        "nomogram": "plot_forest_plot", "alpha_diversity": "plot_alpha_diversity",
        "beta_diversity": "plot_beta_diversity", "cellchat": "plot_cellchat",
        "trajectory": "plot_trajectory", "marker": "plot_marker",
    }
    return alias.get(fig, "plot_heatmap")


_build_auto_routing()


def _normalize_key(s: str) -> str:
    """规范化路由键：小写 + 去特殊字符"""
    return s.lower().strip().replace('-', '').replace('_', '').replace(' ', '')
def _all_routing():
    """合并路由表：基础 ROUTING_TABLE（含全领域扩展条目） + 自动反向生成"""
    merged = dict(ROUTING_TABLE)
    merged.update(AUTO_FULL_ROUTING)
    return merged


def get_native_plot_function(domain: str, plot_type: str):
    """获取原生Python绘图函数（大小写不敏感，覆盖全领域路由）"""
    d = _normalize_key(domain)
    p = _normalize_key(plot_type)
    for (rd, rp), func_name in _all_routing().items():
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
        # 只取数值列（容忍混合类型表）
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] == 0:
            ax.text(0.5, 0.5, 'No numeric columns for heatmap', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        im = ax.imshow(dfn.values, cmap='viridis', aspect='auto')
        ax.set_xticks(range(dfn.shape[1]))
        ax.set_xticklabels(dfn.columns, rotation=45, ha='right')
        ax.set_yticks(range(min(50, dfn.shape[0])))
        ax.set_yticklabels(list(dfn.index)[:50], fontsize=6)
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
            num_cols = data.select_dtypes(include=[np.number]).columns
            if len(num_cols) == 0:
                ax.text(0.5, 0.5, 'No numeric columns', ha='center', va='center')
            else:
                for col in num_cols:
                    ax.boxplot(data[col].dropna(), positions=[list(num_cols).index(col)+1])
                ax.set_xticks(range(1, len(num_cols)+1))
                ax.set_xticklabels(num_cols, rotation=45)
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
            dfn = data.select_dtypes(include=[np.number])
            if dfn.shape[1] == 0:
                ax.text(0.5, 0.5, 'No numeric columns', ha='center', va='center')
            else:
                dfn.mean().plot.bar(ax=ax, **kwargs)
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
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] == 0:
            ax.text(0.5, 0.5, 'No numeric columns', ha='center', va='center')
            plt.tight_layout(); plt.savefig(output_path, bbox_inches='tight', dpi=300); plt.close()
            return output_path
        im = ax.imshow(dfn.values, cmap='viridis', aspect='auto')
        ax.set_xticks(range(dfn.shape[1]))
        ax.set_xticklabels(dfn.columns, rotation=45, ha='right')
        ax.set_yticks(range(min(50, dfn.shape[0])))
        ax.set_yticklabels(list(dfn.index)[:50], fontsize=6)
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


# ═════════════════════════════════════════════════════════════
# 全领域新增绘图函数（空间/流式/甲基化/免疫/癌症/WGS/蛋白/临床/药物）
# ═════════════════════════════════════════════════════════════

def plot_spatial(data, output_path: str, x: str = None, y: str = None,
                 color: str = None, **kwargs):
    """空间转录组：组织切片 2D 坐标散点 + 基因表达颜色"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 7))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        xc = x or next((c for c in num_cols if c.lower() in ["x", "xcoord", "col", "pxl_col"]), None)
        yc = y or next((c for c in num_cols if c.lower() in ["y", "ycoord", "row", "pxl_row"]), None)
        if xc and yc:
            cc = color or next((c for c in num_cols if c != xc and c != yc), None)
            xs = pd.to_numeric(data[xc], errors="coerce").values
            ys = pd.to_numeric(data[yc], errors="coerce").values
            valid = ~(np.isnan(xs) | np.isnan(ys))
            if cc:
                sc = ax.scatter(xs[valid], ys[valid], s=12, alpha=0.8,
                                c=data[cc].values[valid], cmap="inferno")
                plt.colorbar(sc, ax=ax, label=cc, shrink=0.7)
            else:
                ax.scatter(xs[valid], ys[valid], s=12, alpha=0.8, color="steelblue")
            ax.set_xlabel(xc); ax.set_ylabel(yc)
            ax.set_aspect("equal", adjustable="box")
            ax.set_title("Spatial Transcriptomics", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Spatial\n(Requires x/y coordinate columns)",
                    ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Spatial\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_flow_hist(data, output_path: str, x: str = None, group_col: str = None, **kwargs):
    """流式细胞术：分组密度直方叠加"""
    fig, ax = plt.subplots(figsize=(8, 5))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        xc = x or (num_cols[0] if num_cols else None)
        gc = group_col or next((c for c in data.columns if pd.api.types.is_object_dtype(data[c])
                                or (data[c].nunique() <= 6 and data[c].nunique() > 1)), None)
        if xc:
            if gc:
                groups = data[gc].unique()
                for i, g in enumerate(groups):
                    vals = pd.to_numeric(data.loc[data[gc] == g, xc], errors="coerce").dropna().values
                    ax.hist(vals, bins=60, alpha=0.45, density=True,
                            color=plt.cm.tab10(i), label=str(g))
                ax.legend(frameon=False)
            else:
                vals = pd.to_numeric(data[xc], errors="coerce").dropna().values
                ax.hist(vals, bins=60, alpha=0.7, density=True, color="steelblue")
            ax.set_xlabel(xc); ax.set_ylabel("Density")
            ax.set_title("Flow Cytometry Histogram", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "No numeric column", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Flow Hist\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_beta_dist(data, output_path: str, **kwargs):
    """甲基化：β 值分布密度图"""
    fig, ax = plt.subplots(figsize=(8, 5))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)[:8]
        if num_cols:
            for c in num_cols:
                vals = pd.to_numeric(data[c], errors="coerce").dropna().values
                vals = vals[(vals > 0) & (vals < 1)]
                if len(vals) > 10:
                    ax.hist(vals, bins=40, alpha=0.4, density=True, label=c)
            ax.legend(frameon=False, fontsize=7)
            ax.set_xlabel("Beta value"); ax.set_ylabel("Density")
            ax.set_title("Methylation Beta Distribution", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "No numeric columns", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Beta Dist\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_clonotype(data, output_path: str, **kwargs):
    """免疫组库：克隆型占比（Top N 克隆型堆叠/环形）"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        if "frequency" in data.columns and "clonotype" in data.columns:
            dfx = data.sort_values("frequency", ascending=False).head(15)
            labels = dfx["clonotype"].astype(str).values
            vals = dfx["frequency"].values
        elif "clonotype" in data.columns:
            vc = data["clonotype"].value_counts().head(15)
            labels = vc.index.astype(str).values
            vals = vc.values
        elif data.shape[1] >= 2 and pd.api.types.is_numeric_dtype(data.iloc[:, -1]):
            dfn = data.select_dtypes(include=[np.number])
            vals = dfn.iloc[0].sort_values(ascending=False).head(15).values
            labels = dfn.iloc[0].sort_values(ascending=False).head(15).index.astype(str).values
        else:
            ax.text(0.5, 0.5, "Clonotype\n(Requires clonotype column)", ha="center", va="center")
            plt.tight_layout(); plt.savefig(output_path, bbox_inches="tight", dpi=300); plt.close()
            return output_path
        colors = plt.cm.viridis(np.linspace(0, 0.9, len(labels)))
        ax.bar(np.arange(len(labels)), vals, color=colors, alpha=0.9)
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=60, ha="right", fontsize=7)
        ax.set_ylabel("Frequency / Count")
        ax.set_title("TCR/BCR Clonotype Repertoire", fontweight="bold")
    else:
        ax.text(0.5, 0.5, "Clonotype\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_oncoplot(data, output_path: str, **kwargs):
    """癌症基因组：Oncoplot 突变谱（样本 × 基因 tile 图）"""
    fig, ax = plt.subplots(figsize=(12, max(4, 0.35 * data.shape[0] if hasattr(data, "shape") else 5)))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        if len(num_cols) >= 2:
            mat = data[num_cols[:20]].fillna(0).values
            genes = num_cols[:20]
            samples = [f"S{i}" for i in range(mat.shape[0])]
            im = ax.imshow(mat.T, cmap="YlOrRd", aspect="auto")
            ax.set_xticks(np.arange(mat.shape[0]))
            ax.set_xticklabels(samples, rotation=90, fontsize=6)
            ax.set_yticks(np.arange(len(genes)))
            ax.set_yticklabels(genes, fontsize=8)
            plt.colorbar(im, ax=ax, shrink=0.5)
            ax.set_title("Oncoplot (Mutation Spectrum)", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Oncoplot\n(Requires >=2 numeric columns)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Oncoplot\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_variant(data, output_path: str, **kwargs):
    """WGS/WES：变异类型计数条形图"""
    fig, ax = plt.subplots(figsize=(9, 5))
    if isinstance(data, pd.DataFrame):
        type_col = next((c for c in data.columns if c.lower() in ["type", "variant_type", "effect", "class"]), None)
        if type_col:
            vc = data[type_col].value_counts().head(12)
            ax.bar(np.arange(len(vc)), vc.values, color="steelblue", alpha=0.9)
            ax.set_xticks(np.arange(len(vc)))
            ax.set_xticklabels(vc.index.astype(str), rotation=45, ha="right")
            ax.set_ylabel("Count"); ax.set_title("Variant Type Spectrum", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Variant\n(Requires type/effect column)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Variant\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_ppi(data, output_path: str, **kwargs):
    """蛋白互作网络：简化弹簧布局网络图"""
    try:
        import networkx as nx
    except ImportError:
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.text(0.5, 0.5, "PPI requires networkx", ha="center", va="center")
        plt.tight_layout(); plt.savefig(output_path, bbox_inches="tight", dpi=300); plt.close()
        return output_path
    fig, ax = plt.subplots(figsize=(9, 7))
    G = nx.Graph()
    if isinstance(data, pd.DataFrame):
        if data.shape[1] >= 2:
            for _, row in data.head(80).iterrows():
                a, b = str(row.iloc[0]), str(row.iloc[1])
                w = float(row.iloc[2]) if data.shape[1] >= 3 else 1.0
                try:
                    G.add_edge(a, b, weight=w)
                except Exception:
                    pass
        else:
            for i in range(min(40, len(data))):
                G.add_edge(f"P{i}", f"P{(i + 1) % 40}")
    else:
        ax.text(0.5, 0.5, "PPI\n(Requires DataFrame edge list)", ha="center", va="center")
        plt.tight_layout(); plt.savefig(output_path, bbox_inches="tight", dpi=300); plt.close()
        return output_path
    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "PPI: empty network", ha="center", va="center")
        plt.tight_layout(); plt.savefig(output_path, bbox_inches="tight", dpi=300); plt.close()
        return output_path
    pos = nx.spring_layout(G, seed=42, k=0.6)
    weights = [G[u][v].get("weight", 1) for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35, width=[0.5 + 2 * min(w, 3) for w in weights])
    deg = dict(G.degree())
    node_colors = [deg.get(n, 1) for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=250, node_color=node_colors,
                           cmap="viridis", alpha=0.9)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7)
    ax.set_title("Protein-Protein Interaction Network", fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_roc(data, output_path: str, y_true: str = None, y_score: str = None, **kwargs):
    """ROC 曲线（临床/生存模型评估）"""
    try:
        from sklearn.metrics import roc_curve, auc
    except ImportError:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, "ROC requires sklearn", ha="center", va="center")
        plt.tight_layout(); plt.savefig(output_path, bbox_inches="tight", dpi=300); plt.close()
        return output_path
    fig, ax = plt.subplots(figsize=(6, 6))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        yt = y_true or next((c for c in data.columns if c.lower() in ["y_true", "label", "event", "status"]), None)
        if yt and len(num_cols) > 0:
            y_true_vals = pd.to_numeric(data[yt], errors="coerce").values
            for col in num_cols[:4]:
                if col == yt:
                    continue
                score = pd.to_numeric(data[col], errors="coerce").values
                valid = ~(np.isnan(y_true_vals) | np.isnan(score))
                if np.unique(y_true_vals[valid]).size < 2:
                    continue
                fpr, tpr, _ = roc_curve(y_true_vals[valid], score[valid])
                ax.plot(fpr, tpr, lw=2, label=f"{col} (AUC={auc(fpr, tpr):.3f})")
            ax.plot([0, 1], [0, 1], "k--", lw=1)
            ax.legend(frameon=False, fontsize=8)
            ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
            ax.set_title("ROC Curve", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "ROC\n(Requires y_true + score columns)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "ROC\n(Requires DataFrame)", ha="center", va="center")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_calibration(data, output_path: str, **kwargs):
    """校准曲线（预测概率 vs 观测频率）"""
    fig, ax = plt.subplots(figsize=(6, 6))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        pred_col = next((c for c in num_cols if "pred" in c.lower()), None)
        obs_col = next((c for c in num_cols if "obs" in c.lower() or "actual" in c.lower()), None)
        if pred_col and obs_col:
            pred = pd.to_numeric(data[pred_col], errors="coerce").values
            obs = pd.to_numeric(data[obs_col], errors="coerce").values
            valid = ~(np.isnan(pred) | np.isnan(obs))
            bins = np.linspace(0, 1, 11)
            idx = np.digitize(pred[valid], bins) - 1
            means = []
            for b in range(10):
                m = obs[valid][idx == b]
                means.append(np.mean(m) if len(m) > 0 else np.nan)
            ax.plot(bins[:-1] + 0.05, means, "o-", color="steelblue", lw=2)
            ax.plot([0, 1], [0, 1], "k--", lw=1)
            ax.set_xlabel("Predicted Probability"); ax.set_ylabel("Observed Frequency")
            ax.set_title("Calibration Curve", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Calibration\n(Requires pred+obs columns)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Calibration\n(Requires DataFrame)", ha="center", va="center")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_dose_response(data, output_path: str, **kwargs):
    """药物剂量-响应 S 曲线（多化合物）"""
    fig, ax = plt.subplots(figsize=(8, 6))
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        if len(num_cols) >= 2:
            dose = num_cols[0]
            xd = pd.to_numeric(data[dose], errors="coerce").values
            for i, col in enumerate(num_cols[1:6]):
                yd = pd.to_numeric(data[col], errors="coerce").values
                valid = ~(np.isnan(xd) | np.isnan(yd))
                order = np.argsort(xd[valid])
                ax.plot(xd[valid][order], yd[valid][order], "o-", lw=2,
                        color=plt.cm.tab10(i), label=col)
            ax.legend(frameon=False, fontsize=8)
            ax.set_xlabel(dose); ax.set_ylabel("Response (%)")
            ax.set_title("Dose-Response Curve", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Dose-Response\n(Requires dose+response cols)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Dose-Response\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_ic50(data, output_path: str, **kwargs):
    """IC50 比较（化合物 IC50 棒棒糖/柱状）"""
    fig, ax = plt.subplots(figsize=(8, 5))
    if isinstance(data, pd.DataFrame):
        ic_col = next((c for c in data.columns if "ic50" in c.lower() or "ic50" in c.lower()), None)
        if ic_col:
            dfx = data.sort_values(ic_col)
            labels = dfx.iloc[:, 0].astype(str).values if data.shape[1] > 1 else dfx.index.astype(str).values
            vals = pd.to_numeric(dfx[ic_col], errors="coerce").values
            y = np.arange(len(labels))
            ax.barh(y, vals, color="crimson", alpha=0.85)
            ax.set_yticks(y); ax.set_yticklabels(labels)
            ax.set_xlabel("IC50"); ax.set_title("IC50 Comparison", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "IC50\n(Requires ic50 column)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "IC50\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_sashimi(data, output_path: str, **kwargs):
    """剪接事件（Sashimi 简化版）：外显子连接计数"""
    fig, ax = plt.subplots(figsize=(10, 4))
    if isinstance(data, pd.DataFrame):
        dfn = data.select_dtypes(include=[np.number])
        if dfn.shape[1] >= 2:
            xd = np.arange(len(data))
            for i, col in enumerate(dfn.columns[:6]):
                ax.plot(xd, dfn[col].values, lw=1.5, label=col,
                        color=plt.cm.tab10(i), alpha=0.7)
            ax.legend(frameon=False, fontsize=8)
            ax.set_title("Splicing Junction (Sashimi-like)", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Sashimi\n(Requires junction counts)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Sashimi\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_venn_simple(data, output_path: str, **kwargs):
    """韦恩图（2-3 组集合交集，matplotlib 圆）"""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    sets = {}
    if isinstance(data, pd.DataFrame):
        obj_cols = [c for c in data.columns if not pd.api.types.is_numeric_dtype(data[c])
                    or data[c].nunique() <= 2]
        for c in obj_cols[:3]:
            vals = set(data[c].dropna().astype(str).unique())
            if vals and str(vals) not in {"{'nan'}", "{'True'}", "{'False'}", "{'0'}", "{'1'}"}:
                sets[c] = vals
        if len(sets) < 2:
            # 退化为数值列分布
            num_cols = list(data.select_dtypes(include=[np.number]).columns)
            if len(num_cols) >= 2:
                for c in num_cols[:3]:
                    sets[c] = set(data[c].head(30).round(2).astype(str).values)
    if len(sets) == 2:
        names = list(sets)
        a, b = sets[names[0]], sets[names[1]]
        r = 2.2
        c1, c2 = (4.0, 5.0), (6.0, 5.0)
        circle1 = plt.Circle(c1, r, color="steelblue", alpha=0.35)
        circle2 = plt.Circle(c2, r, color="crimson", alpha=0.35)
        ax.add_patch(circle1); ax.add_patch(circle2)
        only_a = len(a - b); inter = len(a & b); only_b = len(b - a)
        ax.text(c1[0] - r / 1.6, 5.0, str(only_a), ha="center", fontsize=16)
        ax.text(5.0, 5.0, str(inter), ha="center", fontsize=16)
        ax.text(c2[0] + r / 1.6, 5.0, str(only_b), ha="center", fontsize=16)
        ax.text(c1[0], 9.2, names[0], ha="center", fontsize=12)
        ax.text(c2[0], 9.2, names[1], ha="center", fontsize=12)
        ax.set_title("Venn Diagram", fontweight="bold")
    elif len(sets) == 3:
        names = list(sets)
        circles = [(4.5, 6.2), (5.5, 6.2), (5.0, 4.4)]
        colors = ["steelblue", "crimson", "gold"]
        for (cx, cy), col, name in zip(circles, colors, names):
            ax.add_patch(plt.Circle((cx, cy), 1.8, color=col, alpha=0.35))
            ax.text(cx, cy + 2.4, name, ha="center", fontsize=11)
        a, b, c = sets.values()
        regs = {
            "abc": a & b & c,
        }
        ax.text(5.0, 5.4, str(len(regs["abc"])), ha="center", fontsize=14)
        ax.set_title("Venn Diagram (3-way)", fontweight="bold")
    else:
        ax.text(0.5, 0.5, "Venn\n(Requires >=2 set columns)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_upset_simple(data, output_path: str, **kwargs):
    """UpSet 图（简化）：集合交集条形 + 点阵"""
    fig, ax = plt.subplots(figsize=(10, 5))
    if isinstance(data, pd.DataFrame):
        obj_cols = [c for c in data.columns if not pd.api.types.is_numeric_dtype(data[c])
                    or data[c].nunique() <= 2][:5]
        if len(obj_cols) >= 3:
            masks = []
            names = []
            for c in obj_cols:
                vals = data[c].dropna().astype(str)
                if vals.nunique() >= 2 and vals.nunique() <= 8:
                    masks.append(set(vals.unique()))
                    names.append(c)
            if len(masks) >= 3:
                from itertools import combinations
                inter_sizes = []
                combos = []
                for r in range(1, len(masks) + 1):
                    for combo in combinations(range(len(masks)), r):
                        inter = set.intersection(*[masks[i] for i in combo]) if r > 1 else set(masks[combo[0]])
                        combos.append(combo)
                        inter_sizes.append(len(inter))
                order = np.argsort(inter_sizes)[::-1][:15]
                ax.bar(np.arange(len(order)), [inter_sizes[i] for i in order],
                       color="steelblue", alpha=0.9)
                ax.set_xticks([])
                ax.set_ylabel("Intersection Size")
                ax.set_title("UpSet Plot (Simplified)", fontweight="bold")
            else:
                ax.text(0.5, 0.5, "UpSet\n(Need >=3 set-like columns)", ha="center", va="center")
        else:
            ax.text(0.5, 0.5, "UpSet\n(Need >=3 categorical columns)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "UpSet\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


def plot_motif(data, output_path: str, **kwargs):
    """转录因子 Motif 富集（简化）：Top motif 条形"""
    fig, ax = plt.subplots(figsize=(9, 5))
    if isinstance(data, pd.DataFrame):
        name_col = next((c for c in data.columns if c.lower() in ["motif", "tf", "name", "factor"]), None)
        p_col = next((c for c in data.columns if c.lower() in ["p", "pvalue", "q", "fdr"]), None)
        if name_col:
            dfx = data.copy()
            if p_col:
                dfx["_score"] = -np.log10(pd.to_numeric(dfx[p_col], errors="coerce").fillna(1) + 1e-20)
                dfx = dfx.sort_values("_score", ascending=False).head(15)
                ax.barh(np.arange(len(dfx)), dfx["_score"].values, color="steelblue", alpha=0.9)
                ax.set_xlabel("-log10(p)")
            else:
                dfx = dfx.head(15)
                ax.barh(np.arange(len(dfx)), np.ones(len(dfx)), color="steelblue", alpha=0.9)
            ax.set_yticks(np.arange(len(dfx)))
            ax.set_yticklabels(dfx[name_col].astype(str).values, fontsize=8)
            ax.set_title("Transcription Factor Motif Enrichment", fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Motif\n(Requires motif/tf column)", ha="center", va="center")
    else:
        ax.text(0.5, 0.5, "Motif\n(Requires DataFrame)", ha="center", va="center")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    return output_path


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

    for (d, p), f in _all_routing().items():
        if clean_domain in _normalize_key(d) and clean_type in _normalize_key(p):
            func = getattr(sys.modules[__name__], f)
            print(f"Using fuzzy matched function: {func.__name__}")
            return func(data, str(output_path), **kwargs)

    # 尝试同图型跨领域匹配（如 volcano 在任意领域都可用）
    for (d, p), f in _all_routing().items():
        if clean_type == _normalize_key(p) and clean_type in ["volcano", "heatmap", "box",
                                                               "violin", "scatter", "line",
                                                               "bar", "donut", "treemap",
                                                               "sankey", "dendrogram", "qqplot",
                                                               "ecdf", "ridgeline", "raincloud",
                                                               "lollipop", "bubble", "hexbin",
                                                               "radar", "ma_plot", "forest_plot",
                                                               "manhattan", "pca", "umap", "tsne",
                                                               "km", "roc", "spatial", "ppi"]:
            func = getattr(sys.modules[__name__], f)
            print(f"Using cross-domain matched function: {func.__name__}")
            return func(data, str(output_path), **kwargs)

    # 尝试图表目录引擎匹配（chart_catalog 中任意图型都能路由）
    try:
        from chart_catalog import get_chart
        meta = get_chart(plot_type)
        if meta:
            func_name = _resolve_function_name(meta.get("id", plot_type))
            if hasattr(sys.modules[__name__], func_name):
                func = getattr(sys.modules[__name__], func_name)
                print(f"Using catalog-resolved function: {func.__name__}")
                return func(data, str(output_path), **kwargs)
    except Exception:
        pass

    # 默认：使用热图或散点图
    print(f"No specific function found for {domain}/{plot_type}, using fallback")
    if hasattr(data, 'X') and data.X is not None:
        return plot_heatmap(data, str(output_path), **kwargs)
    else:
        return plot_scatter(data, str(output_path), **kwargs)


def plot_mechanism_diagram(data: dict, output_path: str, **kwargs) -> str:
    """
    BioRender 风格机制示意图（可编辑矢量）。
    输入 dict：
      {
        "entities": [{"name": "...", "type": "treatment|target|pathway|cell|phenotype",
                       "evidence": "experiment|database|prediction|literature", "level": 0}],
        "relations": [{"from": "...", "to": "...", "type": "activates|inhibits|produces|translocates", "label": "..."}],
        "mechanism": "总体一句话（可选，画在顶部）"
      }
    或 DataFrame：列 = [entity, type, level, evidence] + 关系在 kwargs["relations"]
    输出：SVG/PDF/PNG/TIFF（自动多格式）
    """
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon

    entities = list(data.get("entities", []))
    relations = list(data.get("relations", []))
    mechanism = data.get("mechanism", "")

    # 兼容 DataFrame 输入
    if isinstance(entities, pd.DataFrame):
        entities = entities.to_dict("records")
    if isinstance(relations, pd.DataFrame):
        relations = relations.to_dict("records")

    if not entities:
        # 空输入：画占位说明
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Mechanism diagram: provide entities + relations", ha="center", fontsize=12)
        ax.axis("off")
        _save_multi(base := str(Path(output_path).with_suffix("")), fig)
        plt.close(fig)
        return str(Path(output_path).with_suffix(".svg"))

    # 类型配色（BioRender 风格：温和高对比）
    TYPE_COLOR = {
        "treatment":  "#2E75B6",   # 干预 蓝
        "target":     "#C0392B",   # 靶点/分子 红
        "pathway":    "#2CA02C",   # 通路 绿
        "cell":       "#8E44AD",   # 细胞 紫
        "phenotype":  "#D4AC0D",   # 表型 金
        "metabolite": "#E67E22",   # 代谢物 橙
        "bacteria":   "#1F4E79",   # 菌 深蓝
        "protein":    "#B03A2E",   # 蛋白 深红
    }
    TYPE_LIGHT = {
        "treatment":  "#D6EAF8", "target": "#FADBD8", "pathway": "#D5F5E3",
        "cell":       "#E8DAEF", "phenotype": "#FCF3CF", "metabolite": "#FDEBD0",
        "bacteria":   "#D4E6F1", "protein": "#F5B7B1",
    }
    EV_SUFFIX = {"experiment": "*", "database": "†", "prediction": "‡", "literature": "§"}

    # 分层布局：按 level 从左到右（保证节点不重叠、箭头有空间）
    n = len(entities)
    levels = {}
    for e in entities:
        lv = e.get("level", 0)
        levels.setdefault(lv, []).append(e)
    max_lv = max(levels.keys()) if levels else 0
    n_cols = max_lv + 1
    max_rows = max(len(v) for v in levels.values()) if levels else 1
    col_w, row_h = 2.6, 1.2
    margin_top = 1.3 if mechanism else 0.6
    fig_w = max(8.0, n_cols * col_w + 1.5)
    fig_h = max(4.5, max_rows * row_h + margin_top + 0.5)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")
    # 强制中文字体（覆盖 science 样式）
    ax.set_title("") if False else None
    for _txt in ax.texts:
        _txt.set_fontfamily(["Microsoft YaHei", "SimHei", "DejaVu Sans"])

    if mechanism:
        ax.text(fig_w / 2, fig_h - 0.45, mechanism, ha="center", va="center",
                fontsize=11, fontweight="bold", color="#222",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#F7F9FC", edgecolor="#999", lw=0.6),
                family=["Microsoft YaHei", "SimHei", "DejaVu Sans"])

    # 节点坐标：每列等距、垂直居中
    pos = {}
    node_boxes = {}
    for lv, items in sorted(levels.items()):
        n_items = len(items)
        # 该列 x 中心
        col_x = 1.0 + lv * col_w
        # 垂直均匀分布，留上下边距
        for i, e in enumerate(items):
            y = fig_h - margin_top - (i + 0.5) * (fig_h - margin_top - 0.5) / max(n_items, 1)
            pos[e["name"]] = (col_x, y)
            node_boxes[e["name"]] = (e, col_x, y)

    bw, bh = 1.9, 0.65
    # 节点左右/上下中点（用于箭头锚点）
    def anchor(name, other_pos, this_pos):
        dx, dy = other_pos[0] - this_pos[0], other_pos[1] - this_pos[1]
        if abs(dx) > abs(dy):
            return (this_pos[0] + (bw / 2 if dx > 0 else -bw / 2), this_pos[1])
        return (this_pos[0], this_pos[1] + (bh / 2 if dy > 0 else -bh / 2))

    for name, (e, x, y) in node_boxes.items():
        t = e.get("type", "target")
        color = TYPE_COLOR.get(t, "#555")
        light = TYPE_LIGHT.get(t, "#EEE")
        box = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                             boxstyle="round,pad=0.04,rounding_size=0.12",
                             linewidth=1.1, edgecolor=color, facecolor=light, zorder=2)
        ax.add_patch(box)
        label = e["name"]
        ev = e.get("evidence")
        if ev and ev in EV_SUFFIX:
            label += EV_SUFFIX[ev]
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5,
                color="#111", fontweight="bold", zorder=3,
                family=["Microsoft YaHei", "SimHei", "DejaVu Sans"])

    # 关系箭头（弧形避开节点）
    for r in relations:
        f, t = r.get("from"), r.get("to")
        if f not in pos or t not in pos:
            continue
        p1, p2 = pos[f], pos[t]
        rtype = r.get("type", "activates")
        color = "#2CA02C" if rtype == "activates" else "#C0392B" if rtype == "inhibits" else "#555"
        a1 = anchor(f, p2, p1)
        a2 = anchor(t, p1, p2)
        if rtype == "inhibits":
            arr = FancyArrowPatch(a1, a2, arrowstyle="-",
                                  connectionstyle="arc3,rad=0.18",
                                  color=color, lw=1.4, zorder=1)
            ax.add_patch(arr)
            # T 形抑制端
            dx, dy = a2[0] - a1[0], a2[1] - a1[1]
            L = np.hypot(dx, dy)
            if L > 0:
                ux, uy = dx / L, dy / L
                px, py = -uy, ux
                tx, ty = a2[0] - ux * 0.05, a2[1] - uy * 0.05
                s = 0.12
                ax.plot([tx + px * s, tx - px * s], [ty + py * s, ty - py * s],
                        color=color, lw=1.8, zorder=2)
        else:
            arr = FancyArrowPatch(a1, a2, arrowstyle="->,head_width=6,head_length=9",
                                  connectionstyle="arc3,rad=0.18",
                                  color=color, lw=1.4, zorder=1, mutation_scale=14)
            ax.add_patch(arr)
        if r.get("label"):
            mx, my = (a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2
            ax.text(mx, my + 0.1, r["label"], ha="center",
                    fontsize=6.8, color="#555", style="italic", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
                    family=["Microsoft YaHei", "SimHei", "DejaVu Sans"])

    # 图例
    handles = [mpatches.Patch(facecolor=TYPE_LIGHT.get(t, "#EEE"), edgecolor=TYPE_COLOR.get(t, "#555"),
                              label=f"{t}") for t in TYPE_COLOR if t in {e.get('type') for e in entities}]
    ev_handles = [mpatches.Patch(facecolor="none", edgecolor="none",
                                 label=f"{s}:{w}") for w, s in [("实验","*"),("数据库","†"),("预测","‡"),("文献","§")] if any(e.get("evidence") == w for e in entities)]
    if handles or ev_handles:
        ax.legend(handles=handles + ev_handles, loc="lower right", frameon=False,
                  fontsize=7, ncol=2)

    base = str(Path(output_path).with_suffix(""))
    _save_multi(base, fig)
    plt.close(fig)
    print(f"[mechanism-diagram] {len(entities)} nodes, {len(relations)} edges -> {base}.svg/pdf/png/tiff")
    return base + ".svg"


def _save_multi(base: str, fig):
    """按投稿标准输出多格式：SVG / PDF / PNG 300dpi / TIFF 600dpi"""
    try:
        fig.savefig(base + ".svg", dpi=300, bbox_inches="tight")
        fig.savefig(base + ".pdf", dpi=300, bbox_inches="tight")
        fig.savefig(base + ".png", dpi=300, bbox_inches="tight")
        fig.savefig(base + ".tiff", dpi=600, bbox_inches="tight")
    except Exception as e:
        print(f"[save-multi] partial: {e}")


def _auto_select_plot(df: pd.DataFrame) -> str:
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n_num, n_cat = len(num_cols), len(cat_cols)
    cl = {c.lower(): c for c in df.columns}

    # 1) 差异分析表（log2FC + P 值）→ volcano
    has_fc = any(any(k in key for k in ("log2fc", "logfc", "foldchange", "lfc", "fc")) for key in cl)
    has_p = any(any(k in key for k in ("pvalue", "padj", "p_value", "qvalue", "fdr", "_p", "_q")) for key in cl)
    if has_fc and has_p and n_num >= 2:
        return "volcano"

    # 2) 生存数据（time + event/status）→ KM 曲线
    has_time = any(k in cl for k in ("time", "survival", "os", "days", "months"))
    has_event = any(k in cl for k in ("event", "status", "censor", "cns"))
    if has_time and has_event:
        return "km"

    # 3) 时间序列（time 列 + 数值列）→ line
    if has_time and n_num >= 1:
        return "line"

    # 4) 分类列 + 数值列 → 分组分布（violin 信息密度高于 box/bar）
    if n_cat >= 1 and n_num >= 1:
        # 计数/占比表（category + count/abundance/freq）→ bar/donut
        count_like = [c for c in num_cols if any(k in c.lower() for k in ("count", "freq", "abund", "percent", "proportion", "num", "n_"))]
        if count_like and len(count_like) == n_num:
            if n_cat >= 2:
                return "grouped_bar"
            return "bar"
        if n_num == 1:
            return "violin"
        return "box"  # 多数值 + 分类 → 分组箱线

    # 5) 纯数值多列 → heatmap / 相关
    if n_num >= 8:
        return "heatmap"
    if n_num >= 3:
        return "scatter_matrix" if hasattr(df, "corr") else "heatmap"
    if n_num == 2:
        return "scatter"
    if n_num == 1:
        return "histogram"

    # 6) 纯分类 → 计数占比
    if n_cat >= 2:
        return "grouped_bar"
    return "bar"


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
        # 通用数据：智能选型
        if plot_type == "auto":
            plot_type = _auto_select_plot(data)
            print(f"[auto-select] DataFrame -> {plot_type}")
        return generate_figure("general", plot_type, data, output_path, **kwargs)
    elif isinstance(data, dict) and ("entities" in data or "relations" in data or "nodes" in data):
        # 机制图结构化输入（entities+relations JSON）
        return plot_mechanism_diagram(data, output_path, **kwargs)
    elif isinstance(data, dict) and "edges" in data:
        # 图/网络结构化输入
        if plot_type == "auto":
            plot_type = "network"
        return generate_figure("network", plot_type, data, output_path, **kwargs)
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
