# -*- coding: utf-8 -*-
"""Dump all XNP multi-omics diff molecules per comparison (read-only)."""
import pandas as pd
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

OUT = r"E:\git\sci-figure-master\test_output\xnp_all_diff_dump.txt"
BASE = r"D:\乌灵菌"
lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

def dump_xlsx(p, head=40, maxcols=30):
    try:
        if p.endswith(".xlsx"):
            df = pd.read_excel(p)
        else:
            df = pd.read_csv(p, sep="\t" if p.endswith(".tsv") else ",")
        log(f"  shape={df.shape}")
        log(f"  cols={list(df.columns)[:maxcols]}")
        with pd.option_context("display.max_columns", None, "display.width", 300):
            log(df.head(head).to_string())
        return df
    except Exception as e:
        log(f"  [ERR] {e}")
        return None

# ============ 脑代谢组 XNP comparisons ============
log("#" * 100)
log("# A. 脑代谢组 (Brain Metabolome) - XNP 相关比较")
log("#" * 100)
brain_d = os.path.join(BASE, r"data\LC-P20260131046-脑非靶代谢组学\脑代谢Summary_Extracted\脑代谢Summary\05.DiffExp\COND1")
for root, dirs, files in os.walk(brain_d):
    for f in files:
        if "diff_featurespeaks" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f):
            p = os.path.join(root, f)
            log(f"\n--- {os.path.relpath(p, BASE)} ---")
            dump_xlsx(p, head=50)

# ============ 粪便代谢组 XNP comparisons ============
log("\n" + "#" * 100)
log("# B. 粪便代谢组 (Fecal Metabolome) - XNP 相关比较")
log("#" * 100)
fecal_d = os.path.join(BASE, r"data\LC-P20260131045-粪便非靶代谢组学\粪便代谢Summary_Extracted\粪便代谢Summary\05.DiffExp\COND1")
for root, dirs, files in os.walk(fecal_d):
    for f in files:
        if "diff_featurespeaks" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f):
            p = os.path.join(root, f)
            log(f"\n--- {os.path.relpath(p, BASE)} ---")
            dump_xlsx(p, head=50)

# ============ 血清代谢组 XNP comparisons ============
log("\n" + "#" * 100)
log("# C. 血清代谢组 (Serum Metabolome) - XNP 相关比较")
log("#" * 100)
serum_d = os.path.join(BASE, r"data\LC-P20260131050-血清非靶代谢组学\血清代谢Summary_Extracted")
if not os.path.exists(serum_d):
    serum_d = os.path.join(BASE, r"data\LC-P20260131050-血清非靶代谢组学")
for root, dirs, files in os.walk(serum_d):
    for f in files:
        if "diff_featurespeaks" in f and f.endswith(".xlsx") and ("XNPVS" in f or "VSXNP" in f or "ModelVSControl" in f):
            p = os.path.join(root, f)
            log(f"\n--- {os.path.relpath(p, BASE)} ---")
            dump_xlsx(p, head=50)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print(f"WROTE {OUT} lines={len(lines)}")
