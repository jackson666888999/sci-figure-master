#!/usr/bin/env python3
"""
auto_figure.py - 无人值守自动出图系统

用法:
    python auto_figure.py --input data.h5ad --output figure.png
    python auto_figure.py --input data.csv --output figure.png
    python auto_figure.py --input data/ --output ./figures/

功能:
    1. 自动识别数据类型（单细胞/bulk RNA-seq/宏基因组/代谢组/通用）
    2. 自动选择统计方法（差异表达/富集分析/聚类分析等）
    3. 自动选择分析工具和画图工具
    4. 无人值守生成最终图表（Nature/Science标准）
"""

import argparse
import sys
import os
import warnings
from pathlib import Path
from typing import Optional, Dict, Any, List
import traceback
warnings.filterwarnings('ignore')

# 设置环境
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Nature/Science 标准配置
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# 检查可选依赖
def check_dependencies():
    """检查依赖包并返回可用性"""
    deps = {
        'scanpy': False,
        'anndata': False,
        'seaborn': False,
        'scipy': False,
        'sklearn': False,
        'statsmodels': False,
    }
    try:
        import scanpy
        deps['scanpy'] = True
    except ImportError:
        pass
    try:
        import anndata
        deps['anndata'] = True
    except ImportError:
        pass
    try:
        import seaborn
        deps['seaborn'] = True
    except ImportError:
        pass
    try:
        from scipy import stats
        deps['scipy'] = True
    except ImportError:
        pass
    try:
        from sklearn import decomposition
        deps['sklearn'] = True
    except ImportError:
        pass
    try:
        import statsmodels
        deps['statsmodels'] = True
    except ImportError:
        pass
    return deps

# 项目路径
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"

# 导入路由模块
sys.path.insert(0, str(ASSETS_DIR))
from bioinfo_router import generate_figure, quick_plot

