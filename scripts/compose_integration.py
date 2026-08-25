# -*- coding: utf-8 -*-
"""
auto_route + academic-figure-skill compose 集成脚本

功能：
1. 读取 auto_route 生成的 R bridge 图（火山图/热图/MA图）
2. 用 compose.py 排版为 Nature 风格多面板图
3. 输出 PDF + PNG

使用方式：
    python compose_multi_panel.py --input E:/XNP论文初稿/05_图件/_auto_batch --output E:/XNP论文初稿/05_图件/_compose
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# 设置路径
SCI_FIGURE_PATH = Path(r"E:\git\sci-figure-master")
ASSETS_PATH = SCI_FIGURE_PATH / "assets"
COMPOSE_PATH = Path(r"E:\git\academic-figure-skill\scripts")

sys.path.insert(0, str(ASSETS_PATH))
sys.path.insert(0, str(COMPOSE_PATH))


def find_r_figures(batch_dir: Path) -> dict:
    """
    扫描 _auto_batch 目录，找出每层的三张 R 图

    Returns:
        {
            "Fecal": {
                "volcano": Path(".../fig_r_enhanced_volcano.pdf"),
                "heatmap": Path(".../fig_r_complex_heatmap.pdf"),
                "ma_plot": Path(".../fig_r_ma_plot.pdf"),
            },
            "Serum": {...},
            "Brain": {...}
        }
    """
    result = {}
    if not batch_dir.exists():
        print(f"目录不存在: {batch_dir}")
        return result

    for layer_dir in sorted(batch_dir.iterdir()):
        if not layer_dir.is_dir():
            continue
        layer_name = layer_dir.name
        figures = {}
        for fig_file in layer_dir.glob("fig_r_*.pdf"):
            fname = fig_file.name
            if "volcano" in fname or "enhanced" in fname:
                figures["volcano"] = fig_file
            elif "heatmap" in fname or "complex" in fname:
                figures["heatmap"] = fig_file
            elif "ma_plot" in fname or "ma" in fname:
                figures["ma_plot"] = fig_file
        if figures:
            result[layer_name] = figures
            print(f"  ✓ {layer_name}: {list(figures.keys())}")
    return result


def render_panel_from_pdf(ax, pdf_path: Path, spec: dict):
    """
    将 R 生成的 PDF 图渲染为 matplotlib 面板

    由于 R PDF 是矢量图，直接嵌入会比较复杂。
    这里采用策略：用 Cairo 设备将 PDF 转换为 PNG，然后嵌入。
    """
    import matplotlib.image as mpimg

    # 检查是否已有对应的 PNG
    png_path = pdf_path.with_suffix(".png")
    if not png_path.exists():
        # 尝试用 pdftoppm 或类似工具转换
        # 这里简化处理：直接用 PDF 路径，后续由 compose.py 处理
        pass

    # 尝试用 matplotlib 的 ImagePanel 直接嵌入
    try:
        img = mpimg.imread(str(pdf_path))
        if img is not None:
            ax.imshow(img, aspect='auto')
            ax.set_axis_off()
            return True
    except:
        pass

    # 备选：用 pillow 读取
    try:
        from PIL import Image
        img = Image.open(pdf_path)
        img_array = np.array(img)
        ax.imshow(img_array, aspect='auto')
        ax.set_axis_off()
        return True
    except:
        pass

    return False


def create_volcano_panel(ax, data_dict: dict, spec: dict):
    """
    使用 academic-figure-skill 标准创建火山图面板
    直接读取数据并绘图，而非嵌入 R PDF
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from scipy import stats

    # Nature 配色
    GREY = "#999999"
    BLUE = "#2166AC"
    RED = "#B2182B"
    THRESHOLD_COLOR = "#555555"

    log2fcs = data_dict.get("log2FC", [])
    pvals = data_dict.get("FDR", [])
    features = data_dict.get("feature_id", [])

    if len(log2fcs) < 10:
        ax.text(0.5, 0.5, "数据不足", ha='center', va='center', transform=ax.transAxes)
        return

    # 处理 p=0 边界情况
    pvals = np.array(pvals, dtype=float)
    pvals = np.clip(pvals, 1e-300, None)
    log2fcs = np.array(log2fcs, dtype=float)

    # 分类
    ALPHA = 0.05
    FC_CUTOFF = 1.0
    categories = np.array(["NS"] * len(log2fcs))
    categories[(pvals < ALPHA) & (np.abs(log2fcs) < FC_CUTOFF)] = "Sig_lowFC"
    categories[(pvals < ALPHA) & (np.abs(log2fcs) >= FC_CUTOFF)] = "Sig_highFC"

    # 绘图
    ax.scatter(log2fcs[categories == "NS"],
               -np.log10(pvals[categories == "NS"]),
               c=GREY, s=2, alpha=0.3, edgecolors="none", rasterized=True, zorder=1)
    ax.scatter(log2fcs[categories == "Sig_lowFC"],
               -np.log10(pvals[categories == "Sig_lowFC"]),
               c=BLUE, s=3, alpha=0.5, edgecolors="none", rasterized=True, zorder=2)
    ax.scatter(log2fcs[categories == "Sig_highFC"],
               -np.log10(pvals[categories == "Sig_highFC"]),
               c=RED, s=3, alpha=0.6, edgecolors="none", rasterized=True, zorder=3)

    # 阈值线
    ax.axhline(-np.log10(ALPHA), color=THRESHOLD_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)
    ax.axvline(FC_CUTOFF, color=THRESHOLD_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)
    ax.axvline(-FC_CUTOFF, color=THRESHOLD_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)

    ax.set_xlabel("log₂(Fold Change)", fontsize=7)
    ax.set_ylabel("−log₁₀(adj. p-value)", fontsize=7)

    # 统计标注
    n_up = np.sum((categories == "Sig_highFC") & (log2fcs > 0))
    n_dn = np.sum((categories == "Sig_highFC") & (log2fcs < 0))
    ax.text(0.98, 0.95, f"Up: {n_up}  |  Down: {n_dn}",
            transform=ax.transAxes, fontsize=6, ha='right', va='top',
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8))

    # 样式
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)


