#!/usr/bin/env python3
"""test_full_domain_routing.py - 全领域路由覆盖测试

遍历 chart_catalog 所有领域 × 推荐图表，验证:
1. 每个领域都有路由可用
2. generate_figure 对任意 (领域, 图型) 组合不抛异常
3. 新增领域函数（spatial/oncoplot/ppi/roc 等）能出图
"""
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "assets"))

import numpy as np
import pandas as pd

from chart_catalog import CHART_CATALOG, suggest_for_domain, count_charts
from bioinfo_router import generate_figure, get_native_plot_function

OUT = Path(__file__).parent / "test_output" / "full_routing"
OUT.mkdir(parents=True, exist_ok=True)

passed, failed = [], []


def check(name, ok, detail=""):
    if ok:
        passed.append(name)
    else:
        failed.append(name)
        print(f"[FAIL] {name} {detail}")


# ── 1. 路由表统计 ─────────────
print("=" * 60)
print("[1] Routing table coverage")
print("=" * 60)
from bioinfo_router import _all_routing
routing = _all_routing()
domains_covered = sorted({d for d, _ in routing.keys()})
print(f"  domains in routing table: {len(domains_covered)}")
print(f"  routing entries: {len(routing)}")
check("routing >= 250 entries", len(routing) >= 250, f"got {len(routing)}")
check("routing >= 20 domains", len(domains_covered) >= 20, f"got {len(domains_covered)}")
for dom in ["multiomics", "spatial", "flow", "methylation", "immunology", "cancer",
            "wgs", "protein", "clinical", "drug", "cellline", "rna"]:
    check(f"domain covered: {dom}", any(d == dom or dom in d for d in domains_covered),
          f"covered={domains_covered}")

# ── 2. 领域推荐 × 路由解析 ─────────────
print("=" * 60)
print("[2] Domain suggestions resolve to functions")
print("=" * 60)
DOMAINS = ["scRNA", "bulkRNA", "microbiome", "metabolomics", "proteomics",
           "genome", "phylogeny", "survival", "enrichment", "epigenetic",
           "multiomics", "spatial", "flow", "immunology", "cancer",
           "wgs", "protein", "rna", "clinical", "drug", "cellline", "general"]
resolve_fail = []
for dom in DOMAINS:
    recs = suggest_for_domain(dom, top_n=30)
    unresolved = []
    for fig in recs:
        if get_native_plot_function(dom, fig) is None:
            unresolved.append(fig)
    if unresolved:
        resolve_fail.append((dom, unresolved))
        print(f"  !! {dom}: unresolved -> {unresolved}")
    else:
        print(f"  [OK] {dom}: {len(recs)} recommendations all resolved")
check("all domains resolve", len(resolve_fail) == 0, f"fails={resolve_fail}")

# ── 3. 新增领域函数出图 ─────────────
print("=" * 60)
print("[3] New domain figure functions")
print("=" * 60)
rng = np.random.default_rng(42)

