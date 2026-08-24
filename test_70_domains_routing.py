#!/usr/bin/env python3
"""test_70_domains_routing.py - 70 领域 + K-Dense 22 学科路由全覆盖测试"""
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "assets"))

import numpy as np
import pandas as pd

from domains_70_config import (DOMAINS_70_ROUTING, KDENSE_DISCIPLINE_ROUTING,
                               ALL_70_DOMAINS, DOMAIN_70_NAMES,
                               KDENSE_22_DISCIPLINES, KDENSE_DISCIPLINE_SKILLS)
from bioinfo_router import get_native_plot_function, generate_figure, _all_routing

OUT = Path(__file__).parent / "test_output" / "domains_70"
OUT.mkdir(parents=True, exist_ok=True)

passed, failed = [], []


def check(name, ok, detail=""):
    if ok:
        passed.append(name)
    else:
        failed.append(name)
        print(f"[FAIL] {name} {detail}")


# 通用测试数据（供各节抽样出图使用）
rng = np.random.default_rng(42)
common_df = pd.DataFrame({
    "group": np.repeat(["Ctrl", "Treat", "Model"], 40),
    "value": rng.normal(10, 2, 120),
    "value2": rng.normal(5, 1, 120),
    "gene1": rng.normal(3, 0.8, 120),
})


# ── 1. 配置完整性 ─────────────
print("=" * 60)
print("[1] Config completeness")
print("=" * 60)
check("70 domains defined", len(ALL_70_DOMAINS) == 70, f"got {len(ALL_70_DOMAINS)}")
check("K-Dense 22 disciplines", len(KDENSE_DISCIPLINE_ROUTING) == 22,
      f"got {len(KDENSE_DISCIPLINE_ROUTING)}")
check("70 domains all have figures", all(len(v) > 0 for v in DOMAINS_70_ROUTING.values()))

# K-Dense 官方 22 学科核对
OFFICIAL_DISCIPLINES = ["finance", "clinical", "chemistry", "genomics", "drugdiscovery",
                        "paper", "data", "ml", "physics", "ecology", "proteomics",
                        "cellbio", "visual", "grants", "materials", "neuro", "social",
                        "math", "engineering", "literature", "astro", "scicomm"]
missing_disc = [d for d in OFFICIAL_DISCIPLINES if d not in KDENSE_DISCIPLINE_ROUTING]
check("official 22 disciplines all present", len(missing_disc) == 0, f"missing={missing_disc}")
check("discipline-skill mapping present", len(KDENSE_DISCIPLINE_SKILLS) == 22)
# 每学科图型数充足（官方技能合并结果）
thin_disc = {d: len(v) for d, v in KDENSE_DISCIPLINE_ROUTING.items() if len(v) < 10}
check("every discipline >= 10 figures", len(thin_disc) == 0, f"thin={thin_disc}")
total_kd_figs = sum(len(v) for v in KDENSE_DISCIPLINE_ROUTING.values())
print(f"  K-Dense total figure entries: {total_kd_figs}")

routing = _all_routing()
domains_in_routing = {d for d, _ in routing.keys()}
check("routing entries >= 1000", len(routing) >= 1000, f"got {len(routing)}")
print(f"  routing entries: {len(routing)}")
print(f"  routing domains: {len(domains_in_routing)}")

# ── 2. 70 领域图型全部可解析 ─────────────
print("=" * 60)
print("[2] 70 domains: all figures resolve")
print("=" * 60)
unresolved = []
for domain, figs in DOMAINS_70_ROUTING.items():
    bad = [f for f in figs if get_native_plot_function(domain, f) is None]
    if bad:
        unresolved.append((domain, bad))
check("70 domains all resolve", len(unresolved) == 0,
      f"unresolved={unresolved[:5]}")

# ── 3. K-Dense 22 学科全部可解析 + 抽样出图 ─────────────
print("=" * 60)
print("[3] K-Dense 22 disciplines resolve + sample figures")
print("=" * 60)
kd_bad = []
for domain, figs in KDENSE_DISCIPLINE_ROUTING.items():
    bad = [f for f in figs if get_native_plot_function(domain, f) is None]
    if bad:
        kd_bad.append((domain, bad[:5]))
check("22 disciplines all resolve", len(kd_bad) == 0, f"unresolved={kd_bad[:5]}")

# 抽样：官方学科 × 技能专属图型出图
kd_sample_fail = []
n_kd = 0
kd_sample_tests = [
    ("genomics", "manhattan"), ("genomics", "volcano"), ("genomics", "tree"),
    ("cellbio", "umap"), ("cellbio", "dotplot"), ("cellbio", "trajectory"),
    ("proteomics", "volcano"), ("proteomics", "ppi"),
    ("chemistry", "radar"), ("drugdiscovery", "dose_response"),
    ("clinical", "km"), ("clinical", "roc"), ("clinical", "forest"),
    ("physics", "line"), ("materials", "scatter"), ("neuro", "line"),
    ("ecology", "alpha_diversity"), ("finance", "line"), ("ml", "roc"),
    ("visual", "bar"), ("data", "heatmap"), ("math", "scatter"),
    ("engineering", "line"), ("astro", "scatter"), ("social", "bar"),
    ("paper", "bar"), ("grants", "bar"), ("literature", "network_graph"),
    ("scicomm", "bar"),
]
for domain, fig in kd_sample_tests:
    try:
        out = OUT / f"kd_{domain}_{fig}.svg"
        generate_figure(domain, fig, common_df, str(out))
        n_kd += 1
    except Exception as e:
        kd_sample_fail.append((domain, fig, str(e)[:80]))
check(f"K-Dense sample figures drawn: {n_kd}", len(kd_sample_fail) == 0,
      f"fails={kd_sample_fail[:5]}")

# ── 4. 抽样出图（70 领域每域抽 2 图型） ─────────────
print("=" * 60)
print("[4] Sample figure generation across 70 domains")
print("=" * 60)
fig_fail = []
n_drawn = 0
for domain, figs in DOMAINS_70_ROUTING.items():
    for fig in figs[:2]:
        try:
            out = OUT / f"{domain}_{fig}.svg"
            generate_figure(domain, fig, common_df, str(out))
            n_drawn += 1
        except Exception as e:
            fig_fail.append((domain, fig, str(e)[:80]))
check(f"sample figures drawn: {n_drawn} (no exceptions)", len(fig_fail) == 0,
      f"fails={fig_fail[:5]}")

# ── 5. 汇总 ─────────────
print("=" * 60)
print(f"70 domains: {len(ALL_70_DOMAINS)} | K-Dense: {len(KDENSE_DISCIPLINE_ROUTING)} | "
      f"routing entries: {len(routing)}")
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL TESTS PASSED")
