#!/usr/bin/env python3
"""
test_chart_expansion.py - 100+ 图表类型扩展测试
覆盖: SciVizKit 风格新图表 + 修复后的 UMAP/heatmap/sankey 路由
"""
import os
import sys
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "assets"))

import numpy as np
import pandas as pd

from chart_catalog import CHART_CATALOG, count_charts, list_charts, suggest_for_domain
from bioinfo_router import generate_figure, quick_plot

OUT = Path(__file__).parent / "test_output" / "chart_expansion"
OUT.mkdir(parents=True, exist_ok=True)

passed = []
failed = []


def check(name, ok, detail=""):
    if ok:
        passed.append(name)
        print(f"[OK]   {name}")
    else:
        failed.append(name)
        print(f"[FAIL] {name} {detail}")


# ── 1. 图表目录验证 ─────────────────────────────
print("=" * 60)
print("[1] Chart Catalog (100+ target)")
print("=" * 60)
stats = count_charts()
check("total >= 100", stats["total"] >= 100, f"got {stats['total']}")
check("scRNA domain suggestions", len(suggest_for_domain("scRNA")) >= 5)
check("microbiome domain suggestions", len(suggest_for_domain("microbiome")) >= 5)
check("volcano in catalog", "volcano" in CHART_CATALOG)
check("ridgeline in catalog", "ridgeline" in CHART_CATALOG)

# ── 2. 模拟数据 ─────────────────────────────
np.random.seed(42)
n = 120
df_general = pd.DataFrame({
    'group': np.random.choice(['Ctrl', 'Treat', 'Model'], n),
    'value': np.random.randn(n) * 5 + 20,
    'value2': np.random.randn(n) * 3 + 10,
    'time': np.arange(n),
    'score': np.random.randn(n) * 2,
    'pos': np.random.randn(n) * 0.5 + 0.5,
})

# 火山图数据
df_volcano = pd.DataFrame({
    'gene': [f'G{i}' for i in range(200)],
    'log2FC': np.random.randn(200) * 1.2,
    'pvalue': 10 ** -np.random.uniform(0, 6, 200),
})

# 森林图数据
df_forest = pd.DataFrame({
    'effect': np.random.randn(15) * 0.5,
    'se': np.abs(np.random.randn(15)) * 0.15,
}, index=[f'Study{i}' for i in range(15)])

# 曼哈顿图数据
df_gwas = pd.DataFrame({
    'chrom': np.repeat([f'chr{i}' for i in range(1, 6)], 60),
    'pos': np.tile(np.arange(60), 5),
    'pval': 10 ** -np.random.uniform(0, 8, 300),
})

# ── 3. 新增 SciVizKit 风格图表测试 ─────────────────────────────
print("=" * 60)
print("[2] New SciVizKit-style charts (pure matplotlib)")
print("=" * 60)

chart_tests = [
    ("ridgeline", "general", {"x": "group", "y": "value"}),
    ("raincloud", "general", {"x": "group", "y": "value"}),
    ("radar", "general", {}),
    ("lollipop", "general", {"x": "group", "y": "value"}),
    ("dumbbell", "general", {}),
    ("bubble", "general", {"x": "value", "y": "value2", "size": "score"}),
    ("hexbin", "general", {"x": "value", "y": "value2"}),
    ("parallel_coords", "general", {}),
    ("area", "general", {"x": "time", "y": "value"}),
    ("stacked_area", "general", {}),
    ("donut", "general", {}),
    ("treemap", "general", {}),
    ("waffle", "general", {}),
    ("nightingale", "general", {}),
    ("dendrogram", "general", {}),
    ("qqplot", "general", {"column": "value"}),
    ("ecdf", "general", {"group_col": "group"}),
    ("bland_altman", "general", {"x": "value", "y": "value2"}),
    ("diverging_bar", "general", {}),
    ("radial_bar", "general", {}),
    ("marginal_plot", "general", {"x": "value", "y": "value2"}),
    ("ma_plot", "general", {}),
]

for plot_type, domain, kwargs in chart_tests:
    try:
        out = OUT / f"test_{plot_type}.svg"
        generate_figure(domain, plot_type, df_general, str(out), **kwargs)
        check(f"{plot_type}", out.exists() and out.stat().st_size > 500)
    except Exception as e:
        check(f"{plot_type}", False, str(e)[:100])

# 专用数据图表
try:
    out = OUT / "test_manhattan.svg"
    generate_figure("genome", "manhattan", df_gwas, str(out),
                    chrom_col="chrom", pos_col="pos", pval_col="pval")
    check("manhattan", out.exists() and out.stat().st_size > 500)
except Exception as e:
    check("manhattan", False, str(e)[:100])

try:
    out = OUT / "test_forest_plot.svg"
    generate_figure("survival", "forest", df_forest, str(out))
    check("forest_plot", out.exists() and out.stat().st_size > 500)
except Exception as e:
    check("forest_plot", False, str(e)[:100])

try:
    out = OUT / "test_funnel_plot.svg"
    generate_figure("general", "funnel_plot", df_forest, str(out))
    check("funnel_plot", out.exists() and out.stat().st_size > 500)
except Exception as e:
    check("funnel_plot", False, str(e)[:100])

try:
    out = OUT / "test_volcano_sig.svg"
    generate_figure("general", "volcano", df_volcano, str(out),
                    log2fc_col="log2FC", pval_col="pvalue")
    check("volcano", out.exists() and out.stat().st_size > 500)
except Exception as e:
    check("volcano", False, str(e)[:100])

# ── 4. 单细胞修复验证 ─────────────────────────────
print("=" * 60)
print("[3] scRNA routing fix (UMAP/heatmap)")
print("=" * 60)
try:
    import scanpy as sc
    adata = sc.datasets.pbmc68k_reduced()
    try:
        out = OUT / "test_umap_fix.svg"
        generate_figure("scRNA", "UMAP", adata, str(out), color="louvain")
        check("scRNA UMAP routing", out.exists() and out.stat().st_size > 500)
    except Exception as e:
        check("scRNA UMAP routing", False, str(e)[:120])
    try:
        out = OUT / "test_heatmap_fix.svg"
        generate_figure("scRNA", "heatmap", adata, str(out))
        check("scRNA heatmap (auto groupby)", out.exists() and out.stat().st_size > 500)
    except Exception as e:
        check("scRNA heatmap (auto groupby)", False, str(e)[:120])
    try:
        out = OUT / "test_sankey_fix.svg"
        df_sankey = pd.DataFrame({
            'phylum': np.random.choice(['Bacteroidota', 'Firmicutes', 'Proteobacteria'], 200),
            'genus': np.random.choice(['G1', 'G2', 'G3', 'G4'], 200),
            'species': np.random.choice(['S1', 'S2', 'S3'], 200),
        })
        generate_figure("microbiome", "sankey", df_sankey, str(out))
        check("sankey real impl", out.exists() and out.stat().st_size > 500)
    except Exception as e:
        check("sankey real impl", False, str(e)[:120])
except ImportError as e:
    print(f"  ! scanpy not available: {e}")

# ── 5. 汇总 ─────────────────────────────
print("=" * 60)
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
print("=" * 60)
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL TESTS PASSED")
