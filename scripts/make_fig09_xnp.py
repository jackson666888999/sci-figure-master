#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig09 — 多组学收敛（纯组学版主轴证据图）
Panel A: 16S 6方法共识差异菌（表S15）
Panel B: 血清嘌呤/吲哚代谢物（G2/G1 几何，biomni）
Panel C: MOFA2 Factor3 三组分布（表S14）
Panel D: 单核 FDR 基因（小胶质/OPC，biomni）
Nature 风格：6.5pt / 183mm / 仅 bottom+left spines / SVG+PDF+TIFF600+PNG300
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import os

# ── 输出目录 ──
OUTDIR = r"E:\XNP论文初稿\02_论文\figures\Fig09"
SRC = r"E:\XNP论文初稿\02_论文\figures\Fig09_source_data"
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 6.5, "axes.labelsize": 7, "axes.titlesize": 7.5,
    "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6,
    "font.family": "Microsoft YaHei", "axes.unicode_minus": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "svg.fonttype": "none", "pdf.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})

# ── 配色 ──
C_G1 = "#3B6FA0"      # 恢复（蓝）
C_G2 = "#E07B39"      # XNP 特有（橙）
C_MC = "#7F8C8D"      # SD 改变未恢复（灰）
C_MG = "#8E44AD"      # Microglia 紫
C_OPC = "#16A085"     # OPC 青
C_CTRL = "#5D6D7E"; C_MODEL = "#C0392B"; C_XNP = "#E07B39"

def savefig(fig, name):
    for ext, dpi in [("svg", None), ("pdf", None), ("tiff", 600), ("png", 300)]:
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), dpi=dpi,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)

# ============================================================
# Panel A — 16S 6方法共识
# ============================================================
s15 = pd.read_csv(os.path.join(SRC, "Fig9A_16S_6method.csv"))
s15["genus_clean"] = s15["属"].str.replace("_unclassified", " (uncl.)", regex=False)
# 分类
def a_geom(r):
    if pd.notna(r["MC_LFC"]):
        return "MC-only (SD改变,XNP未恢复)" if pd.isna(r["XM_LFC"]) else "G1"
    return "G2_XNP_specific (仅XNP改变)"
s15["geom"] = s15.apply(a_geom, axis=1)
mc_rows = s15[pd.notna(s15["MC_LFC"])].sort_values("MC_LFC")
xm_rows = s15[pd.isna(s15["MC_LFC"])].sort_values("XM_LFC")
# 合并显示：先 MC（4），后 XM（9）
plot_rows = pd.concat([mc_rows, xm_rows])

fig = plt.figure(figsize=(7.2, 5.6))
gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.45,
                      left=0.10, right=0.97, top=0.93, bottom=0.09)

# ---- A ----
axA = fig.add_subplot(gs[0, 0])
labels, vals, cols = [], [], []
for _, r in plot_rows.iterrows():
    v = r["MC_LFC"] if pd.notna(r["MC_LFC"]) else r["XM_LFC"]
    labels.append(r["genus_clean"])
    vals.append(v)
    if pd.notna(r["MC_LFC"]):
        cols.append(C_MC)
    else:
        cols.append(C_G2)
y = np.arange(len(labels))[::-1]
axA.barh(y, vals, color=cols, height=0.62, edgecolor="none")
axA.set_yticks(y); axA.set_yticklabels(labels, fontsize=5.6)
axA.axvline(0, color="black", lw=0.5)
axA.set_xlabel("Wilcoxon log2FC")
axA.set_title("A  16S 菌群 6 方法共识（≥4/6 方法）", loc="left")
# 标注方法数
for i, (_, r) in enumerate(plot_rows.iterrows()):
    v = r["MC_LFC"] if pd.notna(r["MC_LFC"]) else r["XM_LFC"]
    n = r["MC_n_sig"] if pd.notna(r["MC_LFC"]) else r["XM_n_sig"]
    axA.text(v + (0.08 if v >= 0 else -0.08), y[i], f"{n}/6",
             va="center", ha="left" if v >= 0 else "right", fontsize=5)
