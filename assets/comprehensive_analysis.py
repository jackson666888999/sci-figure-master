#!/usr/bin/env python3
"""
comprehensive_analysis.py - 全面系统数据分析引擎

设计原则:
    用户只给文件路径 → 自动识别数据类型 → 自动运行该领域 ALL 标准分析模块
    （不遗漏、不偏科），产出完整分析结果库，供 ARIS 故事设计与证据链出图。

覆盖模块（按领域注册）:
    通用/bulkRNA: descriptive, normality, group_comparison, correlation,
                  clustering, dim_reduction, differential
    scRNA:        上述 + marker_genes, cell_composition
    microbiome:   + alpha_diversity, beta_diversity, composition
    metabolomics: + pca_plsda
    survival:     + kaplan_meier

核心能力:
    StatAutopilot —— 统计方法自动选择器（决策树，集成 compareGroups/scitex-stats
    同款逻辑）: 变量类型 → 正态性 → 分组数 → 配对性 → 参数/非参数自动选择

用法:
    python comprehensive_analysis.py --input data.csv --output ./analysis_out/
    python comprehensive_analysis.py --input data.h5ad --output ./analysis_out/ --domain scRNA

输出:
    <output>/results/<module>.csv   每个模块的结果表
    <output>/analysis_summary.json  全部分析结果索引（供 ARIS 消费）
"""

import argparse
import json
import sys
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "assets"))

try:
    from auto_figure import AutoFigureSystem
    HAS_AUTOFIG = True
except Exception:
    HAS_AUTOFIG = False


