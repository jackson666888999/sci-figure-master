# -*- coding: utf-8 -*-
"""Summarize significant diff molecules per comparison (concise, top-N by p/VIP)."""
import pandas as pd
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

OUT = r"E:\git\sci-figure-master\test_output\xnp_top_diff_summary.txt"
BASE = r"D:\乌灵菌"
lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def load(p):
    return pd.read_excel(p) if p.endswith(".xlsx") else pd.read_csv(p, sep="\t" if p.endswith(".tsv") else ",")

def summarize(name, path, p_cut=0.05, vip_cut=1.0, top=25):
    log("\n" + "=" * 90)
    log(f"### {name}")
    log(f"### {os.path.relpath(path, BASE)}")
    try:
        df = load(path)
        log(f"  total features={len(df)}")
        cols = [c for c in df.columns]
        # find key columns
        pcol = next((c for c in cols if c.lower() in ("p_value","pvalue","p","p.val")), None)
        qcol = next((c for c in cols if "q_value" in c.lower() or "fdr" in c.lower()), None)
        vipcol = next((c for c in cols if "vip" in c.lower()), None)
        metcol = next((c for c in cols if c.lower() in ("metabolites","name","protein","gene","feature","compound","Metabolites")), None)
        # filter significant
        sub = df.copy()
        if pcol:
            sub[pcol] = pd.to_numeric(sub[pcol], errors="coerce")
            sub = sub[sub[pcol] < p_cut]
        if vipcol:
            sub[vipcol] = pd.to_numeric(sub[vipcol], errors="coerce")
            sub = sub[sub[vipcol] >= vip_cut]
        log(f"  significant (p<{p_cut}" + (f", VIP>={vip_cut}" if vipcol else "") + f") = {len(sub)}")
        # sort by p
        if pcol:
            sub = sub.sort_values(pcol)
        show_cols = [c for c in [metcol, pcol, qcol, vipcol] if c]
        if not show_cols:
            show_cols = cols[:6]
        with pd.option_context("display.max_columns", None, "display.width", 300):
            log(sub[show_cols].head(top).to_string())
        # class distribution if exists
        classcol = next((c for c in cols if c.lower() in ("class","superclass","subclass")), None)
        if classcol is not None and len(sub):
            log("  class distribution:")
            log(sub[classcol].value_counts().head(10).to_string())
    except Exception as e:
        log(f"  [ERR] {e}")

# ===== Brain metabolome =====
bd = os.path.join(BASE, r"data\LC-P20260131046-脑非靶代谢组学\脑代谢Summary_Extracted\脑代谢Summary\05.DiffExp\COND1")
for cmp in ["High_dose_XNPVSModel", "High_dose_XNPVSControl", "ModelVSControl"]:
    p = os.path.join(bd, cmp, f"{cmp}_diff_featurespeaks.xlsx")
    if os.path.exists(p):
        summarize(f"脑代谢组 {cmp}", p)

# ===== Fecal metabolome =====
fd = os.path.join(BASE, r"data\LC-P20260131045-粪便非靶代谢组学\粪便代谢Summary_Extracted\粪便代谢Summary\05.DiffExp\COND1")
for cmp in ["High_dose_XNPVSModel", "High_dose_XNPVSControl", "ModelVSControl"]:
    p = os.path.join(fd, cmp, f"{cmp}_diff_featurespeaks.xlsx")
    if os.path.exists(p):
        summarize(f"粪便代谢组 {cmp}", p)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print(f"WROTE {OUT} lines={len(lines)}")
