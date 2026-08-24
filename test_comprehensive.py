#!/usr/bin/env python3
"""test_comprehensive.py - 全面数据分析引擎测试"""
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "assets"))

import numpy as np
import pandas as pd

from comprehensive_analysis import ComprehensiveAnalyzer, StatAutopilot

OUT = Path(__file__).parent / "test_output" / "comprehensive"
OUT.mkdir(parents=True, exist_ok=True)

passed, failed = [], []


def check(name, ok, detail=""):
    if ok:
        passed.append(name)
        print(f"[OK]   {name}")
    else:
        failed.append(name)
        print(f"[FAIL] {name} {detail}")


# ── 1. StatAutopilot 决策树测试 ─────────────
print("=" * 60)
print("[1] StatAutopilot decision tree")
print("=" * 60)
rng = np.random.default_rng(42)
normal_a = rng.normal(50, 10, 30)
normal_b = rng.normal(55, 10, 30)
skewed_c = rng.exponential(3, 30)
skewed_d = rng.exponential(4, 30)

rec = StatAutopilot.recommend_group_test([normal_a, normal_b])
check("normal 2-group -> t-test", rec["test"] in ["student_t", "welch_t"], rec["test"])
rec2 = StatAutopilot.recommend_group_test([skewed_c, skewed_d])
check("non-normal 2-group -> Mann-Whitney", rec2["test"] == "mann_whitney_u", rec2["test"])
rec3 = StatAutopilot.recommend_group_test([normal_a, normal_b, skewed_c])
check("mixed 3-group -> Kruskal-Wallis", rec3["test"] == "kruskal_wallis", rec3["test"])
res = StatAutopilot.run_group_test("student_t", [normal_a, normal_b])
check("t-test run", "p" in res and "effect_size" in res)
corr = StatAutopilot.recommend_correlation(normal_a, normal_b)
check("correlation auto (pearson/spearman)", corr["test"] in ["pearson", "spearman"])

# ── 2. 全面分析（generic 三组数据） ─────────────
print("=" * 60)
print("[2] Comprehensive analysis (generic)")
print("=" * 60)
df = pd.DataFrame({
    "group": np.repeat(["Ctrl", "Treat", "Model"], 40),
    "value": np.concatenate([rng.normal(50, 8, 40), rng.normal(62, 9, 40), rng.normal(45, 10, 40)]),
    "value2": np.concatenate([rng.normal(20, 4, 40), rng.normal(24, 5, 40), rng.normal(18, 4, 40)]),
    "score": rng.normal(0, 1, 120),
    "gene1": np.concatenate([rng.normal(5, 1, 40), rng.normal(8, 1.2, 40), rng.normal(4, 1, 40)]),
    "gene2": rng.normal(3, 0.8, 120),
    "time": np.random.rand(120) * 30,
    "event": np.random.binomial(1, 0.4, 120),
})
csv_path = OUT / "test_three_group.csv"
df.to_csv(csv_path, index=False)

analyzer = ComprehensiveAnalyzer(output_dir=str(OUT / "analysis_generic"))
summary = analyzer.run(str(csv_path))
ok_modules = [m for m, v in summary["modules"].items() if v["status"] == "ok"]
check("generic: all core modules ok", len(ok_modules) >= 6, f"ok={ok_modules}")
check("generic: differential ok", summary["modules"].get("differential", {}).get("status") == "ok")
check("generic: summary json saved", (OUT / "analysis_generic" / "analysis_summary.json").exists())

# 检查统计自动选择是否在结果里生效
mod = analyzer.module_results.get("group_comparison", {})
tests_used = {r.get("recommended_test") for r in mod.get("rows", [])}
print(f"  -> tests used: {tests_used}")
check("generic: autopilot tests in results", len(tests_used) >= 2)

# ── 3. 微生物组分析 ─────────────
print("=" * 60)
print("[3] Microbiome analysis")
print("=" * 60)
otu_df = pd.DataFrame({
    "sample": [f"S{i}" for i in range(30)],
    "group": np.repeat(["Ctrl", "Treat"], 15),
})
for i, taxon in enumerate([f"g_{x}" for x in "ABCDEFGHIJ"]):
    otu_df[taxon] = rng.poisson(10 + i * 2, 30)
micro_path = OUT / "test_microbiome.csv"
otu_df.to_csv(micro_path, index=False)

analyzer2 = ComprehensiveAnalyzer(output_dir=str(OUT / "analysis_micro"))
s2 = analyzer2.run(str(micro_path))
ok2 = [m for m, v in s2["modules"].items() if v["status"] == "ok"]
check("microbiome: all modules ok", len(ok2) >= 8, f"ok={ok2}")
check("microbiome: alpha_diversity ok", s2["modules"].get("alpha_diversity", {}).get("status") == "ok")
check("microbiome: composition ok", s2["modules"].get("composition", {}).get("status") == "ok")

print("=" * 60)
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL TESTS PASSED")
