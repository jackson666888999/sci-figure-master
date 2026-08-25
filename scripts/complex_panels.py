# -*- coding: utf-8 -*-
"""
顶刊级复杂图型库（非柱状）
============================
为 mechanism-axis 7 层组学大图服务。每个 panel 函数签名：
    panel_xxx(ax, data, ..., title="")
只负责在传入的 ax 上作画（不 savefig），由 compose.py 统一导出 PDF+PNG@300dpi。

统一规范（Nature/Cell/Science）：
- 字体 Arial/Helvetica，8pt 基准
- 克制配色（CATEGORICAL_EXTENDED），禁用 matplotlib 默认
- 去 top/right spine，轴线 0.6pt
- 不用柱状图
"""
from __future__ import annotations
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, Circle, Wedge, Polygon
import matplotlib.path as mpath
from matplotlib.collections import LineCollection
import math

# ── 配色（academic-figure-skill Nature 变体）──────────────────────
CATEGORICAL = ["#08519C", "#A50F15", "#006D2C", "#D94801",
               "#54278F", "#525252", "#2171B5", "#CB181D",
               "#238B45", "#F16913", "#6A51A3", "#737373"]
DIVERGING = ["#08519C", "#F7F7F7", "#A50F15"]
GREY = "#999999"
INK = "#222222"
ACCENT = "#A50F15"

GROUP_COLORS = {
    "Control": "#08519C", "Model": "#A50F15", "XNP": "#006D2C",
    "XNE": "#D94801", "XNF": "#54278F",
}


def _rc(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.6)
    ax.spines["bottom"].set_linewidth(0.6)
    ax.tick_params(width=0.6, length=3, labelsize=7)
    ax.title.set_size(8.5)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontsize(7)


def sci_fmt(p):
    """p 值 → 科学计数文本"""
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "n.s."
    if p < 1e-4:
        return f"p<1e-4"
    return f"p={p:.1e}"


