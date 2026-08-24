#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig10 — 机制轴示意图（纯组学版）
L1 菌群重塑 → L2 血清代谢 → L3 粪便代谢 → L4 小胶质 → L5 OPC → L6 睡眠
Nature 风格：6.5pt / 183mm 宽 / SVG+PDF+TIFF600+PNG300
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd
import os

OUTDIR = r"E:\XNP论文初稿\02_论文\figures\Fig10"
SRC = r"E:\XNP论文初稿\02_论文\figures\Fig09_source_data"
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 7, "font.family": "Microsoft YaHei",
    "axes.unicode_minus": False,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})

# 配色
C_L1 = "#8E44AD"   # 菌群 紫
C_L2 = "#E07B39"   # 血清 橙
C_L3 = "#F39C12"   # 粪便 浅橙
C_L4 = "#3B6FA0"   # 小胶质 蓝
C_L5 = "#16A085"   # OPC 青
C_L6 = "#C0392B"   # 睡眠 红
C_G1 = "#3B6FA0"; C_G2 = "#E07B39"

# ── 6 节点定义（中文 + 关键统计值） ──
NODES = [
    ("L1\n菌群重塑", C_L1, "G2 9 属↑/↓\nMC-only 4 属未恢复\n(Turicimonas↑/Lachnospiraceae↓)\n6 方法共识≥4/6"),
    ("L2\n血清代谢", C_L2, "嘌呤池 5 E1 (G2)\n+ 吲哚 3 E1 (G1)\nMOFA Factor3 p=0.0062\n(IPA/4-HPPA/PS/单糖)"),
    ("L3\n粪便代谢", C_L3, "嘌呤池镜像↓\n腺苷 P=0.008\nAMP P=0.008\n(与血清反向)"),
    ("L4\n小胶质", C_L4, "Tgfbr1 FDR 0.045\nIl1rapl2 FDR 0.045\nTGFβ-嘌呤能程序\n(150k 核 scRNA)"),
    ("L5\nOPC", C_L5, "Il1rapl2 FDR 0.020\nSnhg11 FDR 0.020\n嘌呤能模块唯一显著\n(150k 核 scRNA)"),
    ("L6\n睡眠恢复", C_L6, "XNP 52.3 vs Model 18.0 min\n精确置换 P=0.0036\n全队列 padj=0.019"),
]
N = len(NODES)

fig = plt.figure(figsize=(7.6, 6.0))
ax = fig.add_subplot(111)
ax.set_xlim(0, 12); ax.set_ylim(0, 9)
ax.set_axis_off()

# 节点横向位置（X），Y 中心
ys = [6.2, 6.2, 6.2, 6.2, 6.2, 6.2]
xs = [0.5, 2.5, 4.5, 6.5, 8.5, 10.5]
W, H = 1.8, 1.2

for (title, color, detail), x, y in zip(NODES, xs, ys):
    # 圆角矩形节点
    box = FancyBboxPatch((x - W/2, y - H/2), W, H,
                         boxstyle="round,pad=0.05,rounding_size=0.15",
                         fc=color, ec="black", lw=0.6, alpha=0.92)
    ax.add_patch(box)
    ax.text(x, y + 0.42, title, ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    # 详情框（节点下方）
    det_box = FancyBboxPatch((x - 0.95, y - 2.3), 1.9, 1.7,
                            boxstyle="round,pad=0.04,rounding_size=0.1",
                            fc="white", ec=color, lw=0.5, alpha=0.95)
    ax.add_patch(det_box)
    ax.text(x, y - 1.45, detail, ha="center", va="center",
            fontsize=5.6, color="black", linespacing=1.25)

# 箭头连接
for i in range(N - 1):
    x0, x1 = xs[i] + W/2, xs[i+1] - W/2
    arr = FancyArrowPatch((x0, ys[i]), (x1, ys[i+1]),
                          arrowstyle="-|>", mutation_scale=14,
                          lw=1.2, color="#333333")
    ax.add_patch(arr)

# 顶部标题
ax.text(6, 8.3, "XNP 多组学机制轴：菌群重塑 → 嘌呤/吲哚 → 小胶质/OPC → 睡眠恢复",
        ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(6, 7.7, "(纯组学版 · n=6/组×3 bulk层 + 152,013 核 scRNA, 全部 FDR/精确置换统计)",
        ha="center", va="center", fontsize=6.5, color="#555555", style="italic")

# 底部证据标签
ax.text(0.5, 0.8, "G2 = XNP 特有", color=C_G2, fontsize=6.5, fontweight="bold")
ax.text(2.5, 0.8, "G1 = 真恢复", color=C_G1, fontsize=6.5, fontweight="bold")
ax.text(4.5, 0.8, "MC-only = SD 改 XNP 未复", color="#7F8C8D", fontsize=6.5, fontweight="bold")
ax.text(7.5, 0.8, "配体-受体同源 (嘌呤配体 + 小胶质/OPC 受体程序)",
        color="#333", fontsize=6.5, style="italic")
ax.text(0.5, 0.3, "诚实披露: 嘌呤池非睡眠中介 (臂内残差化 ρ=−0.159); 脑层 FDR 全零; 9 只 snRNA 为行为学极端子集",
        color="#7F0000", fontsize=5.8, style="italic")

# 保存
for ext, dpi in [("svg", None), ("pdf", None), ("tiff", 600), ("png", 300)]:
    fig.savefig(os.path.join(OUTDIR, f"Fig10_Mechanism_Axis.{ext}"),
                dpi=dpi, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Fig10 saved ->", OUTDIR)
