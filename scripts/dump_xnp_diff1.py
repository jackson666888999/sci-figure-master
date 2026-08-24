# -*- coding: utf-8 -*-
"""Extract all XNP multi-omics diff results to a single readable text file (read-only)."""
import pandas as pd
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

OUT = r"E:\git\sci-figure-master\test_output\xnp_results_dump.txt"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

BASE = r"D:\乌灵菌"
lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

# ============ 1. Brain metabolome diff ============
log("=" * 90)
log("### 1. 脑代谢组差异特征 (COND1_diff_featurespeak)")
log("=" * 90)
for sub in [r"data\LC-P20260131046-脑非靶代谢组学\脑代谢Summary_Extracted\脑代谢Summary\05.DiffExp\COND1"]:
    d = os.path.join(BASE, sub)
    for f in os.listdir(d):
        if "diff_featurespeak" in f and f.endswith(".xlsx"):
            p = os.path.join(d, f)
            try:
                df = pd.read_excel(p)
                log(f"\n--- {f} ---")
                log(f"shape={df.shape} cols={list(df.columns)[:20]}")
                with pd.option_context("display.max_columns", None, "display.width", 250):
                    log(df.head(30).to_string())
            except Exception as e:
                log(f"  [ERR] {e}")

# ============ 2. Brain metabolome enrichment ============
log("\n" + "=" * 90)
log("### 2. 脑代谢组 KEGG 富集")
log("=" * 90)
d = os.path.join(BASE, r"data\LC-P20260131046-脑非靶代谢组学\脑代谢Summary_Extracted\脑代谢Summary\05.DiffExp")
for root, dirs, files in os.walk(d):
    for f in files:
        if "KEGG" in root and (f.endswith(".xlsx") or f.endswith(".csv")) and "diff" not in f.lower() and "pathview" not in f.lower():
            p = os.path.join(root, f)
            try:
                df = pd.read_excel(p) if f.endswith(".xlsx") else pd.read_csv(p)
                log(f"\n--- {os.path.relpath(p, BASE)} --- shape={df.shape}")
                with pd.option_context("display.max_columns", None, "display.width", 250):
                    log(df.head(15).to_string())
            except Exception as e:
                log(f"  [ERR] {e}")

# ============ 3. Fecal metabolome diff ============
log("\n" + "=" * 90)
log("### 3. 粪便代谢组差异特征")
log("=" * 90)
d = os.path.join(BASE, r"data\LC-P20260131045-粪便非靶代谢组学\粪便代谢Summary_Extracted\粪便代谢Summary\05.DiffExp\COND1")
if os.path.exists(d):
    for f in os.listdir(d):
        if "diff_featurespeak" in f and f.endswith(".xlsx"):
            p = os.path.join(d, f)
            try:
                df = pd.read_excel(p)
                log(f"\n--- {f} ---")
                log(f"shape={df.shape} cols={list(df.columns)[:20]}")
                with pd.option_context("display.max_columns", None, "display.width", 250):
                    log(df.head(30).to_string())
            except Exception as e:
                log(f"  [ERR] {e}")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
print(f"WROTE {OUT} with {len(lines)} lines")