# ═══════════════════════════════════════════════════════════════
# 1. 弦图 Chord diagram
# ═══════════════════════════════════════════════════════════════
def panel_chord(ax, src_labels, tgt_labels, weights,
                src_colors=None, tgt_colors=None, title="Chord diagram",
                label_threshold=0.0):
    """权重矩阵：src(i) → tgt(j)。在圆环上左右排布两段弧，弦宽=权重。"""
    src_u = list(dict.fromkeys(src_labels))
    tgt_u = list(dict.fromkeys(tgt_labels))
    ns, nt = len(src_u), len(tgt_u)
    S = sum(weights) or 1.0
    # 归一化到弧度
    src_w = [sum(w for s, t, w in zip(src_labels, tgt_labels, weights) if s == u) for u in src_u]
    tgt_w = [sum(w for s, t, w in zip(src_labels, tgt_labels, weights) if t == u) for u in tgt_u]
    src_col = src_colors or [CATEGORICAL[i % len(CATEGORICAL)] for i in range(ns)]
    tgt_col = tgt_colors or [CATEGORICAL[(i + 3) % len(CATEGORICAL)] for i in range(nt)]

    gap = 0.04
    # 左半圆 src（π..2π），右半圆 tgt（0..π）
    def layout(labels, totals, base, direction):
        arcs = []
        tot = sum(totals) or 1
        ang = base
        for i, (lab, wt) in enumerate(zip(labels, totals)):
            sweep = (wt / tot) * (math.pi - gap) if direction > 0 else (wt / tot) * (math.pi - gap)
            a0, a1 = ang, ang + sweep
            arcs.append((a0, a1, lab, i))
            ang = a1 + gap / max(1, len(totals))
        return arcs

    arcs_s = layout(src_u, src_w, math.pi + gap / 2, +1)
    arcs_t = layout(tgt_u, tgt_w, gap / 2, +1)

    def arc_mid(a0, a1):
        return (a0 + a1) / 2

    # 画弧段
    R = 1.0
    for (a0, a1, lab, i) in arcs_s:
        ax.add_patch(Wedge((0, 0), R, math.degrees(a0), math.degrees(a1),
                           width=0.06, facecolor=src_col[i], edgecolor="none"))
        mid = arc_mid(a0, a1)
        ax.text(math.cos(mid) * 1.12, math.sin(mid) * 1.12, lab,
                ha="right" if math.cos(mid) < 0 else "left",
                va="center", fontsize=6.5, rotation=math.degrees(mid) - 90 if math.cos(mid) < 0 else math.degrees(mid) + 90,
                color=INK)
    for (a0, a1, lab, i) in arcs_t:
        ax.add_patch(Wedge((0, 0), R, math.degrees(a0), math.degrees(a1),
                           width=0.06, facecolor=tgt_col[i], edgecolor="none"))
        mid = arc_mid(a0, a1)
        ax.text(math.cos(mid) * 1.12, math.sin(mid) * 1.12, lab,
                ha="left" if math.cos(mid) > 0 else "right",
                va="center", fontsize=6.5,
                rotation=math.degrees(mid) + 90 if math.cos(mid) > 0 else math.degrees(mid) - 90,
                color=INK)

    # 画弦
    def pos_on_arc(arcs, idx, frac):
        a0, a1, _, i = arcs[idx]
        return a0 + (a1 - a0) * frac

    # 聚合 src->tgt 权重
    pair = {}
    for s, t, w in zip(src_labels, tgt_labels, weights):
        pair[(src_u.index(s), tgt_u.index(t))] = pair.get((src_u.index(s), tgt_u.index(t)), 0) + w
    # 每个 src/tgt 内部累计偏移
    s_off = [0.0] * ns
    t_off = [0.0] * nt
    order = sorted(pair.keys(), key=lambda k: (k[0], -pair[k]))
    for (si, ti) in order:
        w = pair[(si, ti)]
        sf = s_off[si] / (src_w[si] or 1)
        s_off[si] += w
        ef = s_off[si] / (src_w[si] or 1)
        tf = t_off[ti] / (tgt_w[ti] or 1)
        t_off[ti] += w
        gf = t_off[ti] / (tgt_w[ti] or 1)
        a_s0 = pos_on_arc(arcs_s, si, sf)
        a_s1 = pos_on_arc(arcs_s, si, ef)
        a_t0 = pos_on_arc(arcs_t, ti, tf)
        a_t1 = pos_on_arc(arcs_t, ti, gf)
        p0 = (math.cos(a_s0), math.sin(a_s0))
        p1 = (math.cos(a_s1), math.sin(a_s1))
        p2 = (math.cos(a_t1), math.sin(a_t1))
        p3 = (math.cos(a_t0), math.sin(a_t0))
        # 贝塞尔弦
        c0 = (0, 0)
        verts = [p0, (p0[0] * 0.4, p0[1] * 0.4), (p3[0] * 0.4, p3[1] * 0.4), p3,
                 p2, (p2[0] * 0.4, p2[1] * 0.4), (p1[0] * 0.4, p1[1] * 0.4), p1]
        codes = [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4,
                 mpath.Path.LINETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4]
        # 简化：两条三次贝塞尔
        path = mpath.Path([p0, (p0[0] * 0.3, p0[1] * 0.3),
                           (p3[0] * 0.3, p3[1] * 0.3), p3],
                          [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4])
        col = tgt_col[ti]
        ax.add_patch(patches.PathPatch(path, facecolor=col, edgecolor="none",
                                       alpha=0.28, lw=0))
        path2 = mpath.Path([p3, (p3[0] * 0.3, p3[1] * 0.3),
                            (p2[0] * 0.3, p2[1] * 0.3), p2],
                           [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4])
        ax.add_patch(patches.PathPatch(path2, facecolor=col, edgecolor="none",
                                       alpha=0.28, lw=0))
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 2. 多层环形树状图 Radial / circular dendrogram
# ═══════════════════════════════════════════════════════════════
def panel_circ_dendrogram(ax, Z, labels, title="Radial dendrogram",
                          leaf_colors=None, R_base=0.35):
    """
    Z: scipy.cluster.hierarchy.linkage 输出 (n-1 × 4)
    labels: 叶子标签 (n)
    在圆环上绘制层级聚类树（辐射状）
    """
    from scipy.cluster.hierarchy import linkage, leaves_list
    import numpy as np
    n = len(labels)
    if Z is None or (isinstance(Z, np.ndarray) and Z.size == 0):
        # 退化为叶子环
        Z = linkage(np.random.default_rng(0).random((n, 2)), method="average")
    # 计算叶子顺序
    order = list(leaves_list(Z))
    # 角度映射
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    leaf_ang = {i: ang[order.index(i)] for i in range(n)}
    # 节点角度（递归）
    node_ang = dict(leaf_ang)
    maxd = float(Z[:, 2].max()) if Z.size else 1.0
    R_leaf = R_base
    # 画叶子刻度 + 标签
    for i in range(n):
        a = leaf_ang[i]
        ax.plot([math.cos(a) * R_leaf, math.cos(a) * (R_leaf + 0.04)],
                [math.sin(a) * R_leaf, math.sin(a) * (R_leaf + 0.04)],
                color=leaf_colors[i] if leaf_colors else INK, lw=1.2)
        la = math.degrees(a)
        rot = la - 90 if math.cos(a) < 0 else la + 90
        ax.text(math.cos(a) * (R_leaf + 0.11), math.sin(a) * (R_leaf + 0.11),
                labels[i], ha="center", va="center", fontsize=5.2, rotation=rot, color=INK)

    def P(a, r):
        return (math.cos(a) * r, math.sin(a) * r)

    def arc_poly(a0, a1, r, nseg=24):
        aa = np.linspace(a0, a1, nseg)
        return [P(x, r) for x in aa]

    for k, row in enumerate(Z):
        i, j, d, _ = int(row[0]), int(row[1]), float(row[2]), int(row[3])
        a_i, a_j = node_ang[i], node_ang[j]
        a_mid = (a_i + a_j) / 2.0
        node_ang[n + k] = a_mid
        r = R_leaf + 0.04 + (d / (maxd or 1)) * (1.0 - R_leaf - 0.04)
        # 径向线
        ax.plot([P(a_i, R_leaf + 0.04), P(a_i, r)], color="#999999", lw=0.5)
        ax.plot([P(a_j, R_leaf + 0.04), P(a_j, r)], color="#999999", lw=0.5)
        # 弧
        seg = arc_poly(a_i, a_mid, r) + arc_poly(a_mid, a_j, r)[1:]
        xs = [p[0] for p in seg]; ys = [p[1] for p in seg]
        ax.plot(xs, ys, color="#777777", lw=0.6)
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 3. 桑基图 Sankey (轻量自实现)
# ═══════════════════════════════════════════════════════════════
def panel_sankey(ax, layers, flows, title="Sankey", colors=None):
    """
    layers: list of lists, 每层节点名  e.g. [['A','B'],['a1','a2','a3'],['x','y']]
    flows: list of (src_layer, src_node, tgt_layer, tgt_node, value)
    """
    nL = len(layers)
    xs = np.linspace(0.08, 0.92, nL)
    node_y = {}
    node_tot = {}
    for li, layer in enumerate(layers):
        for nd in layer:
            node_tot[(li, nd)] = 0.0
    for (sl, sn, tl, tn, v) in flows:
        node_tot[(sl, sn)] += v
        node_tot[(tl, tn)] += v
    # 分配纵向位置
    for li, layer in enumerate(layers):
        tot = sum(node_tot[(li, nd)] for nd in layer) or 1
        y = 0.05
        for nd in layer:
            h = (node_tot[(li, nd)] / tot) * 0.9
            node_y[(li, nd)] = (y, y + h)
            y += h + 0.02
    colmap = colors or {}
    # 画节点
    for (li, nd), (y0, y1) in node_y.items():
        c = colmap.get(nd, CATEGORICAL[hash(nd) % len(CATEGORICAL)])
        ax.add_patch(patches.Rectangle((xs[li] - 0.008, y0), 0.016, y1 - y0,
                                       facecolor=c, edgecolor="none"))
        ax.text(xs[li] + (0.012 if li < nL / 2 else -0.012), (y0 + y1) / 2,
                nd, ha="left" if li < nL / 2 else "right", va="center", fontsize=6, color=INK)
    # 画流（贝塞尔带）
    side = {}
    for (sl, sn, tl, tn, v) in flows:
        y0s, y1s = node_y[(sl, sn)]
        y0t, y1t = node_y[(tl, tn)]
        sh = (v / (node_tot[(sl, sn)] or 1)) * (y1s - y0s)
        th = (v / (node_tot[(tl, tn)] or 1)) * (y1t - y0t)
        key = (sl, sn)
        off = side.get(key, 0.0)
        side[key] = off + sh
        key2 = (tl, tn)
        off2 = side.get(key2, 0.0)
        side[key2] = off2 + th
        ya = y1s - off
        yb = y1t - off2
        c = colmap.get(sn, colmap.get(tn, GREY))
        ax.add_patch(patches.Polygon(
            [[xs[sl] + 0.008, ya], [xs[tl] - 0.008, yb],
             [xs[tl] - 0.008, yb - th], [xs[sl] + 0.008, ya - sh]],
            closed=True, facecolor=c, edgecolor="none", alpha=0.30))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 4. 网络图 Network / co-occurrence
