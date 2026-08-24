#!/usr/bin/env python3
"""
auto_figure_test.py - 无人值守出图系统测试
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from auto_figure import AutoFigureSystem

# 输出根目录（绝对路径，防止相对路径写错盘）
BASE_OUT = Path(__file__).parent / "test_output" / "auto_figure"
BASE_OUT.mkdir(parents=True, exist_ok=True)

def test_auto_figure():
    """测试无人值守出图"""
    print("=" * 60)
    print("Auto Figure System Test")
    print("=" * 60)

    # 创建系统
    system = AutoFigureSystem(output_dir=str(BASE_OUT))

    # 测试1: 创建模拟单细胞数据
    print("\n[Test 1] Simulated scRNA-seq data...")
    try:
        import numpy as np
        import pandas as pd

        # 创建模拟AnnData
        np.random.seed(42)
        n_cells = 100
        n_genes = 50
        data = np.random.randn(n_cells, n_genes)

        # 创建模拟AnnData对象
        try:
            import scanpy as sc
            from anndata import AnnData

            adata = AnnData(data)
            adata.var_names = [f'Gene{i}' for i in range(n_genes)]
            adata.obs_names = [f'Cell{i}' for i in range(n_cells)]

            # 添加模拟聚类
            adata.obs['louvain'] = pd.Categorical(np.random.choice(['A', 'B', 'C'], n_cells))
            adata.obs['n_genes'] = np.random.poisson(1000, n_cells)
            adata.obs['total_counts'] = np.random.poisson(5000, n_cells)

            # 添加UMAP坐标
            adata.obsm['X_umap'] = np.random.randn(n_cells, 2)
            adata.obsm['X_tsne'] = np.random.randn(n_cells, 2)
            adata.obsm['X_pca'] = np.random.randn(n_cells, 2)

            # 保存为h5ad
            test_path = BASE_OUT / "test_scRNA.h5ad"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            adata.write_h5ad(test_path)
            print(f"  ✓ Saved: {test_path}")

            # 处理文件
            results = system.process_file(str(test_path))
            print(f"  Status: {results.get('status')}")
            for f in results.get('generated_files', []):
                print(f"    -> {f}")

        except ImportError:
            print("  ! scanpy/anndata not available, using simple test")
            df = pd.DataFrame(data, columns=[f'Gene{i}' for i in range(n_genes)])
            df['group'] = np.random.choice(['A', 'B', 'C'], n_cells)
            test_path = BASE_OUT / "test_generic.csv"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(test_path)
            print(f"  ✓ Saved: {test_path}")
            results = system.process_file(str(test_path))
            print(f"  Status: {results.get('status')}")

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()

    # 测试2: 创建模拟CSV数据
    print("\n[Test 2] Simulated CSV data...")
    try:
        np.random.seed(42)
        df = pd.DataFrame({
            'group': np.random.choice(['Control', 'Treatment'], 100),
            'value': np.random.randn(100) * 10 + 50,
            'gene1': np.random.randn(100),
            'gene2': np.random.randn(100),
            'gene3': np.random.randn(100),
        })
        test_path = BASE_OUT / "test_data.csv"
        test_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(test_path)
        print(f"  ✓ Saved: {test_path}")

        results = system.process_file(str(test_path))
        print(f"  Status: {results.get('status')}")
        for f in results.get('generated_files', []):
            print(f"    -> {f}")

    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_auto_figure()
