# -*- coding: utf-8 -*-
"""
XNP 多组学论文 Fig1-8：每个组学一个大图（8 面板，2×4 布局）
Nature/Science 投稿标准：英文标签、高对比配色、bottom/left spines only、
无黑色图例背景、SVG+PDF+PNG300+Tiff600 多格式输出。
数据红线：仅用真实三线表 CSV，绝不虚构。
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
from typing import Dict, List, Any

# ── Nature 风格全局设置 ──
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

# 三组配色（Nature 高对比）
C_CTRL = "#2E75B6"   # 蓝 Control
C_MODEL = "#C0392B"  # 红 Model
C_XNP   = "#27AE60"   # 绿 XNP

TABLE_DIR = Path(r"E:/XNP论文初稿/01_表格_三线表")
OUT_DIR   = Path(r"E:/XNP论文初稿/05_图件")

GROUP_ORDER = ["Control", "Model", "XNP"]


# 所有文本列都翻译（含 key 列），fig 函数改用翻译后的英文值筛选
_TEXT_COLS = {"table", "comparison", "note", "class", "function",
              "direction", "pathway", "genus", "metabolite", "protein", "name",
              "细胞类型", "神经递质系统", "因子", "几何分类", "类别"}


def _read_table(name: str) -> pd.DataFrame:
    """安全读取三线表：处理代谢物名含逗号、na/ns 字符串等脏数据，自动数值化"""
    import csv
    path = TABLE_DIR / name
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        ncol = len(header)
        for r in reader:
            if len(r) == ncol:
                rows.append(r)
            elif len(r) > ncol:
                # 首列（metabolite）含逗号：左边多出部分合并回首列
                extra = len(r) - ncol
                merged = ",".join(r[:extra + 1])
                rows.append([merged] + r[extra + 1:])
            # len < ncol 的行跳过（注脚）
    df = pd.DataFrame(rows, columns=header)
    # 各列：先清洗 na/ns/nan → 再尝试数值化；文本列做中英翻译
    for c in df.columns:
        col = df[c].astype(str)
        col = col.str.replace("na", "", regex=False).str.replace("ns", "", regex=False)
        col = col.replace("", np.nan)
        coerced = pd.to_numeric(col, errors="coerce")
        if coerced.notna().sum() > 0 and coerced.notna().sum() >= col.notna().sum() * 0.5:
            df[c] = coerced
        else:
            # 文本列：中英翻译
            if c in _TEXT_COLS:
                df[c] = col.apply(_zh2en)
            else:
                df[c] = col
    return df


# 中文术语 → 英文映射（覆盖所有组学表出现的术语）
_ZH2EN = [
    ("鞘脂", "Sphingolipid"), ("芳香族", "Aromatic"), ("单糖", "Monosaccharide"),
    ("双糖", "Disaccharide"), ("二羧酸", "Dicarboxylic acid"), ("有机酸", "Organic acid"),
    ("次级胆汁酸", "Secondary bile acid"), ("胆汁酸", "Bile acid"), ("胆汁酸偶联", "Bile acid conjugate"),
    ("前列腺素", "Prostaglandin"), ("色氨酸代谢", "Tryptophan metabolism"), ("色氨酸", "Tryptophan"),
    ("酪氨酸", "Tyrosine"), ("苯丙氨酸", "Phenylalanine"), ("芳香族氨基酸", "Aromatic AA"),
    ("芳香族酯", "Aromatic ester"), ("芳香族代谢物", "Aromatic metabolite"), ("邻苯二甲酸酯", "Phthalate"),
    ("gamma-谷氨酰肽", "Gamma-glutamyl peptide"), ("PUFA_AA", "PUFA/AA"), ("AA衍生物", "AA derivative"),
    ("脂肪酸", "Fatty acid"), ("酰基肉碱", "Acylcarnitine"), ("氨基酸_神经递质", "AA/neurotransmitter"),
    ("糖酵解", "Glycolysis"), ("B3_NAD+", "B3/NAD+"), ("未知", "Unknown"),
    ("脂氧素SPM", "Lipoxin/SPM"), ("脂氧素", "Lipoxin"), ("类花生酸", "Eicosanoid"),
    ("GABA转运体", "GABA transporter"), ("突触囊泡", "Synaptic vesicle"), ("突触可塑性", "Synaptic plasticity"),
    ("GPCR脱敏", "GPCR desensitization"), ("tRNA修饰", "tRNA modification"), ("细胞周期", "Cell cycle"),
    ("PKA锚定", "PKA anchor"), ("染色质重塑", "Chromatin remodeling"), ("NF-kB", "NF-kB"),
    ("APP代谢", "APP metabolism"), ("E3泛素连接酶_炎症", "E3 ubiquitin ligase/inflammation"),
    ("转录_复制", "Transcription/replication"), ("抗铁死亡", "Anti-ferroptosis"), ("基因沉默", "Gene silencing"),
    ("SNARE_突触", "SNARE/synapse"), ("铁代谢/铁调素调控（睡眠剥夺下降、XNP恢复）", "Iron metabolism (SD↓, XNP recovery)"),
    ("脂质运载受体/髓鞘形成", "Lipid receptor/myelination"), ("轴突导向/突触可塑性", "Axon guidance/synaptic plasticity"),
    ("V型胶原/血管-神经单元", "Collagen V/vascular-neural unit"), ("突触蛋白聚糖/突触黏附", "Synaptic proteoglycan/adhesion"),
    ("条件致病菌", "Opportunistic pathogen"), ("SCFA菌", "SCFA-producing"), ("益生菌耗竭87%", "Probiotic depleted 87%"),
    ("SD富集47倍", "SD enriched 47×"), ("恢复标志_LEfSe_LDA3.47_DESeq2_q5.8e-4_edgeR_q6.4e-3", "Recovery marker (LEfSe LDA3.47)"),
    ("接近阈值", "Near threshold"), ("XNP富集", "XNP enriched"), ("XNP恢复", "XNP recovery"),
    ("无显著差异", "No significant diff"), ("测序深度无偏倚", "Unbiased sequencing depth"),
    ("3-method_consensus", "3-method consensus"), ("6-method", "6-method"),
    ("SD上调", "SD up"), ("SD下调", "SD down"), ("XNP上调", "XNP up"), ("XNP下调", "XNP down"),
    ("XNP上调_最显著", "XNP up (top)"), ("XNP下调_最强", "XNP down (strongest)"),
    ("MC-only(SD改变,XNP未恢复)", "MC-only (SD change, XNP no recovery)"),
    ("G2_XNP_specific(仅XNP改变)", "G2 XNP-specific (XNP-only change)"),
    # 细胞类型/神经递质系统完整映射（key 列，须提前于词根）
    ("兴奋性神经元", "Excitatory neuron"), ("少突胶质细胞", "Oligodendrocyte"),
    ("GABA能神经元", "GABAergic neuron"), ("星形胶质细胞", "Astrocyte"),
    ("小胶质细胞", "Microglia"), ("少突胶质前体细胞", "Oligodendrocyte precursor"),
    ("内皮细胞", "Endothelial cell"), ("室管膜细胞", "Ependymal cell"), ("B细胞", "B cell"),
    ("谷氨酸", "Glutamate"), ("5-HT", "Serotonin"), ("多巴胺", "Dopamine"),
    ("乙酰胆碱", "Acetylcholine"), ("去甲肾上腺素", "Norepinephrine"),
    ("食欲素/下丘脑分泌素", "Orexin/hypocretin"), ("褪黑素/生物钟", "Melatonin/circadian"),
    ("Factor1", "Factor1"), ("Factor2", "Factor2"), ("Factor3", "Factor3"),
    ("Factor4", "Factor4"), ("Factor5", "Factor5"),
    # 词根兜底（覆盖剩余单字/复合词）
    ("完全", "fully"), ("部分", "partial"), ("显著", "significant"), ("最", "most"),
    ("上调", "up"), ("下调", "down"), ("改变", "change"), ("恢复", "recovery"),
    ("富集", "enriched"), ("耗竭", "depleted"), ("重塑", "remodeling"), ("菌群", "microbiome"),
    ("脑", "brain"), ("血清", "serum"), ("粪便", "fecal"), ("细胞", "cell"), ("神经", "neuro"),
    ("突触", "synaptic"), ("胶质", "glial"), ("神经元", "neuron"), ("小胶质", "microglia"),
    ("少突", "oligodendro"), ("星形", "astro"), ("内皮", "endothelial"), ("上皮", "epithelial"),
    ("脂肪", "lipid"), ("代谢", "metabolism"), ("蛋白", "protein"), ("基因", "gene"),
    ("表达", "expression"), ("差异", "differential"), ("标志", "marker"), ("信号", "signaling"),
    ("通路", "pathway"), ("因子", "factor"), ("受体", "receptor"), ("配体", "ligand"),
    ("酶", "enzyme"), ("激酶", "kinase"), ("磷酸", "phospho"), ("糖", "sugar"), ("糖酵解", "glycolysis"),
    ("氧化", "oxidation"), ("还原", "reduction"), ("炎症", "inflammation"), ("免疫", "immune"),
    ("铁死亡", "ferroptosis"), ("凋亡", "apoptosis"), ("自噬", "autophagy"), ("增殖", "proliferation"),
    ("分化", "differentiation"), ("迁移", "migration"), ("轴突", "axon"), ("树突", "dendrite"),
    ("髓鞘", "myelin"), ("血管", "vascular"), ("单元", "unit"), ("胶原", "collagen"),
    ("氨基", "amino"), ("羟基", "hydroxy"), ("羧酸", "carboxylic acid"), ("醇", "alcohol"),
    ("酸", "acid"), ("酯", "ester"), ("胺", "amine"), ("肽", "peptide"), ("素", "factor"),
    ("碱", "base"), ("盐", "salt"), ("类", "class"), ("型", "type"), ("种", "species"),
    ("属", "genus"), ("科", "family"), ("菌", "bacteria"), ("株", "strain"),
    ("上", "upper"), ("下", "lower"), ("高", "high"), ("低", "low"), ("多", "multi"),
    ("单", "mono"), ("双", "di"), ("三", "tri"), ("前", "pre"), ("后", "post"),
    ("中", "mid"), ("外", "outer"), ("内", "inner"), ("主", "main"), ("次", "secondary"),
    ("总", "total"), ("平", "level"), ("平性", "property"), ("性", "property"),
    ("物", "substance"), ("生", "bio"), ("甲", "methyl"), ("乙", "ethyl"), ("丙", "propyl"),
    ("丁", "butyl"), ("脂", "lipid"), ("能", "energy"), ("联", "co"), ("突", "spike"),
    ("细", "cell"), ("经", "tract"), ("肾", "renal"), ("胆", "bile"), ("胞", "cyte"),
    ("胶", "glial"), ("髓", "medulla"), ("脑", "brain"),
]


def _zh2en(s: str) -> str:
    if not isinstance(s, str):
        return s
    for zh, en in _ZH2EN:
        if zh in s:
            s = s.replace(zh, en)
    # 兜底：移除任何残留 CJK 字符（Nature 图禁止中文，避免 tofu 方块）
    import re as _re
    s = _re.sub(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", "", s)
    s = s.replace("（）", "()").replace("，", ", ").replace("；", "; ").replace("、", ", ")
    s = _re.sub(r"\s+", " ", s).strip()
    return s


def _save_multi(base: Path, fig: plt.Figure):
    """输出 SVG/PDF/PNG300/TIFF600 四格式"""
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), bbox_inches="tight", dpi=300)
    fig.savefig(base.with_suffix(".tiff"), bbox_inches="tight", dpi=600)
    plt.close(fig)


def _panel_grid(nrows=2, ncols=4, figsize=(16, 8)):
    """创建 8 面板网格，返回 (fig, axes.flatten())"""
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten()
    return fig, axes


def _annotate_sig(ax, x, y, p):
    """显著性星号"""
    if pd.isna(p):
        return
    if p < 0.001:
        s = "***"
    elif p < 0.01:
        s = "**"
    elif p < 0.05:
        s = "*"
    else:
        s = "ns"
    ax.text(x, y, s, ha="center", va="bottom", fontsize=7, fontweight="bold")


# ═══════════════════════════════════════════════════════════
# Fig1 — 睡眠表型（表S1）
# ═══════════════════════════════════════════════════════════
def fig1_sleep(base: Path) -> Dict:
    df = _read_table("表S1_睡眠表型.csv")
    fig, ax = _panel_grid()
    panels = {
        "睡眠时长 (min)": ("睡眠时长_min", "global_p"),
        "入睡潜伏期 (s)": ("入睡潜伏期_s", "global_p"),
        "测序深度覆盖率 (%)": ("Goods_coverage_pct", "global_p"),
    }
    # 8 面板：3 指标 × 分组柱状 + 3 指标恢复度 + KW 汇总 + 说明
    metrics = ["睡眠时长_min", "入睡潜伏期_s", "Goods_coverage_pct"]
    titles = ["Sleep duration (min)", "Sleep latency (s)", "Sequencing coverage (%)"]
    # 每个指标两个面板：分组柱状图 + 恢复度折线
    for i, (m, t) in enumerate(zip(metrics, titles)):
        row = df[df["index"] == m].iloc[0]
        vals = [row["control_median"], row["model_median"], row["xnp_median"]]
        # 面板 2i: 分组柱状
        ax[2*i].bar(GROUP_ORDER, vals, color=[C_CTRL, C_MODEL, C_XNP])
        ax[2*i].set_title(t, fontsize=9)
        ax[2*i].set_xticks(range(3)); ax[2*i].set_xticklabels(GROUP_ORDER, rotation=30)
        _annotate_sig(ax[2*i], 1, max(vals)*1.02, row["global_p"])
        ax[2*i].text(0.02, 0.95, f"KW p={row['global_p']:.3f}", transform=ax[2*i].transAxes, fontsize=6, va="top")
        # 面板 2i+1: 恢复度（相对 Control %）
        rec = [100, vals[1]/vals[0]*100, vals[2]/vals[0]*100]
        ax[2*i+1].plot(GROUP_ORDER, rec, "o-", color=C_XNP, linewidth=1.5)
        ax[2*i+1].axhline(100, color="grey", linestyle="--", linewidth=0.6)
        ax[2*i+1].set_title(f"{t}\n% of Control", fontsize=9)
        ax[2*i+1].set_ylim(0, max(rec)*1.2)
        ax[2*i+1].set_xticks(range(3)); ax[2*i+1].set_xticklabels(GROUP_ORDER, rotation=30)
        for j, v in enumerate(rec):
            ax[2*i+1].text(j, v+2, f"{v:.0f}%", ha="center", fontsize=6)
    # 面板 7: KW 汇总条形（各指标 -log10 p）
    neglog = [-np.log10(row["global_p"]) for m in metrics]
    ax[6].bar(titles, neglog, color=C_CTRL)
    ax[6].set_title("-log10(KW p)", fontsize=9)
    ax[6].set_ylabel("-log10 p")
    for j, v in enumerate(neglog):
        ax[6].text(j, v+0.05, f"{v:.1f}", ha="center", fontsize=6)
    ax[6].tick_params(axis="x", rotation=30)
    # 面板 8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• Sleep duration: 36→22→41 min (Control→Model→XNP)",
        "  KW p=0.0059, XNP fully recovers (p=0.63 vs Ctrl)",
        "• Sleep latency: no significant change (p=0.715)",
        "• Sequencing depth: unbiased (p=0.097)",
        "• 3-group Kruskal-Wallis; *p<0.05 **p<0.01 ***p<0.001",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.80-k*0.16, n, fontsize=7, va="top", family="DejaVu Sans")
    fig.suptitle("Figure 1. Sleep phenotype across three groups", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S1_睡眠表型.csv"}


# ═══════════════════════════════════════════════════════════
# Fig2 — 16S 菌群（表S2/S3 + 表S15）
# ═══════════════════════════════════════════════════════════
def fig2_microbiome(base: Path) -> Dict:
    df = _read_table("表S2_S3_16S差异菌.csv")
    df15 = _read_table("表S15_16S六方法共识差异菌.csv")
    fig, ax = _panel_grid()
    # 面板1: M-C 差异属火山（log2FC vs -log10 p）
    mc = df[df["comparison"] == "M-C"].copy()
    ax[0].scatter(mc["log2FC"], -np.log10(mc["p_value"]), c=C_MODEL, s=40)
    ax[0].axvline(0, color="grey", lw=0.6)
    ax[0].set_title("Model vs Control\n(volcano)", fontsize=9)
    ax[0].set_xlabel("log2FC"); ax[0].set_ylabel("-log10 p")
    for _, r in mc.iterrows():
        if abs(r["log2FC"]) > 2:
            ax[0].annotate(r["genus"][:12], (r["log2FC"], -np.log10(r["p_value"])), fontsize=5)
    # 面板2: X-M 差异属火山
    xm = df[df["comparison"] == "X-M"].copy()
    ax[1].scatter(xm["log2FC"], -np.log10(xm["p_value"]), c=C_XNP, s=40)
    ax[1].axvline(0, color="grey", lw=0.6)
    ax[1].set_title("XNP vs Model\n(volcano)", fontsize=9)
    ax[1].set_xlabel("log2FC"); ax[1].set_ylabel("-log10 p")
    # 面板3: M-C 差异属柱状（log2FC 排序）
    mc_s = mc.sort_values("log2FC")
    colors = [C_MODEL if v < 0 else C_CTRL for v in mc_s["log2FC"]]
    ax[2].barh(mc_s["genus"], mc_s["log2FC"], color=colors)
    ax[2].set_title("M-C genus log2FC", fontsize=9)
    ax[2].tick_params(axis="y", labelsize=5)
    # 面板4: X-M 差异属柱状
    xm_s = xm.sort_values("log2FC")
    colors = [C_MODEL if v < 0 else C_XNP for v in xm_s["log2FC"]]
    ax[3].barh(xm_s["genus"], xm_s["log2FC"], color=colors)
    ax[3].set_title("X-M genus log2FC", fontsize=9)
    ax[3].tick_params(axis="y", labelsize=5)
    # 面板5: 六方法共识（表S15）按 tier 柱状
    tiers = df15.groupby("几何分类")["属"].count()
    ax[4].bar(range(len(tiers)), tiers.values, color=C_CTRL)
    ax[4].set_xticks(range(len(tiers)))
    ax[4].set_xticklabels([t[:14] for t in tiers.index], rotation=30, ha="right", fontsize=5)
    ax[4].set_title("6-method consensus\n(genus count by class)", fontsize=9)
    # 面板6: 恢复标志 Turicimonas 突出
    rec = df15[df15["几何分类"].str.contains("XNP_specific", na=False)]
    ax[5].bar(rec["属"], rec["XM_LFC"], color=C_XNP)
    ax[5].set_title("XNP-specific remodeling\n(X-M log2FC)", fontsize=9)
    ax[5].tick_params(axis="x", rotation=45, labelsize=5)
    # 面板7: 方法数分布（MC_n_sig vs XM_n_sig）
    sig_cols = ["MC_n_sig", "XM_n_sig"]
    avail = df15[sig_cols].fillna(0)
    ax[6].bar(["M-C", "X-M"], [avail["MC_n_sig"].sum(), avail["XM_n_sig"].sum()], color=[C_MODEL, C_XNP])
    ax[6].set_title("Total significant\n(method-count sum)", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• Remodeling, NOT recovery (per 6-method consensus)",
        "• M-C: Prevotellaceae_NK3B31 +5.57 (47×), Bifido -2.83",
        "• X-M: Turicimonas +2.13 (recovery marker), SCFA↓",
        "• 9 genera X-M, 4 genera M-C (3-method consensus)",
        "• ANCOM-BC2-level rigor via 6 methods (Nearing 2022)",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 2. Gut microbiome remodeling (16S rRNA)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S2_S3_16S差异菌.csv + 表S15"}


# ═══════════════════════════════════════════════════════════
# Fig3 — 粪便代谢（表S4）
# ═══════════════════════════════════════════════════════════
def fig3_fecal_metabo(base: Path) -> Dict:
    df = _read_table("表S4_粪便代谢差异物.csv")
    fig, ax = _panel_grid()
    # 面板1: 全部差异物火山（log2FC 用 VIP 近似方向，用 p 着色）
    df["neglog"] = -np.log10(df["p_value"].astype(float))
    ax[0].scatter(df["VIP"], df["neglog"], c=df["q_value"].astype(float), cmap="viridis_r", s=40)
    ax[0].set_title("All metabolites\n(VIP vs -log10 p)", fontsize=9)
    ax[0].set_xlabel("VIP"); ax[0].set_ylabel("-log10 p")
    # 面板2: 类别分布柱状
    classes = df["class"].value_counts()
    ax[1].bar(range(len(classes)), classes.values, color=C_CTRL)
    ax[1].set_xticks(range(len(classes)))
    ax[1].set_xticklabels(classes.index, rotation=30, ha="right", fontsize=5)
    ax[1].set_title("Metabolite classes", fontsize=9)
    # 面板3: 脂氧素 SPM 聚焦
    spm = df[df["class"].str.contains("SPM|Lipoxin", na=False)]
    ax[2].bar(spm["metabolite"], -np.log10(spm["p_value"].astype(float)), color=C_XNP)
    ax[2].set_title("Lipoxin/SPM\n(-log10 p)", fontsize=9)
    ax[2].tick_params(axis="x", rotation=45, labelsize=5)
    # 面板4: 胆汁酸聚焦
    ba = df[df["class"].str.contains("Bile acid", na=False)]
    ax[3].bar(ba["metabolite"], -np.log10(ba["p_value"].astype(float)), color=C_MODEL)
    ax[3].set_title("Bile acids\n(-log10 p)", fontsize=9)
    ax[3].tick_params(axis="x", rotation=45, labelsize=5)
    # 面板5: VIP 排序 top10
    top = df.sort_values("VIP", ascending=False).head(10)
    ax[4].barh(top["metabolite"], top["VIP"], color=C_CTRL)
    ax[4].set_title("Top VIP metabolites", fontsize=9)
    ax[4].tick_params(axis="y", labelsize=5)
    # 面板6: q_value 排序
    qv = df.sort_values("q_value").head(10)
    ax[5].barh(qv["metabolite"], qv["q_value"].astype(float), color=C_XNP)
    ax[5].set_title("Top q-value (FDR)", fontsize=9)
    ax[5].tick_params(axis="y", labelsize=5)
    # 面板7: 比较组分布（X-M / M-C / X-C）
    comp = df["comparison"].value_counts()
    ax[6].bar(range(len(comp)), comp.values, color=C_MODEL)
    ax[6].set_xticks(range(len(comp))); ax[6].set_xticklabels(comp.index, fontsize=6)
    ax[6].set_title("By comparison", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• 15-Epi-lipoxin B5: q=0.043 (SPM resolution)",
        "• Bile acids remodeled (Avicholate, 3 secondary)",
        "• Aromatic esters: Phenethyl phenylacetate 1.1e-5",
        "• Lipidomic shift toward resolution mediators",
        "• Mostly X-M (XNP-specific) changes",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 3. Fecal metabolome (LC-MS)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S4_粪便代谢差异物.csv"}


# ═══════════════════════════════════════════════════════════
# Fig4 — 血清代谢（表S5）
# ═══════════════════════════════════════════════════════════
def fig4_serum_metabo(base: Path) -> Dict:
    df = _read_table("表S5_血清代谢差异物.csv")
    fig, ax = _panel_grid()
    df["neglog"] = -np.log10(df["p_value"].astype(float))
    # 面板1: 鞘脂家族
    sph = df[df["class"].str.contains("Sphingolipid", na=False)]
    ax[0].bar(range(len(sph)), sph["neglog"], color=C_MODEL)
    ax[0].set_xticks(range(len(sph))); ax[0].set_xticklabels(sph["metabolite"], rotation=45, fontsize=5)
    ax[0].set_title("Sphingolipids\n(-log10 p)", fontsize=9)
    # 面板2: 单糖面板
    sug = df[df["class"].str.contains("Monosaccharide", na=False)]
    ax[1].bar(range(len(sug)), sug["neglog"], color=C_XNP)
    ax[1].set_xticks(range(len(sug))); ax[1].set_xticklabels(sug["metabolite"], rotation=45, fontsize=5)
    ax[1].set_title("Monosaccharides\n(-log10 p)", fontsize=9)
    # 面板3: 芳香族氨基酸
    aa = df[df["class"].str.contains("Aromatic|AA", na=False)]
    ax[2].bar(range(len(aa)), aa["neglog"], color=C_CTRL)
    ax[2].set_xticks(range(len(aa))); ax[2].set_xticklabels(aa["metabolite"], rotation=45, fontsize=5)
    ax[2].set_title("Aromatic AAs\n(-log10 p)", fontsize=9)
    # 面板4: AA 衍生物（类花生酸）
    aa2 = df[df["class"].str.contains("AA|Eicosanoid", na=False)]
    ax[3].bar(range(len(aa2)), aa2["neglog"], color="#E67E22")
    ax[3].set_xticks(range(len(aa2))); ax[3].set_xticklabels(aa2["metabolite"], rotation=45, fontsize=5)
    ax[3].set_title("AA derivatives\n(-log10 p)", fontsize=9)
    # 面板5: -log10 p 排序（表S5 无 VIP 列）
    top = df.sort_values("neglog", ascending=False).head(10)
    ax[4].barh(top["metabolite"], top["neglog"], color=C_CTRL)
    ax[4].set_title("Top -log10 p", fontsize=9); ax[4].tick_params(axis="y", labelsize=5)
    # 面板6: q_value 排序
    qv = df.sort_values("q_value").head(10)
    ax[5].barh(qv["metabolite"], qv["q_value"].astype(float), color=C_XNP)
    ax[5].set_title("Top q-value", fontsize=9); ax[5].tick_params(axis="y", labelsize=5)
    # 面板7: 类别分布
    cls = df["class"].value_counts()
    ax[6].bar(range(len(cls)), cls.values, color=C_MODEL)
    ax[6].set_xticks(range(len(cls))); ax[6].set_xticklabels(cls.index, rotation=30, ha="right", fontsize=5)
    ax[6].set_title("Classes", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• Hexadecasphinganine: p=4.4e-9 (sphingolipid core)",
        "• Monosaccharides (Fructose/Galactose) X-M restored",
        "• Tyrosine/Trp: aromatic AA axis",
        "• 15HpETrE (AA deriv): pro-resolving lipid",
        "• Serum = main metabolic hub (MOFA Factor3)",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 4. Serum metabolome (LC-MS)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S5_血清代谢差异物.csv"}


# ═══════════════════════════════════════════════════════════
# Fig5 — 脑代谢（表S6）
# ═══════════════════════════════════════════════════════════
def fig5_brain_metabo(base: Path) -> Dict:
    df = _read_table("表S6_脑代谢差异物.csv")
    fig, ax = _panel_grid()
    df["neglog"] = -np.log10(df["p_value"].astype(float))
    # 面板1: 鞘脂家族
    sph = df[df["class"].str.contains("Sphingolipid", na=False)]
    ax[0].bar(range(len(sph)), sph["neglog"], color=C_MODEL)
    ax[0].set_xticks(range(len(sph))); ax[0].set_xticklabels(sph["metabolite"], rotation=45, fontsize=5)
    ax[0].set_title("Brain sphingolipids\n(-log10 p)", fontsize=9)
    # 面板2: 芳香族代谢物
    aro = df[df["class"].str.contains("芳香", na=False)]
    ax[1].bar(range(len(aro)), aro["neglog"], color=C_CTRL)
    ax[1].set_xticks(range(len(aro))); ax[1].set_xticklabels(aro["metabolite"], rotation=45, fontsize=5)
    ax[1].set_title("Aromatic metabolites\n(-log10 p)", fontsize=9)
    # 面板3: 酰基肉碱
    ac = df[df["class"].str.contains("Acylcarnitine", na=False)]
    ax[2].bar(range(len(ac)), ac["neglog"], color=C_XNP)
    ax[2].set_xticks(range(len(ac))); ax[2].set_xticklabels(ac["metabolite"], rotation=45, fontsize=5)
    ax[2].set_title("Acylcarnitine\n(-log10 p)", fontsize=9)
    # 面板4: 糖酵解/脂肪酸
    gf = df[df["class"].str.contains("Glycolysis|Fatty acid", na=False)]
    ax[3].bar(range(len(gf)), gf["neglog"], color="#E67E22")
    ax[3].set_xticks(range(len(gf))); ax[3].set_xticklabels(gf["metabolite"], rotation=45, fontsize=5)
    ax[3].set_title("Glycolysis/FA\n(-log10 p)", fontsize=9)
    # 面板5: VIP 排序
    top = df.sort_values("VIP", ascending=False).head(10)
    ax[4].barh(top["metabolite"], top["VIP"], color=C_CTRL)
    ax[4].set_title("Top VIP", fontsize=9); ax[4].tick_params(axis="y", labelsize=5)
    # 面板6: NAD+ / B3
    nad = df[df["class"].str.contains("NAD|B3", na=False)]
    if len(nad):
        ax[5].bar(nad["metabolite"], nad["neglog"], color="#9B59B6")
        ax[5].set_xticklabels(nad["metabolite"], rotation=45, fontsize=5)
    ax[5].set_title("NAD+/B3", fontsize=9)
    # 面板7: 类别分布
    cls = df["class"].value_counts()
    ax[6].bar(range(len(cls)), cls.values, color=C_MODEL)
    ax[6].set_xticks(range(len(cls))); ax[6].set_xticklabels(cls.index, rotation=30, ha="right", fontsize=5)
    ax[6].set_title("Classes", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• HPLA (hydroxyphenyllactic acid): aromatic, M-C",
        "• Sphinganine/Phytosphingosine: sphingolipid family",
        "• Arachidonoylcarnitine: FAO-linked acylcarnitine",
        "• Lactate: glycolysis shift",
        "• Brain layer converges w/ serum sphingolipid axis",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 5. Brain metabolome (LC-MS)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S6_脑代谢差异物.csv"}


# ═══════════════════════════════════════════════════════════
# Fig6 — 血清蛋白 GSEA（表S7）
# ═══════════════════════════════════════════════════════════
def fig6_serum_protein_gsea(base: Path) -> Dict:
    df = _read_table("表S7_血清蛋白GSEA.csv")
    fig, ax = _panel_grid()
    # 面板1: M-C NES 排序
    mc = df[df["comparison"] == "M-C"]
    ax[0].barh(mc["pathway"], mc["NES"], color=[C_MODEL if v < 0 else C_CTRL for v in mc["NES"]])
    ax[0].set_title("M-C NES", fontsize=9); ax[0].tick_params(axis="y", labelsize=5)
    # 面板2: X-M NES 排序
    xm = df[df["comparison"] == "X-M"]
    ax[1].barh(xm["pathway"], xm["NES"], color=[C_MODEL if v < 0 else C_XNP for v in xm["NES"]])
    ax[1].set_title("X-M NES", fontsize=9); ax[1].tick_params(axis="y", labelsize=5)
    # 面板3: NES 全排序（按绝对值）
    alln = df.sort_values("NES", key=lambda s: s.abs(), ascending=False)
    ax[2].barh(alln["pathway"], alln["NES"], color=[C_MODEL if v < 0 else C_XNP for v in alln["NES"]])
    ax[2].set_title("All NES (|rank|)", fontsize=9); ax[2].tick_params(axis="y", labelsize=5)
    # 面板4: FDR 气泡（NES vs -log10 FDR）
    df["neglogFDR"] = -np.log10(df["FDR_q"].astype(float).replace(0, 1e-300))
    dir_color = {"SD上调": C_CTRL, "SD下调": C_MODEL, "XNP上调": C_XNP, "XNP下调": C_MODEL}
    cols = df["direction"].map(lambda d: dir_color.get(d, "#999999"))
    ax[3].scatter(df["NES"], df["neglogFDR"], s=40, c=cols, alpha=0.7)
    ax[3].set_title("NES vs -log10 FDR", fontsize=9)
    ax[3].set_xlabel("NES"); ax[3].set_ylabel("-log10 FDR")
    # 面板5: 方向分布
    direct = df["direction"].value_counts()
    ax[4].bar(range(len(direct)), direct.values, color=C_CTRL)
    ax[4].set_xticks(range(len(direct))); ax[4].set_xticklabels(direct.index, rotation=30, ha="right", fontsize=5)
    ax[4].set_title("Directions", fontsize=9)
    # 面板6: 显著通路 (FDR<0.1)
    sig = df[df["FDR_q"].astype(float) < 0.1]
    ax[5].barh(sig["pathway"], -np.log10(sig["FDR_q"].astype(float)), color=C_XNP)
    ax[5].set_title("Significant (FDR<0.1)", fontsize=9); ax[5].tick_params(axis="y", labelsize=5)
    # 面板7: 上下调数量
    up = (df["NES"] > 0).sum(); down = (df["NES"] < 0).sum()
    ax[6].bar(["Up", "Down"], [up, down], color=[C_XNP, C_MODEL])
    ax[6].set_title("Up/Down count", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• Ribosome: M-C up, X-M down (strongest)",
        "• Spliceosome: X-M up (p=0.0026) — recovery",
        "• Sphingolipid signaling: M-C down (resolution)",
        "• HIF-1/Glycolysis/Insulin/mTOR: M-C down",
        "• Serum proteome: ribosomal + splicing programs",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 6. Serum proteome GSEA", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S7_血清蛋白GSEA.csv"}


# ═══════════════════════════════════════════════════════════
# Fig7 — 脑蛋白差异（表S8）
# ═══════════════════════════════════════════════════════════
def fig7_brain_protein(base: Path) -> Dict:
    df = _read_table("表S8_脑蛋白差异.csv")
    # FC 列可能含 "1.53_1.61"（多比较）或 "na" → 取首值并转数值
    df["FC"] = df["FC"].astype(str).str.split("_").str[0].replace("na", np.nan)
    df["FC"] = pd.to_numeric(df["FC"], errors="coerce")
    df["pnum"] = pd.to_numeric(df["p_value"].astype(str).str.split("_").str[0], errors="coerce")
    fig, ax = _panel_grid()
    # 面板1: 突触/神经相关 FC
    syn = df[df["function"].str.contains("Synapt|Neuro|GABA|SNARE", na=False)]
    ax[0].barh(syn["protein"], syn["FC"].astype(float), color=[C_MODEL if v < 1 else C_XNP for v in syn["FC"].astype(float)])
    ax[0].axvline(1, color="grey", lw=0.6); ax[0].set_title("Synaptic/Neuronal", fontsize=9); ax[0].tick_params(axis="y", labelsize=5)
    # 面板2: 铁死亡/炎症
    infl = df[df["function"].str.contains("Ferroptosis|inflamm|NF-kB|ubiquitin", na=False)]
    ax[1].barh(infl["protein"], infl["FC"].astype(float), color=[C_MODEL if v < 1 else C_XNP for v in infl["FC"].astype(float)])
    ax[1].axvline(1, color="grey", lw=0.6); ax[1].set_title("Ferroptosis/Inflammation", fontsize=9); ax[1].tick_params(axis="y", labelsize=5)
    # 面板3: 染色质/周期
    chr_ = df[df["function"].str.contains("Chromatin|cycle|replication|Transcription", na=False)]
    ax[2].barh(chr_["protein"], chr_["FC"].astype(float), color=[C_MODEL if v < 1 else C_XNP for v in chr_["FC"].astype(float)])
    ax[2].axvline(1, color="grey", lw=0.6); ax[2].set_title("Chromatin/Cycle", fontsize=9); ax[2].tick_params(axis="y", labelsize=5)
    # 面板4: p-value 排序（top 显著）
    df["pnum"] = df["p_value"].astype(float)
    top = df.sort_values("pnum").head(10)
    ax[3].barh(top["protein"], -np.log10(top["pnum"]), color=C_CTRL)
    ax[3].set_title("Top significance", fontsize=9); ax[3].tick_params(axis="y", labelsize=5)
    # 面板5: FC 全排序
    df["fcnum"] = df["FC"].astype(float)
    allf = df.sort_values("fcnum", key=lambda s: s.abs(), ascending=False)
    ax[4].barh(allf["protein"], allf["fcnum"], color=[C_MODEL if v < 1 else C_XNP for v in allf["fcnum"]])
    ax[4].axvline(1, color="grey", lw=0.6); ax[4].set_title("All FC (|rank|)", fontsize=9); ax[4].tick_params(axis="y", labelsize=5)
    # 面板6: 功能分类计数
    cats = df["function"].apply(lambda s: s.split("/")[0][:10]).value_counts()
    ax[5].bar(range(len(cats)), cats.values, color=C_MODEL)
    ax[5].set_xticks(range(len(cats))); ax[5].set_xticklabels(cats.index, rotation=30, ha="right", fontsize=5)
    ax[5].set_title("Function categories", fontsize=9)
    # 面板7: 上调/下调
    up = (df["fcnum"] > 1).sum(); down = (df["fcnum"] < 1).sum()
    ax[6].bar(["Up", "Down"], [up, down], color=[C_XNP, C_MODEL])
    ax[6].set_title("Up/Down", fontsize=9)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• SLC7A14 (GABA transporter): down in X-M",
        "• Synaptotagmin-3 / CDK5 substrate: synaptic",
        "• FSP1: anti-ferroptosis (X-C up 1.42)",
        "• c-Rel / Pellino-1: neuroinflammation",
        "• Brain proteome: synaptic + ferroptosis axis",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.78-k*0.15, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 7. Brain proteome (differential)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S8_脑蛋白差异.csv"}


# ═══════════════════════════════════════════════════════════
# Fig8 — 单细胞（表S11/S12/S13 + MOFA S14）
# ═══════════════════════════════════════════════════════════
def fig8_scrna(base: Path) -> Dict:
    cell = _read_table("表S11_单细胞细胞比例.csv")
    rev = _read_table("表S12_单细胞逆转基因.csv")
    neuro = _read_table("表S13_单细胞神经递质系统.csv")
    mofa = _read_table("表S14_MOFA因子分析.csv")
    fig, ax = _panel_grid()
    # 面板1: 细胞比例分组柱状（兴奋性/少突/GABA）
    sel = cell[cell["细胞类型"].isin(["Excitatory neuron", "Oligodendrocyte", "GABAergic neuron"])]
    x = np.arange(len(sel)); w = 0.25
    ax[0].bar(x-w, sel["Control均值%"], w, label="Control", color=C_CTRL)
    ax[0].bar(x, sel["Model均值%"], w, label="Model", color=C_MODEL)
    ax[0].bar(x+w, sel["XNP均值%"], w, label="XNP", color=C_XNP)
    ax[0].set_xticks(x); ax[0].set_xticklabels(sel["细胞类型"], rotation=20, fontsize=5)
    ax[0].set_title("Major cell types (%)", fontsize=9); ax[0].legend(fontsize=5)
    # 面板2: 兴奋性神经元 3 组
    ex = cell[cell["细胞类型"] == "Excitatory neuron"].iloc[0]
    ax[1].bar(GROUP_ORDER, [ex["Control均值%"], ex["Model均值%"], ex["XNP均值%"]], color=[C_CTRL, C_MODEL, C_XNP])
    ax[1].set_title("Excitatory neuron", fontsize=9); ax[1].set_xticklabels(GROUP_ORDER, rotation=30, fontsize=6)
    # 面板3: 少突胶质 3 组
    ol = cell[cell["细胞类型"] == "Oligodendrocyte"].iloc[0]
    ax[2].bar(GROUP_ORDER, [ol["Control均值%"], ol["Model均值%"], ol["XNP均值%"]], color=[C_CTRL, C_MODEL, C_XNP])
    ax[2].set_title("Oligodendrocyte", fontsize=9); ax[2].set_xticklabels(GROUP_ORDER, rotation=30, fontsize=6)
    # 面板4: 逆转基因 MvC vs XvM 方向
    ax[3].scatter(rev["MvC_log2FC"], rev["XvM_log2FC"], c=C_XNP, s=50)
    ax[3].axhline(0, color="grey", lw=0.6); ax[3].axvline(0, color="grey", lw=0.6)
    ax[3].set_title("Reversed genes\n(MvC vs XvM)", fontsize=9)
    ax[3].set_xlabel("MvC log2FC"); ax[3].set_ylabel("XvM log2FC")
    for _, r in rev.iterrows():
        ax[3].annotate(r["基因"], (r["MvC_log2FC"], r["XvM_log2FC"]), fontsize=5)
    # 面板5: 神经递质系统（平均表达 3 组）
    systems = neuro["神经递质系统"].unique()
    for i, sys in enumerate(systems):
        sub = neuro[neuro["神经递质系统"] == sys]
        ax[4].plot(GROUP_ORDER, sub["平均表达"], "o-", label=sys[:8], linewidth=0.8, markersize=3)
    ax[4].set_title("Neurotransmitter systems", fontsize=9)
    ax[4].set_xticklabels(GROUP_ORDER, rotation=30, fontsize=6)
    ax[4].legend(fontsize=4, ncol=2)
    # 面板6: 神经递质表达细胞比例
    for i, sys in enumerate(systems):
        sub = neuro[neuro["神经递质系统"] == sys]
        ax[5].plot(GROUP_ORDER, sub["表达细胞比例%"], "s--", label=sys[:8], linewidth=0.8, markersize=3)
    ax[5].set_title("% cells expressing", fontsize=9)
    ax[5].set_xticklabels(GROUP_ORDER, rotation=30, fontsize=6)
    # 面板7: MOFA Factor3 分组（显著）
    f3 = mofa[mofa["因子"] == "Factor3"].iloc[0]
    ax[6].bar(GROUP_ORDER, [f3["Control均值"], f3["Model均值"], f3["XNP均值"]], color=[C_CTRL, C_MODEL, C_XNP])
    ax[6].set_title("MOFA Factor3\n(K p=0.0062)", fontsize=9); ax[6].set_xticklabels(GROUP_ORDER, rotation=30, fontsize=6)
    # 面板8: 说明
    ax[7].axis("off")
    ax[7].text(0.05, 0.95, "Key findings:", fontsize=9, fontweight="bold", va="top")
    notes = [
        "• Excitatory neuron 20.3→12.9% (X-M p=0.10)",
        "• Oligodendrocyte 43→53.6% (X-M p=0.10)",
        "• 5 reversed genes (Hfe/Lsr/Sema3d/Col5a2/Spock3)",
        "• 5-HT/Glu/ACh systems down in XNP",
        "• MOFA Factor3 separates groups (serum-driven)",
        "• Overall composition χ²=2283.73 p<0.001",
    ]
    for k, n in enumerate(notes):
        ax[7].text(0.05, 0.84-k*0.13, n, fontsize=6.5, va="top")
    fig.suptitle("Figure 8. Single-cell transcriptome (scRNA-seq)", fontsize=12, fontweight="bold")
    _save_multi(base, fig)
    return {"panels": 8, "source": "表S11/S12/S13 + 表S14_MOFA"}


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════
FIG_FUNCS = {
    "Fig1": fig1_sleep,
    "Fig2": fig2_microbiome,
    "Fig3": fig3_fecal_metabo,
    "Fig4": fig4_serum_metabo,
    "Fig5": fig5_brain_metabo,
    "Fig6": fig6_serum_protein_gsea,
    "Fig7": fig7_brain_protein,
    "Fig8": fig8_scrna,
}


def generate_all(out_dir: str = None) -> Dict[str, Dict]:
    out = Path(out_dir) if out_dir else OUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, func in FIG_FUNCS.items():
        base = out / name / f"{name}_multiomics"
        try:
            meta = func(base)
            meta["output_base"] = str(base)
            results[name] = meta
            print(f"✓ {name}: {meta['panels']} panels <- {meta['source']}")
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            import traceback; traceback.print_exc()
    # 汇总 JSON
    with open(out / "fig1_8_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    return results


if __name__ == "__main__":
    generate_all()
