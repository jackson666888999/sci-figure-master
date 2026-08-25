# -*- coding: utf-8 -*-
"""
自动路由统计方法 + 复杂图生成（集成 academic-figure-skill 标准）

工作流：
1. 检测数据结构 → 自动选统计方法
2. 根据方法选图型 → R bridge（火山/热图/MA plot）或 Python 原生
3. 输出 Nature 级多面板图

使用示例：
    from auto_route import auto_route_and_plot
    df = pd.read_csv('T01_metabolome_DE_full.csv')
    fecal = df[df['layer']=='Fecal']
    auto_route_and_plot(fecal, 'output/', domain='metabolomics')
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# academic-figure-skill 配色（Nature/Cell/Science 标准）
NATURE_PALETTE = ["#08519C", "#A50F15", "#006D2C", "#D94801", "#54278F", "#525252"]
GROUP_ORDER = ["Control", "Model", "XNP"]
GROUP_COL = {"Control": NATURE_PALETTE[0], "Model": NATURE_PALETTE[1], "XNP": NATURE_PALETTE[2]}


# ─────────────────────────────────────────────────────────────
# 1. 数据结构检测
# ─────────────────────────────────────────────────────────────
def detect_structure(df: pd.DataFrame) -> str:
    """检测 DataFrame 结构类型"""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n_num, n_cat = len(num_cols), len(cat_cols)
    cl = {c.lower(): c for c in df.columns}

    has_fc = any(any(k in key for k in ("log2fc", "logfc", "foldchange", "lfc", "fc")) for key in cl)
    has_p = any(any(k in key for k in ("pvalue", "padj", "p_value", "qvalue", "fdr", "_p", "_q")) for key in cl)
    if has_fc and has_p and n_num >= 2:
        return "diff"

    has_time = any(k in cl for k in ("time", "survival", "os", "days", "months", "followup"))
    has_event = any(k in cl for k in ("event", "status", "censor", "cns", "outcome"))
    if has_time and has_event:
        return "surv"

    if n_cat >= 1 and n_num >= 1:
        return "grouped"
    if n_num >= 3:
        return "wide"
    if n_num == 2:
        return "two_num"
    if n_num == 1:
        return "single"
    return "count"


# ─────────────────────────────────────────────────────────────
# 2. 统计方法自动选择
# ─────────────────────────────────────────────────────────────
def select_stat_method(struct: str, df: pd.DataFrame) -> Dict:
    """
    根据数据结构和领域选择统计方法

    Returns:
        {
            "test": "名称",
            "func": "scipy.stats 函数或 None",
            "params": {},
            "note": "说明"
        }
    """
    if struct == "diff":
        # 差异分析：默认用 t-test（参数）或 Mann-Whitney（非参数）
        # 先做正态性检验
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) >= 2:
            col1, col2 = num_cols[0], num_cols[1]
            try:
                from scipy import stats
                _, p_norm = stats.shapiro(df[col1].dropna().head(50))
                if p_norm > 0.05:
                    return {
                        "test": "Welch's t-test",
                        "func": lambda x, y: stats.ttest_ind(x, y, equal_var=False),
                        "params": {"col1": col1, "col2": col2},
                        "note": "正态分布，使用参数检验"
                    }
            except:
                pass
        return {
            "test": "Mann-Whitney U test",
            "func": None,
            "params": {},
            "note": "非正态或样本量不足，使用非参数检验"
        }

    elif struct == "grouped":
        # 多组比较：ANOVA 或 Kruskal-Wallis
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if len(num_cols) >= 1 and len(cat_cols) >= 1:
            y_col = num_cols[0]
            g_col = cat_cols[0]
            groups = df[g_col].unique()
            if len(groups) == 2:
                return {
                    "test": "Welch's t-test",
                    "func": None,
                    "params": {"y_col": y_col, "g_col": g_col},
                    "note": "两组比较，使用 t-test"
                }
            elif len(groups) >= 3:
                return {
                    "test": "Kruskal-Wallis H test",
                    "func": None,
                    "params": {"y_col": y_col, "g_col": g_col},
                    "note": "三组及以上比较，使用非参数检验"
                }
        return {"test": "未确定", "func": None, "params": {}, "note": "无法检测分组"}

    elif struct == "surv":
        return {
            "test": "Log-rank test",
            "func": None,
            "params": {},
            "note": "生存分析使用 Log-rank 检验"
        }

    return {"test": "未确定", "func": None, "params": {}, "note": "未知数据结构"}


# ─────────────────────────────────────────────────────────────
# 3. 图型自动选择（基于统计方法）
# ─────────────────────────────────────────────────────────────
def select_plot_types(struct: str, stat_method: Dict, domain: str = None) -> List[str]:
    """
    根据数据结构和统计方法选择图型

    Returns:
        图型列表（按优先级排序）
    """
    candidates = []

    # R bridge 复杂图（优先）
    if struct == "diff":
        candidates.extend([
            "r_enhanced_volcano",  # 火山图（EnhancedVolcano）
            "r_complex_heatmap",   # 热图（ComplexHeatmap）
            "r_ma_plot",           # MA plot（ggplot2）
        ])
    elif struct == "grouped":
        candidates.extend([
            "r_complexheatmap",   # 分组热图
            "boxplot",            # 箱线图（Python 原生）
            "violin",             # 小提琴图
        ])
    elif struct == "wide":
        candidates.extend([
            "r_complexheatmap",   # 全量热图
            "pca",                # PCA（Python 原生）
        ])
    elif struct == "surv":
        candidates.extend([
            "km",                 # Kaplan-Meier 生存曲线
            "forest_plot",        # 森林图（Cox 回归）
        ])

    # 领域特定补充
    if domain in ("metabolomics", "proteomics", "bulkRNA"):
        if "r_enhancedvolcano" not in candidates:
            candidates.append("r_enhancedvolcano")

    return candidates


# ─────────────────────────────────────────────────────────────
# 4. 核心路由函数
# ─────────────────────────────────────────────────────────────
def auto_route_and_plot(
    df: pd.DataFrame,
    output_dir: str,
    domain: str = None,
    top_n: int = 8,
    force_r: bool = True
) -> Dict:
    """
    自动路由：检测结构 → 选统计方法 → 选图型 → 生成

    Args:
        df: 输入 DataFrame
        output_dir: 输出目录
        domain: 领域（metabolomics/proteomics/bulkRNA/microbiome）
        top_n: 最多生成几张图
        force_r: 是否强制使用 R bridge（True=优先 R）

    Returns:
        {
            "structure": str,
            "stat_method": Dict,
            "plot_types": List[str],
            "generated": List[str],
            "summary": Dict
        }
    """
    import sys
    sys.path.insert(0, '/e/git/sci-figure-master/assets')
    from r_bridge import plot_r, RBridge
    from bioinfo_router import generate_figure

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Step 1: 检测结构
    struct = detect_structure(df)
    print(f"[1/4] 数据结构: {struct}")

    # Step 2: 选择统计方法
    stat_method = select_stat_method(struct, df)
    print(f"[2/4] 统计方法: {stat_method['test']} - {stat_method['note']}")

    # Step 3: 选择图型
    plot_types = select_plot_types(struct, stat_method, domain)
    print(f"[3/4] 图型候选: {plot_types[:top_n]}")

    # Step 4: 生成
    generated = []
    for pt in plot_types[:top_n]:
        out_file = out_path / f"fig_{pt}.pdf" if force_r or pt.startswith("r_") else out_path / f"fig_{pt}.svg"
        try:
            if force_r and pt.startswith("r_"):
                # R bridge
                if not RBridge.is_available():
                    print(f"  ✗ R 不可用，跳过 {pt}")
                    continue
                # 适配数据格式（去掉 r_ 前缀，保持下划线）
                r_type = pt[2:]  # "r_enhanced_volcano" -> "enhanced_volcano"
                if r_type in ("enhanced_volcano", "ma_plot"):
                    r_data = df.to_dict("records")
                elif r_type == "complex_heatmap":
                    # ComplexHeatmap 需要数值矩阵
                    r_data = df.select_dtypes(include=[np.number]).values.tolist()
                else:
                    r_data = None
                # 修复 Windows 路径转义问题：用正斜杠
                r_out = str(out_file).replace("\\", "/")
                res = plot_r(r_type, r_data, r_out)
                if res.get("status") == "success" and out_file.exists():
                    generated.append(str(out_file))
                    print(f"  ✓ {pt} -> {out_file.name} ({out_file.stat().st_size/1024:.1f}KB)")
                else:
                    print(f"  ✗ {pt} failed: {res.get('error', '')[:50]}")
            else:
                # Python 原生
                res = generate_figure(domain or "general", pt, df, str(out_file))
                if res and Path(res).exists():
                    generated.append(res)
                    print(f"  ✓ {pt} -> {Path(res).name} ({Path(res).stat().st_size/1024:.1f}KB)")
                else:
                    print(f"  ✗ {pt} failed")
        except Exception as e:
            print(f"  ✗ {pt} error: {e}")

    return {
        "structure": struct,
        "stat_method": stat_method,
        "plot_types": plot_types[:top_n],
        "generated": generated,
        "summary": {
            "n_figures": len(generated),
            "n_candidates": len(plot_types),
            "output_dir": str(out_path)
        }
    }


# ─────────────────────────────────────────────────────────────
# 5. 批量生成（多组学层）
# ─────────────────────────────────────────────────────────────
def batch_plot_by_layer(
    full_df: pd.DataFrame,
    layer_col: str,
    output_base: str,
    domain: str = None,
    **kwargs
) -> Dict:
    """
    按层批量生成：对每个 layer 子集单独出图

    Args:
        full_df: 包含 layer 列的完整 DataFrame
        layer_col: 层标识列名（如 'layer'）
        output_base: 输出基础目录（每个层一个子目录）
        domain: 领域
        **kwargs: 透传给 auto_route_and_plot
    """
    layers = full_df[layer_col].unique()
    results = {}
    for layer in layers:
        sub = full_df[full_df[layer_col] == layer]
        out_dir = Path(output_base) / str(layer)
        print(f"\n{'='*60}")
        print(f"Layer: {layer} (n={len(sub)})")
        print(f"{'='*60}")
        results[layer] = auto_route_and_plot(sub, str(out_dir), domain=domain, **kwargs)
    return results


# ─────────────────────────────────────────────────────────────
# 6. 测试入口
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/e/git/sci-figure-master/assets')

    # 测试：XNP 代谢组 Fecal 层
    df = pd.read_csv('D:/乌灵菌/机制轴/tables/T01_metabolome_DE_full.csv')
    fecal = df[df['layer']=='Fecal'][['feature_id','log2FC','FDR','AveExpr']]

    print("="*60)
    print("TEST: XNP Fecal Metabolome")
    print("="*60)
    res = auto_route_and_plot(fecal, 'E:/XNP论文初稿/05_图件/_auto_test', domain='metabolomics', top_n=6)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Structure: {res['structure']}")
    print(f"Stat method: {res['stat_method']['test']}")
    print(f"Generated: {len(res['generated'])} figures")
    for g in res['generated']:
        print(f"  - {Path(g).name}")