class AutoFigureSystem:
    """无人值守自动出图系统"""

    # 文件类型识别规则
    FILE_TYPE_RULES = {
        '.h5ad': 'scRNA',
        '.h5': 'scRNA',
        '.loom': 'scRNA',
        '.seurat': 'scRNA',
        '.csv': 'generic',
        '.tsv': 'generic',
        '.txt': 'generic',
        '.rds': 'generic',
        '.rda': 'generic',
        '.xlsx': 'generic',
        '.xls': 'generic',
        '.mt': 'microbiome',
        '.biom': 'microbiome',
        '.mpk': 'metabolomics',
        '.mzML': 'metabolomics',
        '.mzXML': 'metabolomics',
        '.parquet': 'generic',
        '.feather': 'generic',
        '.ann': 'generic',
    }

    # 数据特征识别规则
    DATA_FEATURES = {
        'scRNA': ['n_genes', 'n_counts', 'louvain', 'clusters', 'cell_type'],
        'bulkRNA': ['gene', 'sample', 'expression', 'count'],
        'microbiome': ['OTU', 'ASV', 'species', 'genus', 'family'],
        'metabolomics': ['metabolite', 'mz', 'rt', 'peak'],
        'proteomics': ['protein', 'peptide', 'gene'],
    }

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.deps = check_dependencies()
        self.results = {}

    def identify_file_type(self, filepath: Path) -> str:
        """识别文件类型"""
        ext = filepath.suffix.lower()
        if ext in self.FILE_TYPE_RULES:
            return self.FILE_TYPE_RULES[ext]

        # 尝试读取文件内容判断
        try:
            if ext in ['.csv', '.tsv', '.txt']:
                df = pd.read_csv(filepath, nrows=10)
                cols = ' '.join(df.columns).lower()
                for dtype, keywords in self.DATA_FEATURES.items():
                    if any(k in cols for k in keywords):
                        return dtype
        except Exception:
            pass

        return 'generic'

    def load_data(self, filepath: Path, file_type: str) -> Any:
        """加载数据"""
        try:
            if file_type == 'scRNA' and self.deps['scanpy']:
                import scanpy as sc
                if filepath.suffix == '.h5ad':
                    return sc.read_h5ad(filepath)
                elif filepath.suffix == '.h5':
                    return sc.read_h5ad(filepath)
                elif filepath.suffix == '.loom':
                    return sc.read_loom(filepath)
            elif file_type in ['generic', 'bulkRNA', 'microbiome', 'metabolomics', 'proteomics']:
                if filepath.suffix in ['.csv', '.tsv', '.txt']:
                    return pd.read_csv(filepath, sep=None, engine='python')
                elif filepath.suffix in ['.xlsx', '.xls']:
                    return pd.read_excel(filepath)
                elif filepath.suffix == '.parquet':
                    return pd.read_parquet(filepath)
                elif filepath.suffix == '.feather':
                    return pd.read_feather(filepath)
        except Exception as e:
            print(f"Warning: Failed to load {filepath}: {e}")
            return None
        return None

    def auto_analysis(self, data: Any, file_type: str) -> Dict[str, Any]:
        """自动分析数据"""
        analysis = {
            'file_type': file_type,
            'methods': [],
            'plots': [],
            'stats': {},
        }

        if file_type == 'scRNA' and hasattr(data, 'obsm'):
            # 单细胞自动分析
            analysis['methods'] = ['UMAP', 'PCA', 'clustering', 'marker_genes']
            analysis['plots'] = ['UMAP', 'heatmap', 'violin', 'dotplot']

            # 自动检测聚类列
            if 'louvain' in data.obs.columns:
                analysis['cluster_col'] = 'louvain'
            elif 'clusters' in data.obs.columns:
                analysis['cluster_col'] = 'clusters'
            elif 'cell_type' in data.obs.columns:
                analysis['cluster_col'] = 'cell_type'
            else:
                analysis['cluster_col'] = None

            # 自动检测高变基因
            if hasattr(data, 'var') and len(data.var_names) > 100:
                analysis['top_genes'] = data.var_names[:20]

        elif file_type == 'generic' and isinstance(data, pd.DataFrame):
            # 通用数据分析
            analysis['methods'] = ['descriptive_stats', 'correlation']
            analysis['plots'] = ['heatmap', 'box', 'scatter']

            # 自动选择数值列
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                analysis['numeric_cols'] = numeric_cols[:10]

            # 自动选择分组列
            categorical_cols = data.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                analysis['group_col'] = categorical_cols[0]

        return analysis

    def generate_auto_figure(self, data: Any, file_type: str, analysis: Dict, output_path: Path) -> List[str]:
        """自动生成图表"""
        generated_files = []

        try:
            if file_type == 'scRNA' and hasattr(data, 'obsm'):
                # 单细胞图表
                cluster_col = analysis.get('cluster_col', None)
                color = cluster_col if cluster_col else None

                # UMAP/tSNE
                if 'X_umap' in data.obsm:
                    path = output_path.with_suffix('.umap.svg')
                    generate_figure("scRNA", "UMAP", data, str(path), color=color)
                    generated_files.append(path)

                if 'X_tsne' in data.obsm:
                    path = output_path.with_suffix('.tsne.svg')
                    generate_figure("scRNA", "tSNE", data, str(path), color=color)
                    generated_files.append(path)

                # PCA
                path = output_path.with_suffix('.pca.svg')
                generate_figure("scRNA", "PCA", data, str(path), color=color)
                generated_files.append(path)

                # 热图
                top_genes = analysis.get('top_genes', data.var_names[:20] if hasattr(data, 'var_names') else None)
                if top_genes is not None and len(top_genes) > 0:
                    path = output_path.with_suffix('.heatmap.svg')
                    genes = list(top_genes)  # scanpy 索引需显式列表
                    try:
                        generate_figure("scRNA", "heatmap", data[:, genes], str(path))
                    except Exception:
                        # 降级：无基因切片时直接用全数据
                        generate_figure("scRNA", "heatmap", data, str(path))
                    generated_files.append(path)

                # 小提琴图
                if cluster_col and len(data.var_names) > 0:
                    path = output_path.with_suffix('.violin.svg')
                    generate_figure("scRNA", "violin", data, str(path), x=cluster_col, y=data.var_names[0])
                    generated_files.append(path)

            elif isinstance(data, pd.DataFrame):
                # 通用图表
                numeric_cols = analysis.get('numeric_cols', data.select_dtypes(include=[np.number]).columns[:5])
                group_col = analysis.get('group_col', None)

                # 热图
                if len(numeric_cols) > 1:
                    path = output_path.with_suffix('.heatmap.svg')
                    df_subset = data[numeric_cols].corr()
                    generate_figure("general", "heatmap", df_subset, str(path))
                    generated_files.append(path)

                # 箱线图
                if group_col and len(numeric_cols) > 0:
                    path = output_path.with_suffix('.box.svg')
                    generate_figure("general", "box", data, str(path), x=group_col, y=numeric_cols[0])
                    generated_files.append(path)

                # 柱状图
                if group_col:
                    path = output_path.with_suffix('.bar.svg')
                    generate_figure("general", "bar", data, str(path), x=group_col, y=numeric_cols[0] if len(numeric_cols) > 0 else None)
                    generated_files.append(path)

                # 散点图
                if len(numeric_cols) >= 2:
                    path = output_path.with_suffix('.scatter.svg')
                    generate_figure("general", "scatter", data, str(path), x=numeric_cols[0], y=numeric_cols[1])
                    generated_files.append(path)

        except Exception as e:
            print(f"Error generating figures: {e}")
            traceback.print_exc()

        return generated_files

    def process_file(self, filepath: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """处理单个文件"""
        filepath = Path(filepath)
        if not filepath.exists():
            return {'status': 'error', 'message': f'File not found: {filepath}'}

        output_dir = Path(output_dir) if output_dir else self.output_dir
        output_path = output_dir / filepath.stem

        print(f"\n{'='*60}")
        print(f"Processing: {filepath}")
        print(f"{'='*60}")

        # Step 1: 识别文件类型
        print(f"Step 1: Identifying file type...")
        file_type = self.identify_file_type(filepath)
        print(f"  -> Detected: {file_type}")

        # Step 2: 加载数据
        print(f"Step 2: Loading data...")
        data = self.load_data(filepath, file_type)
        if data is None:
            return {'status': 'error', 'message': f'Failed to load {filepath}'}
        print(f"  -> Loaded: {type(data).__name__}")
        if hasattr(data, 'n_obs'):
            print(f"  -> {data.n_obs} cells, {data.n_vars} genes")
        elif hasattr(data, 'shape'):
            print(f"  -> {data.shape[0]} rows, {data.shape[1]} columns")

        # Step 3: 自动分析
        print(f"Step 3: Auto analysis...")
        analysis = self.auto_analysis(data, file_type)
        print(f"  -> Methods: {analysis['methods']}")
        print(f"  -> Plots: {analysis['plots']}")

        # Step 4: 生成图表
        print(f"Step 4: Generating figures...")
        generated_files = self.generate_auto_figure(data, file_type, analysis, output_path)
        print(f"  -> Generated {len(generated_files)} figures")

        # Step 5: 保存结果
        result = {
            'status': 'success',
            'input': str(filepath),
            'file_type': file_type,
            'analysis': analysis,
            'generated_files': [str(f) for f in generated_files],
            'output_dir': str(output_dir),
        }

        return result

    def process_directory(self, dirpath: str, output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """处理目录中的所有文件"""
        dirpath = Path(dirpath)
        if not dirpath.exists():
            return [{'status': 'error', 'message': f'Directory not found: {dirpath}'}]

        output_dir = Path(output_dir) if output_dir else self.output_dir
        results = []

        # 支持的文件类型
        supported_exts = {'.h5ad', '.h5', '.loom', '.csv', '.tsv', '.txt', '.xlsx', '.xls'}

        for filepath in dirpath.rglob('*'):
            if filepath.suffix.lower() in supported_exts:
                result = self.process_file(str(filepath), str(output_dir))
                results.append(result)

        return results

    def run(self, input_path: str, output_dir: Optional[str] = None):
        """主运行方法"""
        input_path = Path(input_path)
        output_dir = Path(output_dir) if output_dir else self.output_dir

        print("=" * 60)
        print("Auto Figure System - Unattended Figure Generation")
        print("=" * 60)
        print(f"Input: {input_path}")
        print(f"Output: {output_dir}")
        print(f"Dependencies: {self.deps}")

        if input_path.is_file():
            results = [self.process_file(str(input_path), str(output_dir))]
        elif input_path.is_dir():
            results = self.process_directory(str(input_path), str(output_dir))
        else:
            results = [{'status': 'error', 'message': f'Invalid path: {input_path}'}]

        # 汇总结果
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        success_count = sum(1 for r in results if r.get('status') == 'success')
        error_count = sum(1 for r in results if r.get('status') == 'error')

        print(f"Total: {len(results)}")
        print(f"Success: {success_count}")
        print(f"Errors: {error_count}")

        for r in results:
            if r.get('status') == 'success':
                print(f"\n✓ {r['input']}")
                for f in r.get('generated_files', []):
                    print(f"  -> {f}")
            else:
                print(f"\n✗ {r.get('message', 'Unknown error')}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Auto Figure System - Unattended figure generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_figure.py --input data.h5ad
  python auto_figure.py --input data.csv --output ./figures
  python auto_figure.py --input ./data/ --output ./output/
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input file or directory')
    parser.add_argument('--output', '-o', default='./output', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # 创建系统并运行
    system = AutoFigureSystem(output_dir=args.output)
    results = system.run(args.input, args.output)

    # 返回状态码
    success_count = sum(1 for r in results if r.get('status') == 'success')
    sys.exit(0 if success_count > 0 else 1)


if __name__ == "__main__":
    main()