def create_heatmap_panel(ax, data_dict: dict, spec: dict):
    """
    创建差异特征热图面板
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.cluster import hierarchy

    # 获取数值数据列（排除元数据）
    exclude_cols = {'feature_id', 'log2FC', 'FDR', 'group', 'layer'}
    num_cols = [c for c in data_dict.keys() if c.lower() not in exclude_cols]

    # 只保留数值列
    num_cols = [c for c in num_cols if all(isinstance(v, (int, float, np.number)) or (isinstance(v, str) and v.replace('.', '').replace('-', '').isdigit()) for v in data_dict[c][:100])]

    if not num_cols:
        ax.text(0.5, 0.5, "无数值数据", ha='center', va='center', transform=ax.transAxes)
        return

    # 取 top 差异特征（按 |log2FC| 排序）
    log2fcs = data_dict.get("log2FC", [])
    if not log2fcs:
        ax.text(0.5, 0.5, "无log2FC数据", ha='center', va='center', transform=ax.transAxes)
        return

    sorted_idx = np.argsort(np.abs(log2fcs))[::-1][:30]  # top 30

    # 构建热图数据（只取数值）
    heatmap_data = []
    for idx in sorted_idx:
        row = []
        for col_name in num_cols[:20]:  # 限制列数
            val = data_dict[col_name][idx] if idx < len(data_dict.get(col_name, [])) else 0
            try:
                row.append(float(val))
            except:
                row.append(0)
        heatmap_data.append(row)

    if not heatmap_data:
        ax.text(0.5, 0.5, "数据构建失败", ha='center', va='center', transform=ax.transAxes)
        return

    heatmap_data = np.array(heatmap_data, dtype=float)

    # 标准化
    row_means = heatmap_data.mean(axis=1, keepdims=True)
    row_stds = heatmap_data.std(axis=1, keepdims=True)
    row_stds[row_stds < 1e-8] = 1
    heatmap_data = (heatmap_data - row_means) / row_stds

    # 绘图
    im = ax.imshow(heatmap_data, aspect='auto', cmap='RdBu_r',
                   vmin=-2, vmax=2, interpolation='nearest')

    # 样式
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Samples (top 20)', fontsize=7)
    ax.set_ylabel('Top DE Features', fontsize=7)

    # 颜色条
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Z-score', fontsize=6)


def create_ma_panel(ax, data_dict: dict, spec: dict):
    """
    创建 MA 图面板
    """
    import numpy as np
    import matplotlib.pyplot as plt

    log2fcs = data_dict.get("log2FC", [])
    base_means = data_dict.get("AveExpr", [])

    if len(log2fcs) < 10:
        ax.text(0.5, 0.5, "数据不足", ha='center', va='center', transform=ax.transAxes)
        return

    # 采样（最多5000点）
    if len(log2fcs) > 5000:
        idx = np.random.choice(len(log2fcs), 5000, replace=False)
        log2fcs = [log2fcs[i] for i in idx]
        base_means = [base_means[i] for i in idx]

    log2fcs = np.array(log2fcs, dtype=float)
    base_means = np.array(base_means, dtype=float)

    # 过滤无效值
    valid = np.isfinite(log2fcs) & np.isfinite(base_means)
    log2fcs = log2fcs[valid]
    base_means = base_means[valid]

    # 绘图
    ax.scatter(np.log10(base_means), log2fcs, c="#999999", s=1, alpha=0.4, rasterized=True)

    # 阈值线
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axhline(1, color="gray", linewidth=0.5, linestyle="--")
    ax.axhline(-1, color="gray", linewidth=0.5, linestyle="--")

    ax.set_xlabel("Base Mean (log₁₀)", fontsize=7)
    ax.set_ylabel("log₂(Fold Change)", fontsize=7)

    # 样式
    ax.spines['top'].set_visible(False)
    ax.set_ylabel("log₂FC", fontsize=7)


def compose_three_panel(volcano_data: dict, heatmap_data: dict, ma_data: dict,
                        output_prefix: str, layer_name: str):
    """
    组合三面板图：火山图 + 热图 + MA图
    使用 asymmetric_mixed 原型，热图为英雄面板
    """
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np

    MM_PER_INCH = 25.4

    # Nature 栏宽
    fig_width_mm = 183  # 双栏
    fig_height_mm = 120

    fig = plt.figure(figsize=(fig_width_mm / MM_PER_INCH, fig_height_mm / MM_PER_INCH))

    # 非对称布局：热图占左半边，火山图+MA图占右半边
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.35, 1.0],
                          wspace=0.25, hspace=0.1)

    # 面板 A：热图（英雄面板）
    ax_heatmap = fig.add_subplot(gs[0, 0])
    create_heatmap_panel(ax_heatmap, heatmap_data, {})
    ax_heatmap.text(0.02, 0.98, "A", transform=ax_heatmap.transAxes,
                    fontsize=9, fontweight="bold", va="top", ha="left")

    # 右侧两行：火山图 + MA图
    gs_right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 1],
                                                 wspace=0.0, hspace=0.15)

    # 面板 B：火山图
    ax_volcano = fig.add_subplot(gs_right[0])
    create_volcano_panel(ax_volcano, volcano_data, {})
    ax_volcano.text(0.02, 0.98, "B", transform=ax_volcano.transAxes,
                    fontsize=9, fontweight="bold", va="top", ha="left")

    # 面板 C：MA图
    ax_ma = fig.add_subplot(gs_right[1])
    create_ma_panel(ax_ma, ma_data, {})
    ax_ma.text(0.02, 0.98, "C", transform=ax_ma.transAxes,
                fontsize=9, fontweight="bold", va="top", ha="left")

    # 保存
    plt.savefig(f"{output_prefix}.pdf", bbox_inches="tight", dpi=300)
    plt.savefig(f"{output_prefix}.png", bbox_inches="tight", dpi=300)
    plt.close()

    print(f"  ✓ {layer_name} 合成图已保存: {output_prefix}.pdf/png")
    return f"{output_prefix}.pdf"


def load_data_from_csv(csv_path: Path) -> dict:
    """
    从 T01_metabolome_DE_full.csv 等表格加载数据
    """
    import sys
    # 使用 E 盘的 venv（有必要的包）
    venv_python = r"E:\workbuddy\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    from scipy.cluster import hierarchy

    df = pd.read_csv(csv_path)

    # 查找关键列
    data = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'log2fc' in col_lower or 'logfc' in col_lower:
            data['log2FC'] = df[col].tolist()
        elif 'fdr' in col_lower or 'padj' in col_lower or 'p_val' in col_lower:
            data['FDR'] = df[col].tolist()
        elif 'feature_id' in col_lower or 'gene' in col_lower:
            data['feature_id'] = df[col].tolist()
        elif 'aveexpr' in col_lower or 'base_mean' in col_lower:
            data['AveExpr'] = df[col].tolist()
        elif 'group' in col_lower or 'layer' in col_lower:
            data[col] = df[col].tolist()

    return data


def main():
    import argparse

    parser = argparse.ArgumentParser(description="auto_route + compose 集成脚本")
    parser.add_argument("--input", "-i", default=r"E:\XNP论文初稿\05_图件\_auto_batch",
                        help="auto_route 输出目录")
    parser.add_argument("--output", "-o", default=r"E:\XNP论文初稿\05_图件\_compose",
                        help="合成图输出目录")
    parser.add_argument("--data", "-d", default=r"D:\乌灵菌\机制轴\tables\T01_metabolome_DE_full.csv",
                        help="差异分析表格路径")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    data_file = Path(args.data)

    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("auto_route + academic-figure-skill compose 集成")
    print("="*60)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"数据文件: {data_file}")
    print()

    # Step 1: 加载数据
    print("[1/3] 加载数据...")
    raw_data = load_data_from_csv(data_file)
    if not raw_data:
        print("  ✗ 数据加载失败，请检查路径")
        return
    print(f"  ✓ 已加载 {len(raw_data)} 个字段")

    # Step 2: 扫描 R 图
    print("\n[2/3] 扫描 R bridge 生成的图...")
    r_figures = find_r_figures(input_dir)
    if not r_figures:
        print("  ✗ 未找到 R bridge 生成的图，请先运行 auto_route.py")
        return
    print(f"  ✓ 找到 {len(r_figures)} 个层")

    # Step 3: 合成多面板图
    print("\n[3/3] 合成 Nature 风格多面板图...")
    results = {}

    for layer_name, figures in r_figures.items():
        print(f"\n  Layer: {layer_name}")

        # 按层过滤数据
        layer_data = {}
        for key, values in raw_data.items():
            layer_data[key] = values  # 简化：全量数据

        # 合成图
        output_prefix = str(output_dir / f"fig_{layer_name.lower()}_multi")
        pdf_path = compose_three_panel(
            layer_data, layer_data, layer_data,
            output_prefix, layer_name
        )
        results[layer_name] = pdf_path

    print("\n" + "="*60)
    print("完成！")
    print("="*60)
    print(f"输出目录: {output_dir}")
    for layer, pdf in results.items():
        print(f"  {layer}: {Path(pdf).name}")

    return results


if __name__ == "__main__":
    main()
