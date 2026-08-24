#!/usr/bin/env python3
"""test_aris_2phase.py - ARIS 两阶段流程测试（先故事 → 证据链出图）"""
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "assets"))

import json
import numpy as np
import pandas as pd

from aris_pipeline import ARISPipeline

OUT = Path(__file__).parent / "test_output" / "aris_2phase"
OUT.mkdir(parents=True, exist_ok=True)

passed, failed = [], []


def check(name, ok, detail=""):
    if ok:
        passed.append(name)
        print(f"[OK]   {name}")
    else:
        failed.append(name)
        print(f"[FAIL] {name} {detail}")


# ── 准备模拟数据（三组差异 + 相关结构 + 生存列） ─────
rng = np.random.default_rng(42)
n = 90
df = pd.DataFrame({
    "group": np.repeat(["Ctrl", "Treat", "Model"], n // 3),
})
# 差异变量
for g, shift in [("Ctrl", 0), ("Treat", 1.2), ("Model", -0.8)]:
    df.loc[df["group"] == g, "gene_A"] = rng.normal(5 + shift, 0.8, n // 3)
df["gene_B"] = rng.normal(3, 0.6, n)
df["gene_C"] = rng.normal(7, 1.0, n)
df["gene_D"] = rng.normal(2, 0.4, n)
# 相关结构
df["biomarker"] = df["gene_A"] * 0.8 + rng.normal(0, 0.3, n)
# 生存列
df["time"] = rng.uniform(1, 30, n)
df["event"] = rng.binomial(1, 0.35, n)

csv_path = OUT / "test_study.csv"
df.to_csv(csv_path, index=False)

# ── Phase 1: 全面分析 + 故事 ─────
print("=" * 60)
print("[1] Phase 1: story generation")
print("=" * 60)
pipeline = ARISPipeline(output_dir=str(OUT / "run1"))
r1 = pipeline.phase_story(str(csv_path), "gut microbiome treatment study")

check("story generated", r1.get("status") == "success")
story_path = Path(r1["story"])
check("story.json exists", story_path.exists())
check("story.md exists", Path(r1["story_md"]).exists())
check("analysis summary exists", Path(r1["analysis_summary"]).exists())

story = json.loads(story_path.read_text(encoding="utf-8"))
check("story has 9 stages", len(story.get("stages", [])) == 9)
ev_stages = [s["id"] for s in story["stages"] if s.get("evidence")]
check("story has evidence-bound stages", len(ev_stages) >= 4, f"bound={ev_stages}")
n_ev = sum(len(s.get("evidence", [])) for s in story["stages"])
check("evidence chain non-empty", n_ev >= 5, f"evidence_items={n_ev}")

# 检查证据链是否命中真实分析结果（differential 有 p_adjusted）
s6 = next(s for s in story["stages"] if s["id"] == "S6")
diff_ev = next((e for e in s6.get("evidence", []) if e["module"] == "differential"), None)
if diff_ev:
    check("S6 differential evidence has findings", len(diff_ev.get("findings", [])) > 0)
else:
    check("S6 differential evidence has findings", False, "no differential evidence")

# ── 输出故事预览 ─────
print("\n--- story.md 预览 ---")
print(Path(r1["story_md"]).read_text(encoding="utf-8")[:1200])
print("...\n")

# ── Phase 2: 故事驱动证据链出图 ─────
print("=" * 60)
print("[2] Phase 2: story-driven figures")
print("=" * 60)
r2 = pipeline.phase_figures(str(csv_path), str(story_path))
check("figures generated", r2.get("status") == "success")
files = r2.get("generated_files", [])
check(">=5 figures generated", len(files) >= 5, f"n={len(files)}")
for f in files:
    print(f"    -> {Path(f).name}")
check("evidence_chain.md exists", (OUT / "run1" / "evidence_chain.md").exists())
check("figures are real files", all(Path(f).exists() and Path(f).stat().st_size > 500 for f in files))

print("=" * 60)
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL TESTS PASSED")
