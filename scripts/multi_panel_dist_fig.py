# -*- coding: utf-8 -*-
"""
XNP 多组学论文 — 原始分布图（Fig_S1–S4）：从真实原始矩阵出图
  Fig_S1_Microbiome : 16S 原始分布（α/β 多样性 + 分类单元丰度）
  Fig_S2_scRNA      : 单细胞 UMAP 分面（group / leiden / 比例 / QC）
  Fig_S3_Metabolome : 代谢组 PCA（Fecal/Serum/Brain）
  Fig_S4_Proteome   : 蛋白组 PCA（Brain/Serum）

Nature/Science 标准：英文标签、DejaVu Sans、bottom/left spines、高对比三组配色、
无黑色图例背景、SVG+PDF+PNG300+Tiff600 四格式。
数据红线：仅读真实文件，绝不在 D:/乌灵菌 测序目录写任何东西；产物仅落 E:。
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any, Tuple

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.titlesize": 9,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
})

C_CTRL  = "#2E75B6"
C_MODEL = "#C0392B"
C_XNP   = "#27AE60"
GROUP_ORDER = ["Control", "Model", "XNP"]
GROUP_COL = {"Control": C_CTRL, "Model": C_MODEL, "XNP": C_XNP}

RAW_16S_DIR = Path("D:/乌灵菌/XNP多组学/16S_figure_archive_20260711")
REL_ABUND   = RAW_16S_DIR / "Fig02_16S_microbiota_structure/data_processed/relative_abundance.csv"
TAX_PARSED  = RAW_16S_DIR / "Fig02_16S_microbiota_structure/data_processed/taxonomy_parsed.csv"
BETA_SRC    = RAW_16S_DIR / "16S_figure_archive/main/Fig04_Alpha_Beta_Diversity/plot_source_data_beta.csv"
H5AD        = Path("D:/乌灵菌/cellvoyager_data/XNP_scRNA.h5ad")
DIST_DATA   = Path("E:/XNP论文初稿/05_图件/_dist_data")
OUT_DIR     = Path("E:/XNP论文初稿/05_图件")


def _save_multi(base: Path, fig: plt.Figure):
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), bbox_inches="tight", dpi=300)
    fig.savefig(base.with_suffix(".tiff"), bbox_inches="tight", dpi=600)
    plt.close(fig)


def _grid(nrows=2, ncols=4, figsize=(16, 8)):
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    return fig, axes.flatten()


def _sample_group(col: str) -> str:
    if col.startswith("Control"): return "Control"
    if col.startswith("Model"):   return "Model"
    if col.startswith("High"):    return "XNP"
    return "Other"


def _kw_p(groups: List[np.ndarray]) -> float:
    from scipy.stats import kruskal
    groups = [g[~np.isnan(g)] for g in groups]
    if len(groups) < 2 or any(len(g) < 2 for g in groups):
        return np.nan
    try:
        return float(kruskal(*groups).pvalue)
    except Exception:
        return np.nan


def _pca(X: np.ndarray, n: int = 2) -> Tuple[np.ndarray, np.ndarray]:
    Xc = X - X.mean(axis=0)
    sd = Xc.std(axis=0, ddof=0)
    sd[sd == 0] = 1.0
    Xs = Xc / sd
    U, S, _ = np.linalg.svd(Xs, full_matrices=False)
    scores = U * S
    ev = (S ** 2); ev = ev / ev.sum()
    return scores[:, :n], ev[:n]


def _top_var_idx(M: np.ndarray, n: int) -> np.ndarray:
    v = M.var(axis=1)
    return np.argsort(v)[::-1][:n]


def fig_s1_microbiome(base: Path) -> Dict:
    ra = pd.read_csv(REL_ABUND, index_col=0)
    tax = pd.read_csv(TAX_PARSED).set_index("asv")
    beta = pd.read_csv(BETA_SRC)
    asv2phylum = tax["Phylum"].to_dict()

    samples = list(ra.columns)
    groups = [_sample_group(s) for s in samples]
    gpos = [i for i, g in enumerate(groups) if g in GROUP_ORDER]
    M = ra.iloc[:, gpos].to_numpy(float)
    gs = [groups[i] for i in gpos]

    p = M / M.sum(axis=0, keepdims=True)
    shannon = -np.nansum(p * np.log(p + 1e-12), axis=0)
    observed = np.sum(M > 0, axis=0).astype(float)
    simpson = 1 - np.nansum(p ** 2, axis=0)

    fig, ax = _grid()
    for k, (key, vals) in enumerate([("Shannon", shannon), ("Observed ASVs", observed), ("Simpson", simpson)]):
        data = {g: vals[[i for i, x in enumerate(gs) if x == g]] for g in GROUP_ORDER}
        ax[k].boxplot([data[g] for g in GROUP_ORDER], tick_labels=GROUP_ORDER,
                      patch_artist=True, widths=0.6,
                      boxprops=dict(facecolor="#dddddd", edgecolor="black"),
                      medianprops=dict(color="black"))
        for j, g in enumerate(GROUP_ORDER):
            xs = np.random.RandomState(0).normal(j + 1, 0.05, len(data[g]))
            ax[k].scatter(xs, data[g], s=12, color=GROUP_COL[g], zorder=3, alpha=0.8)
        pval = _kw_p([np.array(data[g]) for g in GROUP_ORDER])
        ax[k].set_title(f"{key} diversity", fontsize=9)
        ax[k].text(0.02, 0.95, f"KW p={pval:.3g}", transform=ax[k].transAxes, fontsize=6, va="top")
        ax[k].tick_params(axis="x", rotation=20)

    for ki, (metric, ai) in enumerate([("Bray-Curtis", 3), ("Jaccard", 4)]):
        sub = beta[beta["distance_metric"] == metric].copy()
        sub["g"] = sub["group_f"].replace({"High-dose XNP": "XNP", "High_dose_XNP": "XNP"})
        sub = sub[sub["g"].isin(GROUP_ORDER)]
        ax[ai].scatter(sub["PC1"], sub["PC2"], c=[GROUP_COL[g] for g in sub["g"]], s=40, edgecolor="k", linewidth=0.3)
        ax[ai].set_title(f"PCoA ({metric})", fontsize=9)
        ax[ai].set_xlabel("PC1"); ax[ai].set_ylabel("PC2")

    phyl = ra.copy()
    phyl.index = [asv2phylum.get(a, "Unknown") for a in phyl.index]
    long = phyl.reset_index().melt(id_vars="index", var_name="sample", value_name="ab")
    long["group"] = long["sample"].map(_sample_group)
    long = long[long["group"].isin(GROUP_ORDER)]
    piv = long.pivot_table(index="index", columns="group", values="ab", aggfunc="mean").fillna(0)
    top10 = piv.sum(axis=1).sort_values(ascending=False).head(10).index
    pct = piv.loc[top10] / piv.loc[top10].sum(axis=0) * 100
    bottom = np.zeros(3)
    for ph in top10:
        ax[5].bar(GROUP_ORDER, pct.loc[ph].values, bottom=bottom, label=ph)
        bottom += pct.loc[ph].values
    ax[5].set_title("Top-10 phylum mean RA", fontsize=9)
    ax[5].set_ylabel("% of RA")
    ax[5].legend(fontsize=5, ncol=1, loc="center left", bbox_to_anchor=(1.0, 0.5))

    mean_ra = ra.mean(axis=1).sort_values(ascending=False)
    ax[6].plot(np.arange(1, len(mean_ra) + 1), mean_ra.values, color="black", linewidth=1)
    ax[6].set_yscale("log")
    ax[6].set_title("Rank-abundance (mean)", fontsize=9)
    ax[6].set_xlabel("ASV rank"); ax[6].set_ylabel("Mean rel. ab. (log)")

    top20 = ra.mean(axis=1).sort_values(ascending=False).head(20).index
    hm = ra.loc[top20, [s for s in ra.columns if _sample_group(s) in GROUP_ORDER]]
    grp_order_cols = [s for g in GROUP_ORDER for s in hm.columns if _sample_group(s) == g]
    hm = hm[grp_order_cols]
    im = ax[7].imshow(hm.to_numpy(float), aspect="auto", cmap="viridis")
    ax[7].set_title("Top-20 ASV x group (mean RA)", fontsize=9)
    ax[7].set_yticks(range(len(top20))); ax[7].set_yticklabels(top20, fontsize=5)
    ax[7].set_xticks(range(hm.shape[1])); ax[7].set_xticklabels([_sample_group(c) for c in hm.columns], rotation=90, fontsize=5)
    fig.colorbar(im, ax=ax[7], fraction=0.046, pad=0.04)

    _save_multi(base, fig)
    return {"figure": "Fig_S1_Microbiome", "panels": 8, "samples": len(gs), "asv": int(M.shape[0])}


def fig_s2_scrna(base: Path) -> Dict:
    import anndata as ad
    adata = ad.read_h5ad(str(H5AD))
    grp_full = adata.obs["group"].astype(str).replace({"High_dose_XNP": "XNP"})
    mask = grp_full.isin(GROUP_ORDER).values
    umap = adata.obsm["X_umap"][mask]
    obs = adata.obs.loc[mask].copy()
    obs["group"] = grp_full[mask].values
    leiden = obs["leiden"].astype(int).values
    n = int(mask.sum())

    rng = np.random.RandomState(42)
    idx = rng.choice(n, size=min(40000, n), replace=False)
    u = umap[idx]; g = obs["group"].values[idx]; le = leiden[idx]

    fig, ax = _grid()
    for grp in GROUP_ORDER:
        m = g == grp
        ax[0].scatter(u[m, 0], u[m, 1], s=1.0, color=GROUP_COL[grp], label=grp, alpha=0.5, linewidths=0)
    ax[0].set_title("UMAP by group", fontsize=9); ax[0].legend(fontsize=6, markerscale=3)
    ax[0].set_xticks([]); ax[0].set_yticks([])

    uniq = sorted(np.unique(le))
    cmap = plt.cm.tab20
    for i, cl in enumerate(uniq):
        m = le == cl
        ax[1].scatter(u[m, 0], u[m, 1], s=1.0, color=cmap(i % 20), alpha=0.5, linewidths=0)
    ax[1].set_title(f"UMAP by leiden ({len(uniq)} clusters)", fontsize=9)
    ax[1].set_xticks([]); ax[1].set_yticks([])

    comp = pd.Series(leiden).value_counts()
    top = comp.head(12).index.tolist()
    prop = np.zeros((3, 13))
    for gi, grp in enumerate(GROUP_ORDER):
        sub = leiden[obs["group"].values == grp]
        vc = pd.Series(sub).value_counts(normalize=True)
        for ti, cl in enumerate(top):
            prop[gi, ti] = vc.get(cl, 0.0)
        prop[gi, 12] = 1 - prop[gi, :12].sum()
    bottom = np.zeros(3)
    for ti in range(13):
        ax[2].bar(GROUP_ORDER, prop[:, ti] * 100, bottom=bottom,
                  color=(cmap(ti % 20) if ti < 12 else "#999999"))
        bottom += prop[:, ti] * 100
    ax[2].set_title("Cluster composition by group", fontsize=9)
    ax[2].set_ylabel("% of cells")
    ax[2].tick_params(axis="x", rotation=20)

    samples = sorted(obs["sample"].unique())
    scmap = {s: plt.cm.tab20(i % 20) for i, s in enumerate(samples)}
    for s in samples:
        m = obs["sample"].values[idx] == s
        ax[3].scatter(u[m, 0], u[m, 1], s=0.8, color=scmap[s], alpha=0.5, linewidths=0)
    ax[3].set_title(f"UMAP by sample ({len(samples)})", fontsize=9)
    ax[3].set_xticks([]); ax[3].set_yticks([])

    ax[4].bar([str(c) for c in top], [comp[c] * 100 / n for c in top], color=[cmap(i % 20) for i in range(12)])
    ax[4].set_title("Top-10 cluster abundance", fontsize=9)
    ax[4].set_ylabel("% of all cells"); ax[4].tick_params(axis="x", rotation=90)

    ax[5].bar(range(len(uniq)), comp.values, color="#888888")
    ax[5].set_title("Cluster sizes", fontsize=9)
    ax[5].set_xlabel("cluster id"); ax[5].set_ylabel("n cells")

    for grp in GROUP_ORDER:
        ax[6].hist(obs["n_genes"].values[obs["group"].values == grp], bins=40, density=True,
                   histtype="step", color=GROUP_COL[grp], label=grp, linewidth=1.2)
    ax[6].set_title("n_genes distribution", fontsize=9); ax[6].legend(fontsize=6); ax[6].set_xlabel("n_genes")

    parts = [obs["n_counts"].values[obs["group"].values == grp] for grp in GROUP_ORDER]
    ax[7].violinplot(parts, showmedians=True)
    ax[7].set_xticks(range(1, 4)); ax[7].set_xticklabels(GROUP_ORDER, rotation=20)
    ax[7].set_title("n_counts (UMI) by group", fontsize=9); ax[7].set_ylabel("n_counts")

    _save_multi(base, fig)
    return {"figure": "Fig_S2_scRNA", "cells": int(n), "clusters": int(len(uniq))}


def _pca_layer(expr_csv, meta_csv, layer, ax_pca, ax_box, topN=200):
    e = pd.read_csv(expr_csv).set_index("feature_id")
    m = pd.read_csv(meta_csv)
    m["group"] = m["group"].replace({"High_dose_XNP": "XNP"})
    m = m[m["group"].isin(GROUP_ORDER)]
    cols = m["sample"].tolist()
    Xmat = e[cols].to_numpy(float).T
    Y = m["group"].values
    tv = _top_var_idx(e[cols].to_numpy(float), topN)
    Xt = Xmat[:, tv]
    scores, ev = _pca(Xt, 2)
    for gi, grp in enumerate(GROUP_ORDER):
        mm = Y == grp
        ax_pca.scatter(scores[mm, 0], scores[mm, 1], s=45, color=GROUP_COL[grp], label=grp,
                       edgecolor="k", linewidth=0.3)
    ax_pca.set_title(f"PCA - {layer}", fontsize=9)
    ax_pca.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)"); ax_pca.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)")
    ax_pca.legend(fontsize=6)
    feat = e.index[tv[0]]
    vals = {grp: e.loc[feat, cols][Y == grp].to_numpy(float) for grp in GROUP_ORDER}
    ax_box.boxplot([vals[g] for g in GROUP_ORDER], tick_labels=GROUP_ORDER, patch_artist=True,
                   boxprops=dict(facecolor="#dddddd"))
    for j, grp in enumerate(GROUP_ORDER):
        xs = np.random.RandomState(1).normal(j + 1, 0.05, len(vals[grp]))
        ax_box.scatter(xs, vals[grp], s=12, color=GROUP_COL[grp], zorder=3, alpha=0.8)
    ax_box.set_title(f"Top-var feature - {layer}", fontsize=9)
    ax_box.set_ylabel("log2 intensity")
    ax_box.tick_params(axis="x", rotation=20)
    return ev, str(feat)


def fig_s3_metabolome(base: Path) -> Dict:
    fig, ax = _grid()
    layers = ["Fecal", "Serum", "Brain"]
    evs = {}
    for i, layer in enumerate(layers):
        ev, feat = _pca_layer(DIST_DATA / f"metabolome_{layer}_expr.csv",
                              DIST_DATA / f"metabolome_{layer}_meta.csv",
                              layer, ax[i], ax[3 + i])
        evs[layer] = (ev.tolist(), feat)
    for i, layer in enumerate(layers):
        ev = np.array(evs[layer][0]); full = np.concatenate([ev, [0] * (3 - len(ev))])
        ax[6].bar([f"{layer}\nPC{j+1}" for j in range(3)], full[:3], label=layer if i == 0 else None)
    ax[6].set_title("Variance explained (PC1-3)", fontsize=9)
    ax[6].set_ylabel("% variance")
    e = pd.read_csv(DIST_DATA / "metabolome_Fecal_expr.csv").set_index("feature_id")
    m = pd.read_csv(DIST_DATA / "metabolome_Fecal_meta.csv")
    m["group"] = m["group"].replace({"High_dose_XNP": "XNP"})
    m = m[m["group"].isin(GROUP_ORDER)]
    cols = [s for g in GROUP_ORDER for s in m[m["group"] == g]["sample"]]
    tv = _top_var_idx(e[cols].to_numpy(float), 30)
    hm = e.iloc[tv][cols].to_numpy(float)
    hm = (hm - hm.mean(axis=1, keepdims=True)) / (hm.std(axis=1, keepdims=True) + 1e-9)
    im = ax[7].imshow(hm, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
    ax[7].set_title("Top-30 var metabolites (Fecal)", fontsize=9)
    ax[7].set_xticks(range(len(cols))); ax[7].set_xticklabels([_sample_group(c) for c in cols], rotation=90, fontsize=5)
    ax[7].set_yticks([])
    fig.colorbar(im, ax=ax[7], fraction=0.046, pad=0.04)
    _save_multi(base, fig)
    return {"figure": "Fig_S3_Metabolome", "layers": layers, "top_features": evs}


def _pca_layer_prot(expr_csv, meta_csv, layer, ax_pca, ax_box, ax_heat, topN=300):
    e = pd.read_csv(expr_csv).set_index("feature_id")
    m = pd.read_csv(meta_csv)
    m["group"] = m["group"].replace({"High_dose_XNP": "XNP"})
    m = m[m["group"].isin(GROUP_ORDER)]
    cols = m["sample"].tolist()
    Xmat = e[cols].to_numpy(float)
    keep = ~np.isnan(Xmat).all(axis=1)
    Xmat = Xmat[keep]; e2 = e.iloc[keep]
    floor = float(np.nanmin(Xmat) - 1.0)
    Xmat = np.where(np.isnan(Xmat), floor, Xmat)
    Xt = Xmat.T
    tv = _top_var_idx(Xt, topN)
    scores, ev = _pca(Xt[:, tv], 2)
    Y = m["group"].values
    for gi, grp in enumerate(GROUP_ORDER):
        mm = Y == grp
        ax_pca.scatter(scores[mm, 0], scores[mm, 1], s=45, color=GROUP_COL[grp], label=grp,
                       edgecolor="k", linewidth=0.3)
    ax_pca.set_title(f"PCA - {layer}", fontsize=9)
    ax_pca.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)"); ax_pca.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)")
    ax_pca.legend(fontsize=6)
    feat = e2.index[tv[0]]
    vals = {grp: e2.loc[feat, cols][Y == grp].to_numpy(float) for grp in GROUP_ORDER}
    ax_box.boxplot([vals[g] for g in GROUP_ORDER], tick_labels=GROUP_ORDER, patch_artist=True,
                   boxprops=dict(facecolor="#dddddd"))
    for j, grp in enumerate(GROUP_ORDER):
        xs = np.random.RandomState(2).normal(j + 1, 0.05, len(vals[grp]))
        ax_box.scatter(xs, vals[grp], s=12, color=GROUP_COL[grp], zorder=3, alpha=0.8)
    ax_box.set_title(f"Top-var protein - {layer}", fontsize=9)
    ax_box.set_ylabel("log2 intensity"); ax_box.tick_params(axis="x", rotation=20)
    cols_ord = [s for g in GROUP_ORDER for s in m[m["group"] == g]["sample"]]
    tvh = _top_var_idx(Xt, 30)
    hm = Xt[np.ix_(tvh, [cols.index(c) for c in cols_ord])]
    hm = (hm - hm.mean(axis=1, keepdims=True)) / (hm.std(axis=1, keepdims=True) + 1e-9)
    im = ax_heat.imshow(hm, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
    ax_heat.set_title(f"Top-30 var proteins ({layer})", fontsize=9)
    ax_heat.set_xticks(range(len(cols_ord))); ax_heat.set_xticklabels([_sample_group(c) for c in cols_ord], rotation=90, fontsize=5)
    ax_heat.set_yticks([])
    ax_heat.figure.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
    return ev, str(feat)


def fig_s4_proteome(base: Path) -> Dict:
    fig, ax = _grid()
    layers = ["Brain", "Serum"]
    info = {}
    for i, layer in enumerate(layers):
        ev, feat = _pca_layer_prot(DIST_DATA / f"proteome_{layer}_expr.csv",
                                   DIST_DATA / f"proteome_{layer}_meta.csv",
                                   layer, ax[i], ax[2 + i], ax[4 + i])
        info[layer] = (ev.tolist(), feat)
    for i, layer in enumerate(layers):
        ev = np.array(info[layer][0]); full = np.concatenate([ev, [0]*(3-len(ev))])
        ax[6].bar([f"{layer}\nPC{j+1}" for j in range(3)], full[:3])
    ax[6].set_title("Variance explained (PC1-3)", fontsize=9)
    ax[6].set_ylabel("% variance")
    for i, layer in enumerate(layers):
        e = pd.read_csv(DIST_DATA / f"proteome_{layer}_expr.csv").set_index("feature_id")
        m = pd.read_csv(DIST_DATA / f"proteome_{layer}_meta.csv")
        m["group"] = m["group"].replace({"High_dose_XNP": "XNP"})
        m = m[m["group"].isin(GROUP_ORDER)]
        cols = m["sample"].tolist()
        det = {grp: 100 * (1 - e[cols].isna().sum(axis=0)[m["group"].values == grp].mean() / e.shape[0]) for grp in GROUP_ORDER}
        ax[7].bar([f"{layer}\n{g}" for g in GROUP_ORDER], [det[g] for g in GROUP_ORDER], color=[GROUP_COL[g] for g in GROUP_ORDER])
    ax[7].set_title("Protein quantification rate", fontsize=9)
    ax[7].set_ylabel("% detected")
    _save_multi(base, fig)
    return {"figure": "Fig_S4_Proteome", "layers": layers, "top_features": info}


def generate_all() -> Dict:
    out = {}
    out["Fig_S1_Microbiome"] = fig_s1_microbiome(OUT_DIR / "FigS1_Microbiome" / "FigS1_Microbiome_multiomics")
    out["Fig_S2_scRNA"]      = fig_s2_scrna(OUT_DIR / "FigS2_scRNA" / "FigS2_scRNA_multiomics")
    out["Fig_S3_Metabolome"] = fig_s3_metabolome(OUT_DIR / "FigS3_Metabolome" / "FigS3_Metabolome_multiomics")
    out["Fig_S4_Proteome"]   = fig_s4_proteome(OUT_DIR / "FigS4_Proteome" / "FigS4_Proteome_multiomics")
    (OUT_DIR / "dist_summary.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    res = generate_all()
    print(json.dumps(res, indent=2, ensure_ascii=False))
