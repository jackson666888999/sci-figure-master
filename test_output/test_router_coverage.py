# -*- coding: utf-8 -*-
"""全领域×结构自动选型覆盖测试 + chart_catalog 映射覆盖率"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\git\sci-figure-master\assets")
import numpy as np
import pandas as pd
import bioinfo_router as br
import chart_catalog as cc

rng = np.random.default_rng(7)
n = 40

# 构造各结构样例
def sample(struct):
    if struct == "diff":
        return pd.DataFrame({"gene": [f"g{i}" for i in range(n)], "log2FC": rng.normal(0,1,n),
                             "pvalue": rng.uniform(0,1,n), "padj": rng.uniform(0,1,n)})
    if struct == "surv":
        return pd.DataFrame({"sample": [f"s{i}" for i in range(n)], "time": rng.uniform(1,30,n),
                             "status": rng.integers(0,2,n), "group": np.repeat(["A","B"], n//2)})
    if struct == "ts":
        return pd.DataFrame({"time": np.arange(n), "y1": np.cumsum(rng.normal(0,0.1,n)),
                             "y2": np.cumsum(rng.normal(0,0.1,n))})
    if struct == "grouped":
        g = np.repeat(["C","M","X"], [14, 13, 13]) if n == 40 else np.repeat(["C","M","X"], n // 3 + 1)[:n]
        return pd.DataFrame({"group": g[:n], "value": rng.normal(0,1,n)})
    if struct == "wide":
        return pd.DataFrame(rng.normal(0,1,(12,15)), columns=[f"m{i}" for i in range(15)])
    if struct == "two_num":
        return pd.DataFrame({"x": rng.normal(0,1,n), "y": rng.normal(0,1,n)})
    if struct == "single":
        return pd.DataFrame({"value": rng.normal(0,1,n)})
    if struct == "count":
        return pd.DataFrame({"category": ["A","B","C","D"], "count": [10,20,15,5]})
    return pd.DataFrame({"a": [1,2,3]})

structs = ["diff","surv","ts","grouped","wide","two_num","single","count"]
domains = ["general","microbiome","metabolomics","proteomics","bulkrna","survival",
           "genome","multiomics","scrna","phylogeny","epigenetic","spatial","flow","enrichment"]

print("=== 结构 → 自动选型（无领域） ===")
for s in structs:
    cands = br._auto_select_plot(sample(s), top_n=3)
    print(f"  {s:9s} -> {cands}")

print("\n=== 领域 × 结构 → 自动选型 ===")
for d in domains:
    row = []
    for s in ["diff","grouped","wide","count"]:
        cands = br._auto_select_plot(sample(s), domain=d, top_n=2)
        row.append(f"{s}:{cands[0] if cands else '-'}")
    print(f"  {d:12s} | " + " | ".join(row))

print("\n=== chart_catalog 图型 → PLOT_INPUT_MAP 覆盖率 ===")
total = len(cc.CHART_CATALOG)
mapped = sum(1 for cid in cc.CHART_CATALOG if cid in br.PLOT_INPUT_MAP)
print(f"  total charts: {total}, mapped: {mapped} ({mapped/total*100:.0f}%)")
unmapped = [cid for cid in cc.CHART_CATALOG if cid not in br.PLOT_INPUT_MAP]
print(f"  unmapped ({len(unmapped)}): {unmapped[:20]}...")

print("\n=== 无 native 函数的图型（走 fallback 链） ===")
no_native = [cid for cid in cc.CHART_CATALOG
             if not br.get_native_plot_function("general", cid)
             and not br.get_native_plot_function("scRNA", cid)]
print(f"  {len(no_native)} 个需 fallback: {no_native[:15]}...")

# quick_plot 端到端
print("\n=== quick_plot 端到端 ===")
OUT = r"E:\git\sci-figure-master\test_output\router_fix"
os.makedirs(OUT, exist_ok=True)
p = br.quick_plot(sample("diff"), os.path.join(OUT, "e2e_diff.svg"))
print("  diff ->", os.path.basename(p))
p = br.quick_plot(sample("grouped"), os.path.join(OUT, "e2e_grp.svg"))
print("  grouped ->", os.path.basename(p))
p = br.quick_plot(sample("wide"), os.path.join(OUT, "e2e_wide.svg"))
print("  wide ->", os.path.basename(p))
p = br.quick_plot(sample("surv"), os.path.join(OUT, "e2e_surv.svg"))
print("  surv ->", os.path.basename(p))

print("\nALL DONE")
