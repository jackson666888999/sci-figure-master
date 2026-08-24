# -*- coding: utf-8 -*-
"""
XNP 多组学论文 — PLS-DA 监督判别分析图（Fig_S5 / Fig_S6）

方法（sklearn 1.9 已移除 PLSDiscriminantAnalysis，故用 PLSRegression + one-hot Y 实现经典 PLS-DA）：
  - 经典 PLS-DA：X 标准化，Y 为组别的 one-hot 矩阵，PLSRegression(n_components=2)
  - 得分图：transform(X) 前两分量
  - VIP 值：标准公式 VIP_j = sqrt( p * sum_a[s_a*(w*_{a,j})^2] / sum_a s_a )
  - 模型验证：留一交叉验证(LOO) 分类准确率 + Q2 = 1 - PRESS/TSS
  - 置换检验：200 次打乱 Y 标签重算 LOO 准确率，得经验 p 值

数据来源：E:/XNP论文初稿/05_图件/_dist_data/ 下由 omics_data.rds 导出的真实样本×特征强度矩阵
  （代谢组 log2 强度；蛋白组 log2 强度，缺失值以特征检测下限常量填充）
Nature/Science 标准：英文标签、DejaVu Sans、bottom/left spines、高对比三组配色、SVG+PDF+PNG300+Tiff600。
数据红线：本脚本只读 E: 中间文件，绝不在 D:/乌灵菌 测序目录写任何东西。
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pathlib import Path
from typing import Dict, List, Any, Tuple

from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict, LeaveOneOut

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

DIST_DATA = Path("E:/XNP论文初稿/05_图件/_dist_data")
OUT_DIR   = Path("E:/XNP论文初稿/05_图件")

N_PERM = 200
TOPN   = 50    # 非 DE 层的回退：top-N 方差特征预筛选（避免 p>>n 严重过拟合）
DE_FALLBACK_MIN = 10  # DE 特征数 >= 此值才用 DE 子集，否则回退 top-N 方差

# DE 三线表（提供与 expr 同源的 feature_id 与显著性）
DE_TABLE = {
    "metabolome": "D:/乌灵菌/机制轴/tables/T01_metabolome_DE_full.csv",
    "proteome":   "D:/乌灵菌/机制轴/tables/T04_proteome_DE_full.csv",
}
DE_FDR_COLS = {
    "metabolome": ["FDR"],
    "proteome":   ["FDR_DEqMS", "FDR_limma"],
}


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


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------
def de_ids_for(om: str, layer: str) -> set:
    """从项目 DE 三线表取该层显著特征（sig==True 或任一 FDR<0.05）。"""
    import warnings
    df = pd.read_csv(DE_TABLE[om])
    df = df[df["layer"].astype(str) == layer]
    mask = df["sig"].astype(str).str.lower().isin(["true", "1"])
    for c in DE_FDR_COLS[om]:
        if c in df.columns:
            mask = mask | (pd.to_numeric(df[c], errors="coerce") < 0.05)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return set(df.loc[mask, "feature_id"].astype(str))


def load_layer(om: str, layer: str, de_ids: set = None):
    meta = pd.read_csv(DIST_DATA / f"{om}_{layer}_meta.csv")
    expr = pd.read_csv(DIST_DATA / f"{om}_{layer}_expr.csv").set_index("feature_id")
    meta["group"] = meta["group"].replace({"High_dose_XNP": "XNP"})
    meta = meta[meta["group"].isin(GROUP_ORDER)].reset_index(drop=True)
    cols = meta["sample"].tolist()
    Xt = expr[cols].T                      # 行=样本，列=特征（feature_id 在列名）
    X = Xt.values.astype(float)

    if om == "proteome":                   # 检测下限填充（per-feature min）
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            floor = np.nanmin(X, axis=0)
            gmin = np.nanmin(X)
        floor = np.where(np.isnan(floor), gmin, floor)
        X = np.where(np.isnan(X), floor, X)
        Xt = pd.DataFrame(X, index=Xt.index, columns=Xt.columns)

    fids_all = list(Xt.columns)

    # 优先用 DE 显著特征；不足则回退 top-N 方差
    use_ids = None
    source = "all_var"
    if de_ids:
        inter = [i for i in fids_all if str(i) in de_ids]
        if len(inter) >= DE_FALLBACK_MIN:
            use_ids = inter
            source = f"de_sig({len(inter)})"

    if use_ids is None:
        if X.shape[1] > TOPN:
            var = np.nanvar(X, axis=0)
            keep = np.argsort(var)[::-1][:TOPN]
            X = X[:, keep]
            fids = [fids_all[i] for i in keep]
        else:
            fids = fids_all
        return X, fids, meta["group"].values, source

    sub = Xt[use_ids]                      # 特征是列，按列选取
    X = sub.values.astype(float)
    fids = list(sub.columns)
    return X, fids, meta["group"].values, source


# ---------------------------------------------------------------------------
# PLS-DA 核心
# ---------------------------------------------------------------------------
def _onehot(y: np.ndarray):
    classes = np.array(sorted(np.unique(y)))
    Y = np.zeros((len(y), len(classes)))
    for i, c in enumerate(classes):
        Y[y == c, i] = 1.0
    return Y, classes


def plsda(X: np.ndarray, y: np.ndarray, n_comp: int = 2) -> Dict[str, Any]:
    Y, classes = _onehot(y)
    pls = PLSRegression(n_components=n_comp, scale=True)
    pls.fit(X, Y)
    scores = pls.transform(X)
    Yhat = pls.predict(X)
    ypred = classes[np.argmax(Yhat, axis=1)]
    acc = float((ypred == y).mean())

    loo = LeaveOneOut()
    Yhat_cv = cross_val_predict(PLSRegression(n_components=n_comp, scale=True), X, Y,
                                cv=loo, method="predict")
    ypred_cv = classes[np.argmax(Yhat_cv, axis=1)]
    cv_acc = float((ypred_cv == y).mean())
    Ymean = Y.mean(axis=0)
    Q2 = 1.0 - float(np.sum((Y - Yhat_cv) ** 2) / np.sum((Y - Ymean) ** 2))
    return dict(pls=pls, scores=scores, acc=acc, cv_acc=cv_acc, Q2=Q2,
                ypred_cv=ypred_cv, Y=Y, classes=classes)


def vip(pls: PLSRegression) -> np.ndarray:
    t = pls.x_scores_
    w = pls.x_weights_
    q = pls.y_loadings_
    p, h = w.shape
    s = np.sum(t ** 2, axis=0) * np.sum(q ** 2, axis=0)
    wnorm = w / np.linalg.norm(w, axis=0)
    return np.sqrt(p * (wnorm ** 2 @ s) / np.sum(s))


def perm_test(X: np.ndarray, y: np.ndarray, n_comp: int = 2, n_perm: int = N_PERM):
    Y, classes = _onehot(y)
    loo = LeaveOneOut()
    Yhat_cv = cross_val_predict(PLSRegression(n_components=n_comp, scale=True), X, Y,
                                cv=loo, method="predict")
    obs = float((classes[np.argmax(Yhat_cv, axis=1)] == y).mean())
    rng = np.random.default_rng(7)
    null = np.empty(n_perm)
    for b in range(n_perm):
        yp = rng.permutation(y)
        Yp, _ = _onehot(yp)
        Yh = cross_val_predict(PLSRegression(n_components=n_comp, scale=True), X, Yp,
                               cv=loo, method="predict")
        null[b] = float((classes[np.argmax(Yh, axis=1)] == yp).mean())
    pval = (np.sum(null >= obs) + 1) / (n_perm + 1)
    return obs, null, float(pval)


# ---------------------------------------------------------------------------
# 面板绘制
# ---------------------------------------------------------------------------
def _ellipse(ax, x, y, color, nstd=2):
    if len(x) < 3:
        return
    cov = np.cov(x, y)
    lam, vec = np.linalg.eigh(cov)
    ang = np.degrees(np.arctan2(vec[1, 0], vec[0, 0]))
    a, b = nstd * np.sqrt(lam[0]), nstd * np.sqrt(lam[1])
    e = Ellipse((x.mean(), y.mean()), 2 * a, 2 * b, angle=ang,
                edgecolor=color, facecolor="none", lw=1.0, ls="--", alpha=0.8)
    ax.add_patch(e)


def _panel_score(ax, r: Dict, y: np.ndarray, title: str):
    sc = r["scores"]
    for grp in GROUP_ORDER:
        m = y == grp
        ax.scatter(sc[m, 0], sc[m, 1], s=45, color=GROUP_COL[grp], label=grp,
                   edgecolor="k", linewidth=0.3, zorder=3)
        _ellipse(ax, sc[m, 0], sc[m, 1], GROUP_COL[grp])
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("PLS-DA 1"); ax.set_ylabel("PLS-DA 2")
    ax.legend(fontsize=6, loc="best")
    ax.text(0.02, 0.97, f"CV acc={r['cv_acc']*100:.1f}%  Q²={r['Q2']:.2f}",
            transform=ax.transAxes, fontsize=6, va="top",
            bbox=dict(boxstyle="round", fc="white", ec="#cccccc", lw=0.5))


def _panel_vip(ax, vipv: np.ndarray, fids: List[str], title: str):
    top = np.argsort(vipv)[::-1][:15][::-1]
    vals = vipv[top]
    names = [str(fids[i])[:16] for i in top]
    colors = ["#C0392B" if v >= 1 else "#888888" for v in vals]
    ax.barh(range(len(top)), vals, color=colors)
    ax.set_yticks(range(len(top))); ax.set_yticklabels(names, fontsize=5)
    ax.axvline(1.0, color="black", lw=0.8, ls="--")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("VIP")
    ax.text(0.98, 0.05, "red: VIP>1", transform=ax.transAxes, fontsize=5,
            ha="right", color="#C0392B")


def _panel_perm(ax, perm, title: str):
    obs, null, pval = perm
    ax.hist(null, bins=20, color="#cccccc", edgecolor="black", linewidth=0.5)
    ax.axvline(obs, color=C_MODEL, lw=1.5, label=f"observed={obs*100:.1f}%")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("permuted CV accuracy")
    ax.set_ylabel("frequency")
    ax.legend(fontsize=6)
    ax.text(0.02, 0.95, f"p={pval:.3f}", transform=ax.transAxes, fontsize=7, va="top",
            bbox=dict(boxstyle="round", fc="white", ec="#cccccc", lw=0.5))


def _panel_acc(ax, layer_res: Dict[str, Dict]):
    layers = list(layer_res.keys())
    accs = [layer_res[L]["cv_acc"] * 100 for L in layers]
    q2 = [layer_res[L]["Q2"] for L in layers]
    bars = ax.bar(range(len(layers)), accs, color="#2E75B6", edgecolor="black", linewidth=0.5)
    ax.set_xticks(range(len(layers)))
    ax.set_xticklabels(layers, rotation=20, fontsize=6)
    ax.set_ylim(0, 105)
    ax.set_ylabel("LOO CV accuracy (%)")
    ax.set_title("Cross-validated accuracy", fontsize=9)
    for i, (a, q) in enumerate(zip(accs, q2)):
        ax.text(i, a + 1.5, f"{a:.0f}%\nQ²={q:.2f}", ha="center", fontsize=5)


def _panel_loading(ax, r: Dict, fids: List[str], title: str):
    w = r["pls"].x_loadings_[:, 0]
    top = np.argsort(np.abs(w))[::-1][:20][::-1]
    vals = w[top]
    names = [str(fids[i])[:16] for i in top]
    colors = [C_MODEL if v > 0 else C_CTRL for v in vals]
    ax.barh(range(len(top)), vals, color=colors)
    ax.set_yticks(range(len(top))); ax.set_yticklabels(names, fontsize=5)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("loading (comp 1)")


# ---------------------------------------------------------------------------
# 整图组装
# ---------------------------------------------------------------------------
def build_specs(layers: List[str]) -> List[Tuple[str, str]]:
    specs: List[Tuple[str, str]] = [("score", L) for L in layers]
    specs.append(("perm", layers[0]))
    specs += [("vip", L) for L in layers]
    specs.append(("acc", ""))
    li = 0
    while len(specs) < 8:
        specs.append(("loading", layers[li % len(layers)]))
        li += 1
    return specs[:8]


def fig_plsda(om: str, layers: List[str], base: Path, prefix: str) -> Dict:
    data = {}
    for L in layers:
        de_ids = de_ids_for(om, L)
        X, fids, y, source = load_layer(om, L, de_ids)
        r = plsda(X, y, n_comp=2)
        vv = vip(r["pls"])
        perm = perm_test(X, y, n_comp=2)
        data[L] = dict(r=r, vip=vv, fids=fids, y=y, perm=perm, source=source)

    specs = build_specs(layers)
    fig, ax = _grid()
    for k, (kind, L) in enumerate(specs):
        if kind == "score":
            _panel_score(ax[k], data[L]["r"], data[L]["y"], f"PLS-DA score - {L}")
        elif kind == "vip":
            _panel_vip(ax[k], data[L]["vip"], data[L]["fids"], f"VIP (top 15) - {L}")
        elif kind == "perm":
            _panel_perm(ax[k], data[L]["perm"], f"Permutation test - {L}")
        elif kind == "acc":
            _panel_acc(ax[k], {L: data[L]["r"] for L in layers})
        elif kind == "loading":
            _panel_loading(ax[k], data[L]["r"], data[L]["fids"], f"Loadings c1 - {L}")

    _save_multi(base, fig)
    return {
        "figure": prefix,
        "omics": om,
        "layers": {L: {"cv_acc": data[L]["r"]["cv_acc"], "Q2": data[L]["r"]["Q2"],
                      "train_acc": data[L]["r"]["acc"],
                      "perm_p": data[L]["perm"][2],
                      "n_features": len(data[L]["fids"]),
                      "feature_source": data[L]["source"],
                      "top_vip": [str(data[L]["fids"][i]) for i in np.argsort(data[L]["vip"])[::-1][:10]]}
                  for L in layers},
    }


def generate_all() -> Dict:
    out = {}
    out["Fig_S5_PLSDA_Metabolome"] = fig_plsda(
        "metabolome", ["Fecal", "Serum", "Brain"],
        OUT_DIR / "FigS5_PLSDA_Metabolome" / "FigS5_PLSDA_Metabolome_multiomics",
        "Fig_S5_PLSDA_Metabolome")
    out["Fig_S6_PLSDA_Proteome"] = fig_plsda(
        "proteome", ["Brain", "Serum"],
        OUT_DIR / "FigS6_PLSDA_Proteome" / "FigS6_PLSDA_Proteome_multiomics",
        "Fig_S6_PLSDA_Proteome")
    (OUT_DIR / "plsda_summary.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


if __name__ == "__main__":
    summary = generate_all()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
