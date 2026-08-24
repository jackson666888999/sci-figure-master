#!/usr/bin/env python3
"""
bioinfo_router_test.py - 路由系统快速测试
"""

import sys
import os
from pathlib import Path

# 设置UTF-8输出
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "assets"))

from bioinfo_router import generate_figure, quick_plot

def test_router():
    """测试路由系统"""
    print("=" * 60)
    print("Bioinfo Router Test")
    print("=" * 60)

    # 创建测试数据
    try:
        import scanpy as sc
        import numpy as np
        adata = sc.datasets.pbmc68k_reduced()
        print(f"[OK] Test data: {adata.n_obs} cells, {adata.n_vars} genes")
    except ImportError:
        print("[SKIP] scanpy not installed, using mock data")
        import pandas as pd
        np.random.seed(42)
        adata = pd.DataFrame(
            np.random.randn(100, 10),
            columns=[f'Gene{i}' for i in range(10)]
        )
        adata['group'] = np.random.choice(['A', 'B', 'C'], 100)

    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)

    # 测试1: UMAP
    print("\n[Test 1] UMAP (scanpy)...")
    try:
        path = output_dir / "test_UMAP.svg"
        generate_figure("scRNA", "UMAP", adata, path, color="louvain")
        print(f"  [OK] {path}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    # 测试2: 热图
    print("\n[Test 2] Heatmap...")
    try:
        path = output_dir / "test_heatmap.svg"
        generate_figure("scRNA", "heatmap", adata, path)
        print(f"  [OK] {path}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    # 测试3: 快速绘图
    print("\n[Test 3] Quick Plot (auto)...")
    try:
        path = output_dir / "test_quick.svg"
        quick_plot(adata, path)
        print(f"  [OK] {path}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    # 测试4: 箱线图
    print("\n[Test 4] Box Plot...")
    try:
        path = output_dir / "test_box.svg"
        generate_figure("general", "box", adata, path, x="louvain", y="n_genes_by_counts")
        print(f"  [OK] {path}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    # 测试5: 点图
    print("\n[Test 5] Dot Plot...")
    try:
        path = output_dir / "test_dotplot.svg"
        generate_figure("scRNA", "dotplot", adata, path)
        print(f"  [OK] {path}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print(f"Output directory: {output_dir.absolute()}")

if __name__ == "__main__":
    test_router()
