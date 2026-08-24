# -*- coding: utf-8 -*-
"""验证: 语法 + 智能选型 + 机制图"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\git\sci-figure-master\assets")
import numpy as np
import pandas as pd
import bioinfo_router as br
import chart_catalog as cc

OUT = r"E:\git\sci-figure-master\test_output\router_fix"
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)
n = 30

# 1) 差异分析表 → volcano
de = pd.DataFrame({
    "gene": [f"g{i}" for i in range(n)],
    "log2FC": rng.normal(0, 1, n),
    "pvalue": rng.uniform(0, 0.5, n),
    "padj": rng.uniform(0, 0.5, n),
})
t1 = br._auto_select_plot(de)
print("[1] DE table ->", t1)

# 2) 分类+数值 → violin
grp = pd.DataFrame({
    "group": np.repeat(["C", "M", "X"], 10),
    "value": rng.normal(0, 1, n),
})
t2 = br._auto_select_plot(grp)
print("[2] group+value ->", t2)

# 3) 生存 → km
km = pd.DataFrame({
    "sample": [f"s{i}" for i in range(n)],
    "time": rng.uniform(1, 30, n),
    "status": rng.integers(0, 2, n),
    "group": np.repeat(["C", "M"], n // 2),
})
t3 = br._auto_select_plot(km)
print("[3] survival ->", t3)

# 4) 时间序列 → line
ts = pd.DataFrame({
    "time": np.arange(n),
    "y1": np.cumsum(rng.normal(0, 0.1, n)),
    "y2": np.cumsum(rng.normal(0, 0.1, n)),
})
t4 = br._auto_select_plot(ts)
print("[4] timeseries ->", t4)

# 5) 多数值 → heatmap
hm = pd.DataFrame(rng.normal(0, 1, (10, 12)), columns=[f"m{i}" for i in range(12)])
t5 = br._auto_select_plot(hm)
print("[5] wide numeric ->", t5)

# 6) 分类占比 → bar
cb = pd.DataFrame({"category": ["A", "B", "C", "D"], "count": [10, 20, 15, 5]})
t6 = br._auto_select_plot(cb)
print("[6] category count ->", t6)

# 7) 机制图（XNP 纯组学主轴测试）
mech = {
    "mechanism": "XNP 菌群重塑-嘌呤/吲哚-小胶质/OPC 轴（纯组学版）",
    "entities": [
        {"name": "XNP", "type": "treatment", "evidence": "experiment", "level": 0},
        {"name": "Turicimonas↑/Bacillus↑", "type": "bacteria", "evidence": "experiment", "level": 1},
        {"name": "Bifidobacterium↓(未恢复)", "type": "bacteria", "evidence": "experiment", "level": 1},
        {"name": "血清嘌呤池↑", "type": "metabolite", "evidence": "experiment", "level": 2},
        {"name": "IPA/5-MIAA恢复", "type": "metabolite", "evidence": "experiment", "level": 2},
        {"name": "小胶质 TGFβ-嘌呤能", "type": "cell", "evidence": "experiment", "level": 3},
        {"name": "OPC 嘌呤能耦合", "type": "cell", "evidence": "experiment", "level": 3},
        {"name": "睡眠时长恢复", "type": "phenotype", "evidence": "experiment", "level": 4},
    ],
    "relations": [
        {"from": "XNP", "to": "Turicimonas↑/Bacillus↑", "type": "activates"},
        {"from": "XNP", "to": "Bifidobacterium↓(未恢复)", "type": "inhibits"},
        {"from": "Turicimonas↑/Bacillus↑", "to": "血清嘌呤池↑", "type": "produces", "label": "嘌呤配体 E1"},
        {"from": "Turicimonas↑/Bacillus↑", "to": "IPA/5-MIAA恢复", "type": "produces", "label": "G1 恢复"},
        {"from": "血清嘌呤池↑", "to": "小胶质 TGFβ-嘌呤能", "type": "activates", "label": "受体程序"},
        {"from": "血清嘌呤池↑", "to": "OPC 嘌呤能耦合", "type": "activates", "label": "FDR 0.0201"},
        {"from": "小胶质 TGFβ-嘌呤能", "to": "OPC 嘌呤能耦合", "type": "activates"},
        {"from": "OPC 嘌呤能耦合", "to": "睡眠时长恢复", "type": "activates", "label": "padj=0.0191"},
    ],
}
mech_out = br.plot_mechanism_diagram(mech, os.path.join(OUT, "mech_test.svg"))
print("[7] mechanism ->", mech_out, os.path.exists(mech_out))

# 8) 机制图 via quick_plot 自动路由（dict 输入）
q_out = br.quick_plot(mech, os.path.join(OUT, "mech_quick.svg"))
print("[8] quick_plot dict ->", q_out)

# 9) chart_catalog 机制图注册
print("[9] presentation count:", cc.count_charts()["by_category"].get("Presentation"))
for cid in ["mechanism_diagram", "graphical_abstract", "pathway_diagram", "flowchart"]:
    m = cc.get_chart(cid)
    print("   ", cid, "->", m["name_zh"] if m else "MISSING")

print("\nALL DONE")
