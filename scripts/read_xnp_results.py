# -*- coding: utf-8 -*-
"""Read XNP multi-omics key result tables (read-only, no writes)."""
import pandas as pd
import sys, os
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\乌灵菌"
files = {
    "M6_pathway_class_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\MechanismAxis_DataDriven\Data\M6_pathway_class_summary.xlsx"),
    "M5_node_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\MechanismAxis_DataDriven\Data\M5_node_summary.xlsx"),
    "M1_diff_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\MechanismAxis_DataDriven\Data\M1_diff_summary.xlsx"),
    "M2_reversal_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\MechanismAxis_DataDriven\Data\M2_reversal_summary.xlsx"),
    "Step1_diff_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\DataDriven_AxisDiscovery\Data\Step1_diff_summary_by_omics_comparison.xlsx"),
    "Step2_reversal_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\DataDriven_AxisDiscovery\Data\Step2_reversal_summary_by_omics.xlsx"),
    "Step4_node_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\DataDriven_AxisDiscovery\Data\Step4_node_summary.xlsx"),
    "Step4_pair_summary": os.path.join(BASE, r"XNE血清蛋白组等5项文件\XNE多组学关联\DataDriven_AxisDiscovery\Data\Step4_pair_summary.xlsx"),
}

for name, path in files.items():
    print("=" * 80)
    print(f"### {name}")
    print(f"### {path}")
    try:
        if not os.path.exists(path):
            print("  [MISSING]")
            continue
        df = pd.read_excel(path)
        print(f"  shape: {df.shape}")
        print(f"  columns: {list(df.columns)}")
        # print first rows limited
        with pd.option_context("display.max_columns", None, "display.width", 200):
            print(df.head(15).to_string())
    except Exception as e:
        print(f"  [ERROR] {e}")
    print()