# 图例（简化标签 + 移至外侧）
from matplotlib.patches import Patch
axA.legend(handles=[Patch(color=C_MC, label="MC-only"),
                    Patch(color=C_G2, label="G2_XNP_specific")],
           loc="upper right", frameon=False, fontsize=5.5)

# ---- B ----
axB = fig.add_subplot(gs[0, 1])
sb = pd.read_csv(os.path.join(SRC, "Fig9B_serum_metabolites.csv"))
sb = sb.sort_values("XM_log2FC")
y = np.arange(len(sb))[::-1]
colsB = [C_G1 if g == "G1_restoration" else C_G2 for g in sb["geometry"]]
axB.barh(y, sb["XM_log2FC"], color=colsB, height=0.62)
axB.set_yticks(y); axB.set_yticklabels(sb["metabolite"], fontsize=5.4)
axB.axvline(0, color="black", lw=0.5)
axB.set_xlabel("XM log2FC")
axB.set_title("B  血清嘌呤/吲哚代谢物", loc="left")
for i, (_, r) in enumerate(sb.iterrows()):
    axB.text(r["XM_log2FC"] + (0.1 if r["XM_log2FC"] >= 0 else -0.1), y[i],
             f"FDR={r['FDR']:.3g}", va="center",
             ha="left" if r["XM_log2FC"] >= 0 else "right", fontsize=5)
axB.legend(handles=[Patch(color=C_G1, label="G1_restoration"),
                    Patch(color=C_G2, label="G2_XNP_specific")],
           loc="upper right", frameon=False, fontsize=5.5)

# ---- C ----
axC = fig.add_subplot(gs[1, 0])
sc = pd.read_csv(os.path.join(SRC, "Fig9C_MOFA_Factor3.csv"))
order = ["Control", "Model", "High_dose_XNP"]
gcols = {"Control": C_CTRL, "Model": C_MODEL, "High_dose_XNP": C_XNP}
xpos = np.arange(3)
for xi, g in enumerate(order):
    vals = sc.loc[sc["group"] == g, "Factor3"]
    jit = np.random.default_rng(42).uniform(-0.12, 0.12, len(vals))
    axC.scatter(xi + jit, vals, s=14, color=gcols[g], alpha=0.85, edgecolor="none", zorder=3)
    axC.hlines(vals.mean(), xi - 0.28, xi + 0.28, color=gcols[g], lw=1.4, zorder=4)
axC.set_xticks(xpos); axC.set_xticklabels(["Control", "Model", "XNP"], fontsize=6)
axC.set_ylabel("MOFA2 Factor 3 得分")
axC.set_title("C  MOFA2 Factor3（K-W p=0.0062）", loc="left")
axC.text(0.02, 0.96, "MvC p=0.026\nXvM p=0.0022", transform=axC.transAxes,
         fontsize=5.5, va="top", ha="left", color="#555555")

# ---- D ----
axD = fig.add_subplot(gs[1, 1])
sd = pd.read_csv(os.path.join(SRC, "Fig9D_scRNA_FDR_genes.csv"))
sd["label"] = sd["gene"] + " · " + sd["celltype"]
sd = sd.sort_values("XC_log2FC")
y = np.arange(len(sd))[::-1]
colsD = [C_MG if ct == "Microglia" else C_OPC for ct in sd["celltype"]]
axD.barh(y, sd["XC_log2FC"], color=colsD, height=0.55)
axD.set_yticks(y); axD.set_yticklabels(sd["label"], fontsize=5.8)
axD.axvline(0, color="black", lw=0.5)
axD.set_xlabel("XC log2FC")
axD.set_title("D  单核 FDR<0.05 基因（小胶质/OPC）", loc="left")
for i, (_, r) in enumerate(sd.iterrows()):
    axD.text(r["XC_log2FC"] + (0.06 if r["XC_log2FC"] >= 0 else -0.06), y[i],
             f"FDR={r['FDR']:.3g}", va="center",
             ha="left" if r["XC_log2FC"] >= 0 else "right", fontsize=5)
axD.legend(handles=[Patch(color=C_MG, label="Microglia"),
                    Patch(color=C_OPC, label="OPC")],
           loc="upper right", frameon=False, fontsize=5.5)

savefig(fig, "Fig09_Multiomics_Convergence")
print("Fig09 saved ->", OUTDIR)
