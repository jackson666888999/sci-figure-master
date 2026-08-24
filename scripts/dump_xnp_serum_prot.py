# -*- coding: utf-8 -*-
"""Extract serum metabolome + serum/brain proteome diff results (concise)."""
import pandas as pd
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

OUT = r"E:\git\sci-figure-master\test_output\xnp_serum_prot_dump.txt"
BASE = r"D:\乌灵菌"
lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def load(p):
    return pd.read_excel(p) if p.endswith(".xlsx") else pd.read_csv(p, sep="\t" if p.endswith(".tsv") else ",")

def summarize(name, path, p_cut=0.05, top=25, extra_cols=None):
    log("\n" + "=" * 90)
    log(f"### {name}")
    log(f"### {os.path.relpath(path, BASE)}")
    try:
        df = load(path)
        log(f"  total features={len(df)}")
        cols = list(df.columns)
        pcol = next((c for c in cols if c.lower() in ("p_value","pvalue","p","p.val","p.value")), None)
        qcol = next((c for c in cols if "q_value" in c.lower() or "fdr" in c.lower() or "qvalue" in c.lower()), None)
        namecol = next((c for c in cols if c.lower() in ("metabolites","name","protein","gene","feature","compound","metabolites","description","proteinname","protein name")), None)
        sub = df.copy()
        if pcol:
            sub[pcol] = pd.to_numeric(sub[pcol], errors="coerce")
            sub = sub[sub[pcol] < p_cut]
        log(f"  significant p<{p_cut} = {len(sub)}")
        if pcol:
            sub = sub.sort_values(pcol)
        show = [c for c in [namecol, pcol, qcol] if c]
        if extra_cols:
            show += [c for c in extra_cols if c in cols]
        if not show:
            show = cols[:6]
        with pd.option_context("display.max_columns", None, "display.width", 300):
            log(sub[show].head(top).to_string())
    except Exception as e:
        log(f"  [ERR] {e}")

# ===== Serum metabolome: find extracted dir =====
sm_root = os.path.join(BASE, r"data\LC-P20260131050-血清非靶代谢组学")
# find any extracted folder
cands = [os.path.join(sm_root, d) for d in os.listdir(sm_root) if "Extracted" in d or "Summary" in d]
log("Serum metabolome candidates: " + "; ".join(cands))
for root in cands:
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if "diff_featurespeaks" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f):
                summarize(f"血清代谢组 {f.replace('_diff_featurespeaks.xlsx','')}", os.path.join(dirpath, f), top=20)

# ===== Serum proteome: XNP comparisons =====
log("\n" + "#" * 100)
log("# 血清蛋白组 XNP 比较")
log("#" * 100)
sp_root = os.path.join(BASE, r"data\LC-P20260131050-血清质谱蛋白组学(Fast-Astral-DIA)")
# the extracted root
cands = [os.path.join(sp_root, d) for d in os.listdir(sp_root) if "Extracted" in d]
for root in cands:
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if "diff_annotation" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f or "COND1_diff_stat" in f):
                summarize(f"血清蛋白组 {f}", os.path.join(dirpath, f), top=20,
                          extra_cols=["log2FC","FC","log2FoldChange","fold_change","Significant","regulated","Regulated","expression","Expression"])

# ===== Brain proteome: XNP comparisons =====
log("\n" + "#" * 100)
log("# 脑蛋白组 XNP 比较")
log("#" * 100)
bp_root = os.path.join(BASE, r"data\LC-P20260131046-脑质谱蛋白组学(Fast-Astral-DIA)")
cands = [os.path.join(bp_root, d) for d in os.listdir(bp_root) if "Extracted" in d]
if not cands:
    cands = [bp_root]
for root in cands:
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if "diff_annotation" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f or "COND1_diff_stat" in f):
                summarize(f"脑蛋白组 {f}", os.path.join(dirpath, f), top=20,
                          extra_cols=["log2FC","FC","log2FoldChange","fold_change","Significant","regulated","Regulated"])

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print(f"WROTE {OUT} lines={len(lines)}")