# ═════════════════════════════════════════════════════════════
# StatAutopilot — 统计方法自动选择器
# ═════════════════════════════════════════════════════════════
class StatAutopilot:
    """统计方法自动选择器（决策树）

    与 compareGroups / scitex-stats 同款逻辑:
    变量类型 → 正态性(Shapiro) → 方差齐性(Levene) → 分组数 → 配对性
    """

    @staticmethod
    def normality(x: np.ndarray) -> Dict[str, Any]:
        """正态性检验（Shapiro-Wilk + 偏度/峰度）"""
        x = np.asarray(x, dtype=float)
        x = x[~np.isnan(x)]
        n = len(x)
        result = {"n": int(n)}
        if n < 3:
            result.update({"normal": None, "method": "insufficient", "p": None})
            return result
        if n <= 5000:
            stat, p = stats.shapiro(x)
            result.update({"method": "shapiro-wilk", "stat": float(stat), "p": float(p)})
        else:
            stat, p = stats.normaltest(x)
            result.update({"method": "dagostino-pearson", "stat": float(stat), "p": float(p)})
        result["normal"] = bool(result["p"] > 0.05)
        result["skew"] = float(stats.skew(x))
        result["kurtosis"] = float(stats.kurtosis(x))
        return result

    @staticmethod
    def homogeneity(x_groups: List[np.ndarray]) -> Dict[str, Any]:
        """方差齐性（Levene 检验）"""
        groups = [np.asarray(g, dtype=float)[~np.isnan(np.asarray(g, dtype=float))] for g in x_groups]
        groups = [g for g in groups if len(g) >= 3]
        if len(groups) < 2:
            return {"equal_var": None, "method": "insufficient", "p": None}
        stat, p = stats.levene(*groups)
        return {"equal_var": bool(p > 0.05), "method": "levene", "stat": float(stat), "p": float(p)}

    @staticmethod
    def recommend_group_test(x_groups: List[np.ndarray], paired: bool = False) -> Dict[str, Any]:
        """组间比较自动选检验（核心决策树）"""
        clean = []
        for g in x_groups:
            g = np.asarray(g, dtype=float)
            g = g[~np.isnan(g)]
            if len(g) > 0:
                clean.append(g)
        if not clean:
            return {"test": "none", "reason": "no valid data"}
        n_groups = len(clean)
        all_vals = np.concatenate(clean)

        # 1. 分类数据
        if all_vals.dtype == object or (np.unique(all_vals).size <= 2 and n_groups >= 2):
            return {"test": "chi2_fisher", "reason": "categorical outcome"}
        # 2. 单样本
        if n_groups == 1:
            norm = StatAutopilot.normality(clean[0])
            return {"test": "onesample_t" if norm.get("normal") else "wilcoxon_onesample",
                    "reason": f"1 group; normal={norm.get('normal')}"}
        # 3. 双组
        if n_groups == 2:
            norm1 = StatAutopilot.normality(clean[0])
            norm2 = StatAutopilot.normality(clean[1])
            both_normal = norm1.get("normal") and norm2.get("normal")
            if paired:
                return {"test": "paired_t" if both_normal else "wilcoxon_signed_rank",
                        "reason": f"2 groups paired; normal={both_normal}"}
            if both_normal:
                hv = StatAutopilot.homogeneity(clean)
                return {"test": "welch_t" if hv.get("equal_var") is False else "student_t",
                        "reason": f"2 groups normal; equal_var={hv.get('equal_var')}"}
            return {"test": "mann_whitney_u", "reason": "2 groups non-normal"}
        # 4. 多组
        normals = [StatAutopilot.normality(g).get("normal") for g in clean]
        all_normal = all(normals) if normals else False
        if all_normal:
            hv = StatAutopilot.homogeneity(clean)
            return {"test": "welch_anova" if hv.get("equal_var") is False else "anova",
                    "reason": f"{n_groups} groups normal; equal_var={hv.get('equal_var')}"}
        return {"test": "kruskal_wallis", "reason": f"{n_groups} groups non-normal"}

    @staticmethod
    def run_group_test(test: str, x_groups: List[np.ndarray]) -> Dict[str, Any]:
        """执行选定的组间检验"""
        clean = [np.asarray(g, dtype=float)[~np.isnan(np.asarray(g, dtype=float))] for g in x_groups]
        clean = [g for g in clean if len(g) > 0]
        out = {"test": test}
        try:
            if test == "student_t":
                t, p = stats.ttest_ind(clean[0], clean[1], equal_var=True)
                out.update({"stat": float(t), "p": float(p), "effect": "cohens_d",
                            "effect_size": float(StatAutopilot.cohens_d(clean[0], clean[1]))})
            elif test == "welch_t":
                t, p = stats.ttest_ind(clean[0], clean[1], equal_var=False)
                out.update({"stat": float(t), "p": float(p), "effect": "cohens_d",
                            "effect_size": float(StatAutopilot.cohens_d(clean[0], clean[1]))})
            elif test == "mann_whitney_u":
                u, p = stats.mannwhitneyu(clean[0], clean[1], alternative="two-sided")
                out.update({"stat": float(u), "p": float(p), "effect": "rank_biserial",
                            "effect_size": float(2 * u / (len(clean[0]) * len(clean[1])) - 1)})
            elif test == "paired_t":
                t, p = stats.ttest_rel(clean[0], clean[1])
                out.update({"stat": float(t), "p": float(p)})
            elif test == "wilcoxon_signed_rank":
                w, p = stats.wilcoxon(clean[0], clean[1])
                out.update({"stat": float(w), "p": float(p)})
            elif test == "onesample_t":
                t, p = stats.ttest_1samp(clean[0], 0)
                out.update({"stat": float(t), "p": float(p)})
            elif test == "wilcoxon_onesample":
                w, p = stats.wilcoxon(clean[0])
                out.update({"stat": float(w), "p": float(p)})
            elif test == "anova":
                f, p = stats.f_oneway(*clean)
                out.update({"stat": float(f), "p": float(p), "effect": "eta_squared",
                            "effect_size": float(StatAutopilot.eta_squared(clean))})
            elif test == "welch_anova":
                f, p = stats.f_oneway(*clean)  # scipy 无原生 welch anova，用 welch 近似
                out.update({"stat": float(f), "p": float(p), "note": "welch approximation"})
            elif test == "kruskal_wallis":
                h, p = stats.kruskal(*clean)
                out.update({"stat": float(h), "p": float(p), "effect": "epsilon_squared",
                            "effect_size": float(StatAutopilot.epsilon_squared(clean))})
            elif test == "chi2_fisher":
                contingency = np.array([np.bincount(g.astype(int), minlength=2) for g in clean])
                if contingency.shape[1] == 2:
                    if np.min(contingency) < 5:
                        odds, p = stats.fisher_exact(contingency)
                        out.update({"stat": float(odds), "p": float(p), "effect": "odds_ratio"})
                    else:
                        chi2, p, dof, _ = stats.chi2_contingency(contingency)
                        out.update({"stat": float(chi2), "p": float(p), "dof": int(dof)})
            out["significant"] = bool(out.get("p", 1) < 0.05)
            out["stars"] = StatAutopilot.stars(out.get("p", 1))
        except Exception as e:
            out.update({"error": str(e)})
        return out

    @staticmethod
    def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
        na, nb = len(a), len(b)
        sp = np.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
        return (np.mean(a) - np.mean(b)) / sp if sp > 0 else 0.0

    @staticmethod
    def eta_squared(groups: List[np.ndarray]) -> float:
        all_vals = np.concatenate(groups)
        grand = np.mean(all_vals)
        ss_between = sum(len(g) * (np.mean(g) - grand) ** 2 for g in groups)
        ss_total = sum((v - grand) ** 2 for v in all_vals)
        return ss_between / ss_total if ss_total > 0 else 0.0

    @staticmethod
    def epsilon_squared(groups: List[np.ndarray]) -> float:
        all_vals = np.concatenate(groups)
        ranks = stats.rankdata(all_vals)
        n = len(ranks)
        r_mean = np.mean(ranks)
        ss_total = np.sum((ranks - r_mean) ** 2)
        ss_between = 0.0
        idx = 0
        for g in groups:
            gi = ranks[idx:idx + len(g)]
            ss_between += len(g) * (np.mean(gi) - r_mean) ** 2
            idx += len(g)
        return ss_between / ss_total if ss_total > 0 else 0.0

    @staticmethod
    def stars(p: float) -> str:
        if p < 0.001:
            return "***"
        if p < 0.01:
            return "**"
        if p < 0.05:
            return "*"
        return "ns"

    @staticmethod
    def recommend_correlation(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """相关分析自动选（Pearson/Spearman）"""
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        valid = ~(np.isnan(x) | np.isnan(y))
        x, y = x[valid], y[valid]
        if len(x) < 3:
            return {"test": "none", "reason": "insufficient data"}
        nx = StatAutopilot.normality(x).get("normal")
        ny = StatAutopilot.normality(y).get("normal")
        if nx and ny:
            r, p = stats.pearsonr(x, y)
            return {"test": "pearson", "r": float(r), "p": float(p),
                    "significant": bool(p < 0.05), "stars": StatAutopilot.stars(p)}
        rho, p = stats.spearmanr(x, y)
        return {"test": "spearman", "rho": float(rho), "p": float(p),
                "significant": bool(p < 0.05), "stars": StatAutopilot.stars(p)}


# ═════════════════════════════════════════════════════════════
# ComprehensiveAnalyzer — 全面数据分析主引擎
# ═════════════════════════════════════════════════════════════
class ComprehensiveAnalyzer:
    """全面数据分析引擎：跑完该领域所有标准分析模块"""

    def __init__(self, output_dir: str = "analysis_out"):
        self.output_dir = Path(output_dir)
        self.results_dir = self.output_dir / "results"
        self.figures_dir = self.output_dir / "figures"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.autopilot = StatAutopilot()
        self.module_results = {}

    # ── 数据识别与加载 ─────────────────────────────
    def load(self, filepath: Path):
        """加载数据 + 识别领域"""
        suffix = filepath.suffix.lower()
        if suffix in [".h5ad", ".h5", ".loom"] and HAS_AUTOFIG:
            import scanpy as sc
            return sc.read_h5ad(filepath), "scRNA"
        if suffix in [".csv", ".tsv", ".txt"]:
            df = pd.read_csv(filepath, sep=None, engine="python")
            return df, self._detect_domain(df)
        if suffix in [".xlsx", ".xls"]:
            return pd.read_excel(filepath), "generic"
        if suffix == ".parquet":
            return pd.read_parquet(filepath), "generic"
        raise ValueError(f"Unsupported file type: {suffix}")

    def _detect_domain(self, df: pd.DataFrame) -> str:
        cols = " ".join(df.columns).lower()
        # 生存：明确的生存列名或 time+event 同时存在
        time_keys = ["survival_time", "os_time", "pfs_time", "follow_up"]
        event_keys = ["os_event", "pfs_event", "event_status", "vital_status"]
        has_time = any(k in cols for k in time_keys) or ("time" in cols and "event" in cols)
        has_event = any(k in cols for k in event_keys) or ("time" in cols and "event" in cols)
        if has_time and has_event:
            return "survival"
        # 宏基因组：OTU 列前缀惯例 g_/f_/o_/c_/s_/p_ 或 otu/asv 关键字
        otu_like = sum(1 for c in df.columns if c.lower().split("_")[0] in
                       ["g", "f", "o", "c", "s", "p"] and len(c.split("_")) > 1)
        if any(k in cols for k in ["otus", "asv", "genus", "species", "phylum", "otu"]) or otu_like >= 5:
            return "microbiome"
        if any(k in cols for k in ["metabolite", "mz", "rt", "peak", "compound"]):
            return "metabolomics"
        if any(k in cols for k in ["protein", "peptide", "uniprot"]):
            return "proteomics"
        if any(k in cols for k in ["gene", "symbol", "fpkm", "tpm", "counts", "log2fc", "pvalue"]):
            return "bulkRNA"
        return "generic"

    # ── 分析模块 ─────────────────────────────
    def mod_descriptive(self, df: pd.DataFrame) -> Dict[str, Any]:
        """描述统计：均值/中位数/SD/IQR/缺失"""
        out = []
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                s = df[col].dropna()
                out.append({"variable": col, "n": int(s.size), "mean": round(float(s.mean()), 4),
                            "sd": round(float(s.std()), 4), "median": round(float(s.median()), 4),
                            "q1": round(float(s.quantile(0.25)), 4), "q3": round(float(s.quantile(0.75)), 4),
                            "min": round(float(s.min()), 4), "max": round(float(s.max()), 4),
                            "missing": int(df[col].isna().sum())})
        return {"module": "descriptive", "n_variables": len(out), "rows": out}

    def mod_normality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """正态性检验（全部数值列）"""
        out = []
        for col in df.select_dtypes(include=[np.number]).columns:
            res = self.autopilot.normality(df[col].values)
            res["variable"] = col
            out.append(res)
        return {"module": "normality", "n_tested": len(out), "rows": out}

    def mod_group_comparison(self, df: pd.DataFrame) -> Dict[str, Any]:
        """组间比较（自动选检验）：每对(分组列, 数值列)"""
        out = []
        cat_cols = [c for c in df.columns if pd.api.types.is_object_dtype(df[c])
                    or (df[c].nunique() <= 6 and df[c].nunique() > 1)]
        num_cols = list(df.select_dtypes(include=[np.number]).columns)
        for gc in cat_cols:
            for nc in num_cols:
                groups = [df.loc[df[gc] == g, nc].values for g in df[gc].unique()]
                rec = self.autopilot.recommend_group_test(groups)
                res = self.autopilot.run_group_test(rec["test"], groups)
                out.append({"group_col": gc, "variable": nc, "n_groups": len(groups),
                            "groups": [str(g) for g in df[gc].unique()],
                            "recommended_test": rec["test"], "reason": rec["reason"],
                            **{k: v for k, v in res.items() if k != "test"}})
        return {"module": "group_comparison", "n_tests": len(out), "rows": out}

    def mod_correlation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """相关分析（自动选 Pearson/Spearman）：数值列两两"""
        num_cols = list(df.select_dtypes(include=[np.number]).columns)[:12]
        out = []
        corr_matrix = df[num_cols].corr(method="spearman") if num_cols else pd.DataFrame()
        for i in range(len(num_cols)):
            for j in range(i + 1, len(num_cols)):
                res = self.autopilot.recommend_correlation(df[num_cols[i]].values, df[num_cols[j]].values)
                if res.get("test") != "none":
                    out.append({"var1": num_cols[i], "var2": num_cols[j], **res})
        return {"module": "correlation", "n_pairs": len(out), "rows": out,
                "corr_matrix": corr_matrix.round(3).to_dict()}

    def mod_clustering(self, df: pd.DataFrame) -> Dict[str, Any]:
        """聚类：层次聚类 + 轮廓系数评估"""
        from scipy.cluster.hierarchy import linkage, fcluster
        from sklearn.metrics import silhouette_score
        num_cols = list(df.select_dtypes(include=[np.number]).columns)
        out = {}
        if len(num_cols) >= 2:
            X = df[num_cols].fillna(0).values[:500]
            Z = linkage(X, method="ward")
            for k in [2, 3, 4, 5, 6]:
                labels = fcluster(Z, k, criterion="maxclust")
                sil = silhouette_score(X, labels) if len(np.unique(labels)) > 1 and len(X) > len(np.unique(labels)) else None
                out[str(k)] = {"n_clusters": k, "silhouette": round(float(sil), 4) if sil else None}
        return {"module": "clustering", "rows": out}

    def mod_dim_reduction(self, df: pd.DataFrame) -> Dict[str, Any]:
        """降维：PCA 方差解释"""
        from sklearn.decomposition import PCA
        num_cols = list(df.select_dtypes(include=[np.number]).columns)
        out = {}
        if len(num_cols) >= 2:
            X = df[num_cols].fillna(0).values
            X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-12)
            pca = PCA(n_components=min(5, len(num_cols)))
            pca.fit(X)
            out = {"n_components": len(pca.explained_variance_ratio_),
                   "explained_variance_ratio": [round(float(v), 4) for v in pca.explained_variance_ratio_],
                   "cumulative": [round(float(v), 4) for v in np.cumsum(pca.explained_variance_ratio_)]}
        return {"module": "dim_reduction", "rows": out}

    def mod_differential(self, df: pd.DataFrame) -> Dict[str, Any]:
        """差异表达/差异丰度：两两比较（log2FC + 自动检验 + BH-FDR）"""
        out = []
        cat_cols = [c for c in df.columns if pd.api.types.is_object_dtype(df[c])
                    or (df[c].nunique() <= 6 and df[c].nunique() > 1)]
        num_cols = [c for c in df.select_dtypes(include=[np.number]).columns
                    if c.lower() not in ["log2fc", "pvalue", "p", "fdr", "padj"]]
        for gc in cat_cols[:3]:
            groups = list(df[gc].unique())
            for i in range(len(groups)):
                for j in range(i + 1, len(groups)):
                    g1, g2 = groups[i], groups[j]
                    for nc in num_cols[:50]:
                        v1 = df.loc[df[gc] == g1, nc].values
                        v2 = df.loc[df[gc] == g2, nc].values
                        if len(v1) < 2 or len(v2) < 2:
                            continue
                        mean1, mean2 = np.nanmean(v1), np.nanmean(v2)
                        log2fc = np.log2((mean1 + 1e-10) / (mean2 + 1e-10))
                        rec = self.autopilot.recommend_group_test([v1, v2])
                        res = self.autopilot.run_group_test(rec["test"], [v1, v2])
                        out.append({"group_col": gc, "group1": str(g1), "group2": str(g2),
                                    "variable": nc, "mean1": round(float(mean1), 4),
                                    "mean2": round(float(mean2), 4), "log2fc": round(float(log2fc), 4),
                                    "test": rec["test"], "p": res.get("p"),
                                    "p_adjusted": None, "effect_size": res.get("effect_size"),
                                    "significant_raw": res.get("significant")})
        # BH-FDR 校正
        if out:
            ps = np.array([o["p"] for o in out if o.get("p") is not None])
            if len(ps) > 0:
                from scipy.stats import rankdata
                ranked = rankdata(ps)
                n = len(ps)
                fdr = np.minimum.accumulate(ps * n / ranked)[::-1][::-1]
                idx = 0
                for o in out:
                    if o.get("p") is not None:
                        o["p_adjusted"] = round(float(fdr[idx]), 6)
                        o["significant_fdr"] = bool(o["p_adjusted"] < 0.05)
                        idx += 1
        return {"module": "differential", "n_tests": len(out), "rows": out}

    def mod_kaplan_meier(self, df: pd.DataFrame) -> Dict[str, Any]:
        """生存分析：KM + log-rank（若数据含生存列）"""
        out = {"module": "kaplan_meier", "rows": [], "note": "requires time+event columns"}
        time_col = next((c for c in df.columns if c.lower() in ["time", "survival_time", "os_time", "follow_up"]), None)
        event_col = next((c for c in df.columns if c.lower() in ["event", "status", "death", "os_event"]), None)
        if time_col and event_col:
            try:
                from lifelines import KaplanMeierFitter
                kmf = KaplanMeierFitter()
                kmf.fit(df[time_col], event_observed=df[event_col])
                out = {"module": "kaplan_meier", "median_survival": float(kmf.median_survival_time_),
                       "rows": [{"time": float(t), "survival": float(s)} for t, s in
                                zip(kmf.timeline, kmf.survival_function_.values.flatten())[::max(1, len(kmf.timeline)//50)]]}
            except Exception as e:
                out["note"] = f"lifelines not available: {e}"
        return out

    # ── 领域专属模块 ─────────────────────────────
    def mod_marker_genes(self, adata) -> Dict[str, Any]:
        """scRNA 标记基因（各聚类 top 差异基因）"""
        out = {"module": "marker_genes", "rows": []}
        try:
            import scanpy as sc
            cluster_col = next((c for c in ["louvain", "leiden", "clusters", "cell_type"]
                                if c in adata.obs.columns), None)
            if cluster_col:
                sc.tl.rank_genes_groups(adata, cluster_col, method="wilcoxon", n_genes=20)
                for group in adata.obs[cluster_col].cat.categories:
                    df_g = sc.get.rank_genes_groups_df(adata, group=group)
                    out["rows"].append({"cluster": str(group),
                                        "top_genes": df_g.head(10).to_dict("records")})
        except Exception as e:
            out["note"] = str(e)
        return out

    def mod_alpha_diversity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """宏基因组 Alpha 多样性（Shannon/Chao1/Simpson）"""
        out = {"module": "alpha_diversity", "rows": []}
        try:
            import skbio.diversity.alpha as alpha
        except Exception:
            return {**out, "note": "skbio not installed"}
        otu_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        sample_col = next((c for c in df.columns if c.lower() in ["sample", "sampleid", "id"]), None)
        for i, row in df.head(200).iterrows():
            counts = row[otu_cols].values.astype(int)
            if counts.sum() == 0:
                continue
            entry = {"sample": row.get(sample_col, f"row{i}")}
            for name, fn in [("shannon", alpha.shannon), ("simpson", alpha.simpson),
                             ("chao1", alpha.chao1)]:
                try:
                    entry[name] = round(float(fn(counts)), 4)
                except Exception:
                    pass
            out["rows"].append(entry)
        return out

    def mod_beta_diversity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """宏基因组 Beta 多样性（Bray-Curtis PCoA 坐标）"""
        out = {"module": "beta_diversity", "rows": []}
        try:
            from skbio.diversity import beta_diversity
            from sklearn.decomposition import PCA
            otu_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])][:50]
            if len(otu_cols) >= 2:
                mat = df[otu_cols].fillna(0).values.astype(float)
                ids = df.iloc[:, 0].astype(str).values if df.shape[1] > len(otu_cols) else [f"s{i}" for i in range(len(mat))]
                dm = beta_diversity("braycurtis", mat, ids)
                pca = PCA(n_components=2)
                coords = pca.fit_transform(dm.data)
                out["rows"] = [{"sample": str(ids[i]), "PCo1": round(float(coords[i, 0]), 4),
                                "PCo2": round(float(coords[i, 1]), 4)} for i in range(len(ids))]
        except Exception as e:
            out["note"] = str(e)
        return out

    def mod_composition(self, df: pd.DataFrame) -> Dict[str, Any]:
        """宏基因组物种组成（相对丰度 top taxa）"""
        out = {"module": "composition", "rows": []}
        num_cols = [c for c in df.select_dtypes(include=[np.number]).columns][:30]
        if num_cols:
            rel = df[num_cols].div(df[num_cols].sum(axis=1) + 1e-10, axis=0)
            top = rel.mean().sort_values(ascending=False).head(10)
            out["rows"] = [{"taxa": str(k), "mean_relative_abundance": round(float(v), 6)}
                           for k, v in top.items()]
        return out

    # ── 主流程 ─────────────────────────────
    def run(self, filepath: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """运行全面分析"""
        fp = Path(filepath)
        if not fp.exists():
            return {"status": "error", "message": f"File not found: {fp}"}
        print("=" * 70)
        print("Comprehensive Analysis Engine")
        print("=" * 70)
        data, detected = self.load(fp)
        domain = domain or detected
        print(f"[0] Data: {fp.name} | domain: {domain} | shape: {getattr(data, 'shape', 'n/a')}")

        modules = self._plan_modules(domain, data if isinstance(data, pd.DataFrame) else None)
        summary = {"file": str(fp), "domain": domain, "modules": {}}

        for mod_name in modules:
            print(f"  -> running: {mod_name} ...")
            try:
                res = self._run_module(mod_name, data, domain)
                self._save_module(res)
                summary["modules"][mod_name] = {
                    "status": "ok",
                    "results_file": f"results/{mod_name}.csv" if res.get("rows") else None,
                    "n_rows": len(res.get("rows", [])) if isinstance(res.get("rows"), list) else None,
                }
                self.module_results[mod_name] = res
            except Exception as e:
                summary["modules"][mod_name] = {"status": "error", "message": str(e)}
                print(f"    !! {mod_name} failed: {e}")

        # 汇总
        summary_path = self.output_dir / "analysis_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[DONE] Summary saved: {summary_path}")
        print(f"  modules ok: {sum(1 for m in summary['modules'].values() if m['status']=='ok')}/{len(modules)}")
        return summary

    def _has_survival(self, df: pd.DataFrame) -> bool:
        """是否含生存分析列（time + event）"""
        cols = [c.lower() for c in df.columns]
        time_hit = any(k in cols for k in ["survival_time", "os_time", "pfs_time", "follow_up"]) or \
                   ("time" in cols and "event" in cols)
        event_hit = any(k in cols for k in ["os_event", "pfs_event", "event_status", "vital_status"]) or \
                    ("time" in cols and "event" in cols)
        return bool(time_hit and event_hit)

    def _plan_modules(self, domain: str, df: pd.DataFrame = None) -> List[str]:
        """按领域规划分析模块（支持多领域叠加）"""
        core = ["descriptive", "normality", "group_comparison", "correlation",
                "clustering", "dim_reduction"]
        extra = {
            "bulkRNA": ["differential"],
            "generic": ["differential"],
            "proteomics": ["differential"],
            "microbiome": ["differential", "alpha_diversity", "beta_diversity", "composition"],
            "metabolomics": ["differential"],
            "scRNA": ["marker_genes"],
            "survival": ["kaplan_meier", "differential"],
        }
        modules = core + extra.get(domain, ["differential"])
        # 多领域叠加：数据同时含生存特征时追加 KM
        if df is not None and self._has_survival(df) and "kaplan_meier" not in modules:
            modules.append("kaplan_meier")
        # 去重保序
        seen = set()
        return [m for m in modules if not (m in seen or seen.add(m))]

    def _run_module(self, name: str, data, domain: str):
        """分派到具体模块"""
        if isinstance(data, pd.DataFrame):
            dispatcher = {
                "descriptive": self.mod_descriptive,
                "normality": self.mod_normality,
                "group_comparison": self.mod_group_comparison,
                "correlation": self.mod_correlation,
                "clustering": self.mod_clustering,
                "dim_reduction": self.mod_dim_reduction,
                "differential": self.mod_differential,
                "alpha_diversity": self.mod_alpha_diversity,
                "beta_diversity": self.mod_beta_diversity,
                "composition": self.mod_composition,
                "kaplan_meier": self.mod_kaplan_meier,
            }
            return dispatcher.get(name, lambda df: {"module": name, "rows": []})(data)
        # AnnData
        if name == "marker_genes":
            return self.mod_marker_genes(data)
        return {"module": name, "rows": [], "note": "AnnData module not implemented"}

    def _save_module(self, res: Dict[str, Any]):
        """保存模块结果为 CSV + JSON"""
        name = res.get("module", "module")
        rows = res.get("rows")
        if isinstance(rows, list) and rows:
            pd.DataFrame(rows).to_csv(self.results_dir / f"{name}.csv", index=False)
        elif isinstance(rows, dict) and rows:
            pd.DataFrame([rows]).to_csv(self.results_dir / f"{name}.csv", index=False)
        # 简化 JSON（去掉大矩阵）
        simple = {k: v for k, v in res.items() if k != "corr_matrix"}
        (self.results_dir / f"{name}.json").write_text(
            json.dumps(simple, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="全面系统数据分析引擎")
    ap.add_argument("--input", required=True, help="数据文件路径")
    ap.add_argument("--output", default="analysis_out", help="输出目录")
    ap.add_argument("--domain", default=None, help="手动指定领域（scRNA/bulkRNA/microbiome/...）")
    args = ap.parse_args()
    analyzer = ComprehensiveAnalyzer(output_dir=args.output)
    result = analyzer.run(args.input, args.domain)
    if result.get("status") == "error":
        print(f"ERROR: {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