# ═══════════════════════════════════════════════════════════════
def panel_network(ax, adj, node_labels, title="Network",
                  node_colors=None, node_sizes=None, edge_thresh=0.0):
    """
    adj: (n×n) 相关/权重矩阵（对称）
    node_labels: n
    """
    n = len(node_labels)
    np.fill_diagonal(adj, 0)
    # 弹簧布局（简单圆形+扰动）
    angles = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rng = np.random.default_rng(42)
    pos = {i: (math.cos(angles[i]) + rng.normal(0, 0.05),
               math.sin(angles[i]) + rng.normal(0, 0.05)) for i in range(n)}
    # 边
    for i in range(n):
        for j in range(i + 1, n):
            w = adj[i, j]
            if abs(w) >= edge_thresh and abs(w) > 1e-9:
                a, b = pos[i], pos[j]
                col = ACCENT if w > 0 else "#08519C"
                ax.plot([a[0], b[0]], [a[1], b[1]], color=col,
                        lw=0.4 + abs(w) * 2.0, alpha=0.35, zorder=1)
    # 节点
    for i in range(n):
        x, y = pos[i]
        sz = (node_sizes[i] if node_sizes else 60)
        ax.scatter(x, y, s=sz, c=node_colors[i] if node_colors else CATEGORICAL[i % len(CATEGORICAL)],
                   edgecolors="white", linewidths=0.6, zorder=2)
        ax.text(x, y, node_labels[i], fontsize=5.5, ha="center", va="center",
                color="white", zorder=3, fontweight="bold")
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 5. 旭日图 Sunburst (径向分层，非柱状)
# ═══════════════════════════════════════════════════════════════
def panel_sunburst(ax, hierarchy, title="Sunburst", colors=None):
    """
    hierarchy: 嵌套 dict  {name: value 或 {child: value}}
    径向扇形，逐层外扩
    """
    def flatten(node, depth=0, parent_frac=1.0, start=0.0):
        items = []
        if isinstance(node, dict):
            total = sum(v if not isinstance(v, dict) else sum(c if not isinstance(c, dict) else 1 for c in v.values()) for v in node.values())
            acc = start
            for k, v in node.items():
                if isinstance(v, dict):
                    sub_total = sum(c if not isinstance(c, dict) else 1 for c in v.values())
                    frac = (sub_total / total) * parent_frac
                    items.append((k, depth, acc, acc + frac, True))
                    items += flatten(v, depth + 1, frac, acc)
                    acc += frac
                else:
                    frac = (v / total) * parent_frac
                    items.append((k, depth, acc, acc + frac, False))
                    acc += frac
        return items

    segs = flatten(hierarchy)
    R0 = 0.3
    ring = 0.22
    colmap = colors or {}
    used = {}
    for (name, depth, a0, a1, is_parent) in segs:
        r_in = R0 + depth * ring
        r_out = r_in + ring * 0.92
        c = colmap.get(name, CATEGORICAL[hash(name) % len(CATEGORICAL)])
        ax.add_patch(Wedge((0, 0), r_out, math.degrees(a0 * 2 * math.pi),
                           math.degrees(a1 * 2 * math.pi), width=r_out - r_in,
                           facecolor=c, edgecolor="white", linewidth=0.5))
        if (a1 - a0) > 0.04:
            mid = (a0 + a1) * math.pi
            ax.text(math.cos(mid) * (r_in + r_out) / 2, math.sin(mid) * (r_in + r_out) / 2,
                    name[:10], ha="center", va="center", fontsize=5, color="white",
                    rotation=math.degrees(mid) - 90, fontweight="bold")
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 6. 山脊图 Ridgeline
# ═══════════════════════════════════════════════════════════════
def panel_ridge(ax, groups, values_list, title="Ridgeline", colors=None, xlabel=""):
    """
    groups: [str]; values_list: list of arrays（每组一个分布）
    """
    n = len(groups)
    col = colors or CATEGORICAL
    overlap = 0.55
    ymax = 1.0
    for i, (g, vals) in enumerate(zip(groups, values_list)):
        v = np.asarray(vals)
        v = v[np.isfinite(v)]
        if len(v) < 2:
            continue
        k = np.histogram(v, bins=30, density=True)[1]
        dens, edges = np.histogram(v, bins=30, density=True)
        x = (edges[:-1] + edges[1:]) / 2
        yoff = (n - 1 - i) * overlap
        ax.fill_between(x, yoff, yoff + dens / (dens.max() or 1) * ymax,
                        color=col[i % len(col)], alpha=0.55, lw=0)
        ax.plot(x, yoff + dens / (dens.max() or 1) * ymax, color=col[i % len(col)],
                lw=0.8)
        ax.text(x.min(), yoff + 0.02, g, fontsize=6.5, color=INK, va="bottom")
    ax.set_yticks([])
    ax.set_xlabel(xlabel, fontsize=7)
    _rc(ax)
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 7. 气泡富集图 Bubble / enrichment
# ═══════════════════════════════════════════════════════════════
def panel_bubble(ax, terms, sizes, pvals, title="Enrichment", colors=None,
                 x_labels=None, max_size=120):
    """
    terms: list of term names (y)
    sizes: list (气泡面积 ∝ 该值)
    pvals: list (颜色 ∝ -log10)
    x_labels: optional 列分组（多列气泡）
    """
    n = len(terms)
    if x_labels is None:
        x_labels = ["enrich"]
    xs = np.arange(len(x_labels))
    ypos = np.arange(n)[::-1]
    p_arr = -np.log10(np.array([max(p, 1e-300) for p in pvals]))
    pmax = p_arr.max() or 1
    s_arr = np.array(sizes)
    smax = s_arr.max() or 1
    cmap = plt.cm.Reds
    for yi, t in zip(ypos, terms):
        for xi in xs:
            idx = yi  # 简化：每 term 一行
            s = (s_arr[idx] / smax) * max_size
            c = cmap(p_arr[idx] / pmax)
            ax.scatter(xi, yi, s=s, c=[c], edgecolors="#888888", linewidths=0.4, alpha=0.85, zorder=3)
    ax.set_yticks(ypos); ax.set_yticklabels([t[:22] for t in terms], fontsize=6)
    ax.set_xticks(xs); ax.set_xticklabels(x_labels, fontsize=6.5)
    ax.set_xlim(-0.6, len(x_labels) - 0.4)
    ax.set_ylim(-0.8, n - 0.2)
    _rc(ax)
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)
    # 颜色条
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, pmax))
    sm.set_array([])
    cb = ax.figure.colorbar(sm, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("−log₁₀(p)", fontsize=6); cb.ax.tick_params(labelsize=5)


# ═══════════════════════════════════════════════════════════════
# 8. 雷达图 Radar
# ═══════════════════════════════════════════════════════════════
def panel_radar(ax, categories, series, title="Radar", colors=None):
    """
    categories: [str] (轴)
    series: dict {name: [vals 0..1]}  或 list of (name, vals)
    在普通笛卡尔 ax 上手绘雷达（兼容 compose 的常规 subplots）
    """
    n = len(categories)
    angles = np.linspace(0, 2 * math.pi, n, endpoint=False)
    for rr in [0.25, 0.5, 0.75, 1.0]:
        ax.plot(np.cos(angles) * rr, np.sin(angles) * rr, color="#dddddd", lw=0.4, zorder=0)
    for k, cat in enumerate(categories):
        a = angles[k]
        ax.plot([0, math.cos(a)], [0, math.sin(a)], color="#cccccc", lw=0.4, zorder=0)
        ax.text(math.cos(a) * 1.12, math.sin(a) * 1.12, cat, ha="center", va="center",
                fontsize=6, color=INK)
    col = colors or CATEGORICAL
    if isinstance(series, dict):
        series = list(series.items())
    for i, (name, vals) in enumerate(series):
        xs = [math.cos(angles[k]) * max(0.0, min(1.0, v)) for k, v in enumerate(vals)]
        ys = [math.sin(angles[k]) * max(0.0, min(1.0, v)) for k, v in enumerate(vals)]
        xs.append(xs[0]); ys.append(ys[0])
        ax.plot(xs, ys, color=col[i % len(col)], lw=1.0, label=name, zorder=2)
        ax.fill(xs, ys, color=col[i % len(col)], alpha=0.12, zorder=1)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 9. Circos 风格热图（环形矩阵）
# ═══════════════════════════════════════════════════════════════
def panel_circos_heatmap(ax, matrix, row_labels, col_labels=None, title="Circos heatmap",
                         cmap=plt.cm.RdBu_r, vmin=None, vmax=None):
    """
    matrix: (n×m) 在圆环上排成色块（行=径向，列=角向）
    """
    mat = np.asarray(matrix, dtype=float)
    nr, nc = mat.shape
    if col_labels is None:
        col_labels = row_labels
    a_edges = np.linspace(0, 2 * math.pi, nc + 1)
    r_in = 0.45
    r_out = 1.05
    vmin = mat.min() if vmin is None else vmin
    vmax = mat.max() if vmax is None else vmax
    norm = plt.Normalize(vmin, vmax)
    for ri in range(nr):
        r0 = r_in + (r_out - r_in) * ri / nr
        r1 = r_in + (r_out - r_in) * (ri + 1) / nr
        for ci in range(nc):
            a0, a1 = a_edges[ci], a_edges[ci + 1]
            val = mat[ri, ci]
            c = cmap(norm(val))
            ax.add_patch(Wedge((0, 0), r1, math.degrees(a0), math.degrees(a1),
                               width=r1 - r0, facecolor=c, edgecolor="white",
                               linewidth=0.2))
    # 标签
    for ci, lab in enumerate(col_labels):
        a = (a_edges[ci] + a_edges[ci + 1]) / 2
        ax.text(math.cos(a) * 1.18, math.sin(a) * 1.18, str(lab)[:8],
                rotation=math.degrees(a) - 90, ha="center", va="center", fontsize=5, color=INK)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 10. UpSet（集合交集，非柱状用点+连线表示）
# ═══════════════════════════════════════════════════════════════
def panel_upset(ax, sets_dict, title="UpSet"):
    """
    sets_dict: {set_name: set_of_items}
    画交集矩阵（点阵）+ 大小（用气泡而非柱）
    """
    names = list(sets_dict.keys())
    k = len(names)
    # 计算两两/全局交集
    from itertools import combinations
    all_items = set().union(*sets_dict.values())
    # 仅画单集与两两交集（简化）
    combos = [tuple([i]) for i in range(k)] + [c for c in combinations(range(k), 2)][:6]
    matrix = np.zeros((len(combos), k))
    sizes = []
    for r, combo in enumerate(combos):
        inter = None
        for i in combo:
            inter = sets_dict[names[i]] if inter is None else (inter & sets_dict[names[i]])
        sizes.append(len(inter))
        for i in combo:
            matrix[r, i] = 1
    nr = len(combos)
    for ci in range(k):
        for r in range(nr):
            if matrix[r, ci]:
                ax.scatter(ci, r, s=22, c=CATEGORICAL[ci % len(CATEGORICAL)],
                           edgecolors="white", linewidths=0.4, zorder=3)
            else:
                ax.scatter(ci, r, s=6, c="#cccccc", zorder=2)
        # 连线
        rs = [r for r in range(nr) if matrix[r, ci]]
        if len(rs) > 1:
            ax.plot([ci, ci], [min(rs), max(rs)], color=CATEGORICAL[ci % len(CATEGORICAL)],
                    lw=1.2, zorder=1)
    # 交集大小（气泡）
    for r, sz in enumerate(sizes):
        if sz > 0:
            ax.scatter(k + 0.5, r, s=min(60, 10 + sz / max(sizes) * 50),
                       c="#888888", alpha=0.6, zorder=4)
            ax.text(k + 0.8, r, str(sz), fontsize=5, va="center", color=INK)
    ax.set_yticks(range(nr))
    ax.set_yticklabels([",".join(names[i][:3] for i in c) for c in combos], fontsize=5)
    ax.set_xticks(range(k)); ax.set_xticklabels([n[:4] for n in names], fontsize=6, rotation=45)
    ax.set_xlim(-0.5, k + 1.2)
    ax.set_ylim(-0.5, nr - 0.5)
    _rc(ax)
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 11. 环形火山图 Circular volcano（变体，散点非柱）
# ═══════════════════════════════════════════════════════════════
def panel_circ_volcano(ax, log2fc, neg_log_p, title="Circular volcano"):
    """把火山图映射到一个圆环：角度=log2FC，半径=−log10(p)"""
    lfc = np.asarray(log2fc, float); nlp = np.asarray(neg_log_p, float)
    lfc = lfc[np.isfinite(lfc) & np.isfinite(nlp)]
    nlp = nlp[np.isfinite(nlp)]
    if len(lfc) == 0:
        ax.axis("off"); return
    ang = (lfc / (np.abs(lfc).max() or 1)) * math.pi  # −π..π
    nmax = nlp.max() or 1
    r = 0.3 + (nlp / nmax) * 0.95
    col = np.where(nlp > -np.log10(0.05), np.where(lfc > 0, ACCENT, "#08519C"), GREY)
    ax.scatter(np.cos(ang) * r, np.sin(ang) * r, s=6, c=col, alpha=0.5, edgecolors="none")
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 12. 相关性热图（方型，非柱）
# ═══════════════════════════════════════════════════════════════
def panel_corr_heatmap(ax, matrix, labels, title="Correlation", cmap=plt.cm.RdBu_r,
                       vmin=-1, vmax=1, text=False):
    mat = np.asarray(matrix, float)
    ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=5, rotation=90)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=5)
    if text:
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                ax.text(j, i, f"{mat[i,j]:.1f}", fontsize=4, ha="center", va="center",
                        color="white" if abs(mat[i, j]) > 0.5 else "black")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)