# spatial 数据（x/y 坐标 + 表达）
sp_df = pd.DataFrame({
    "x": rng.uniform(0, 10, 200),
    "y": rng.uniform(0, 10, 200),
    "gene_A": rng.normal(3, 1, 200),
    "gene_B": rng.normal(5, 1.5, 200),
})
# oncoplot 数据
onc_df = pd.DataFrame({f"Gene{i}": rng.binomial(1, 0.2, 40) * rng.poisson(2, 40) for i in range(1, 11)})
# ppi 边表
ppi_df = pd.DataFrame({
    "p1": [f"P{rng.integers(0, 30)}" for _ in range(60)],
    "p2": [f"P{rng.integers(0, 30)}" for _ in range(60)],
    "score": rng.uniform(0.3, 1.0, 60),
})
# roc 数据
roc_df = pd.DataFrame({
    "y_true": rng.binomial(1, 0.4, 100),
    "score1": rng.normal(0.5, 0.3, 100),
    "score2": rng.normal(0.6, 0.35, 100),
})
# 流式数据
flow_df = pd.DataFrame({
    "group": np.repeat(["Ctrl", "Treat"], 80),
    "FSC_A": np.concatenate([rng.normal(50, 10, 80), rng.normal(60, 12, 80)]),
    "SSC_A": rng.normal(40, 8, 160),
})
# 甲基化数据
meth_df = pd.DataFrame({f"cg{i}": rng.beta(2, 2, 100) for i in range(6)})
# 免疫组库
clono_df = pd.DataFrame({
    "clonotype": [f"CL{i}" for i in range(20)],
    "frequency": rng.poisson(30, 20),
})
# 变异
variant_df = pd.DataFrame({
    "type": rng.choice(["Missense", "Frameshift", "Nonsense", "Splice", "Synonymous"], 300),
})
# 剂量响应
dr_df = pd.DataFrame({
    "dose": np.logspace(-2, 2, 40),
    "drugA": 100 / (1 + np.exp(-(np.log10(np.logspace(-2, 2, 40)) + 0.5) * 1.5)),
    "drugB": 100 / (1 + np.exp(-(np.log10(np.logspace(-2, 2, 40)) - 0.2) * 1.5)),
})
# IC50
ic50_df = pd.DataFrame({"drug": ["A", "B", "C", "D", "E"], "ic50": [0.5, 1.2, 3.4, 0.8, 2.1]})
# 校准
cal_df = pd.DataFrame({"pred": rng.uniform(0, 1, 500), "obs": rng.binomial(1, 0.5, 500)})
# 剪接
sashimi_df = pd.DataFrame({f"exon{i}": rng.poisson(10, 50) for i in range(1, 5)})
# 韦恩
venn_df = pd.DataFrame({
    "setA": rng.choice(["x", "y", "z"], 100),
    "setB": rng.choice(["x", "y", "w"], 100),
})
# Motif
motif_df = pd.DataFrame({
    "motif": [f"MOTIF{i}" for i in range(15)],
    "pvalue": 10 ** -rng.uniform(1, 10, 15),
})

domain_tests = [
    ("spatial", "spot", sp_df, {}),
    ("flow", "histogram", flow_df, {}),
    ("methylation", "beta", meth_df, {}),
    ("immunology", "clonotype", clono_df, {}),
    ("cancer", "oncoplot", onc_df, {}),
    ("wgs", "variant", variant_df, {}),
    ("protein", "ppi", ppi_df, {}),
    ("clinical", "roc", roc_df, {}),
    ("clinical", "calibration", cal_df, {}),
    ("drug", "dose_response", dr_df, {}),
    ("drug", "ic50", ic50_df, {}),
    ("rna", "sashimi", sashimi_df, {}),
    ("general", "venn", venn_df, {}),
    ("enrichment", "motif", motif_df, {}),
]
for domain, fig, df, kw in domain_tests:
    try:
        out = OUT / f"{domain}_{fig}.svg"
        generate_figure(domain, fig, df, str(out), **kw)
        check(f"{domain}/{fig}", out.exists() and out.stat().st_size > 500)
    except Exception as e:
        check(f"{domain}/{fig}", False, str(e)[:120])

# ── 4. 跨领域通用图型兜底（任意领域 × 高频图型） ─────────────
print("=" * 60)
print("[4] Cross-domain fallback (any domain x common figure)")
print("=" * 60)
common_df = pd.DataFrame({
    "group": np.repeat(["A", "B", "C"], 40),
    "value": rng.normal(10, 2, 120),
    "value2": rng.normal(5, 1, 120),
})
random_domains = ["metabolomics", "flow", "immunology", "cancer", "drug", "rna", "protein", "wgs"]
common_figs = ["volcano", "heatmap", "box", "scatter", "donut", "treemap", "sankey",
               "dendrogram", "qqplot", "ecdf", "ridgeline", "raincloud", "lollipop",
               "radar", "ma_plot", "forest_plot", "manhattan", "pca", "bubble", "hexbin"]
cross_ok = 0
cross_fail = []
for dom in random_domains:
    for fig in common_figs:
        try:
            out = OUT / f"cross_{dom}_{fig}.svg"
            generate_figure(dom, fig, common_df, str(out))
            cross_ok += 1
        except Exception as e:
            cross_fail.append((dom, fig, str(e)[:60]))
check(f"cross-domain: {cross_ok} combinations OK", len(cross_fail) == 0,
      f"fails={cross_fail[:5]}")

# ── 5. 汇总 ─────────────
print("=" * 60)
stats = count_charts()
print(f"Chart catalog: {stats['total']} types | Routing: {len(routing)} entries | "
      f"{len(domains_covered)} domains")
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL TESTS PASSED")