# ═══════════════════════════════════════════════════════════════
# 13. 弦图变体：组↔分类 双向流（多用于多组学层）
# ═══════════════════════════════════════════════════════════════
def panel_group_chord(ax, group_labels, cat_labels, matrix,
                      title="Group–category chord", group_colors=None, cat_colors=None):
    """matrix: (n_group × n_cat) 权重"""
    ns = len(group_labels); nt = len(cat_labels)
    src = []; tgt = []; w = []
    for i in range(ns):
        for j in range(nt):
            if matrix[i, j] > 0:
                src.append(group_labels[i]); tgt.append(cat_labels[j]); w.append(matrix[i, j])
    panel_chord(ax, src, tgt, w, src_colors=group_colors, tgt_colors=cat_colors, title=title)


# 导出可用 panel 名
PANEL_REGISTRY = {
    "chord": panel_chord, "circ_dendrogram": panel_circ_dendrogram,
    "sankey": panel_sankey, "network": panel_network, "sunburst": panel_sunburst,
    "ridge": panel_ridge, "bubble": panel_bubble, "radar": panel_radar,
    "circos_heatmap": panel_circos_heatmap, "upset": panel_upset,
    "circ_volcano": panel_circ_volcano, "corr_heatmap": panel_corr_heatmap,
    "group_chord": panel_group_chord,
}
