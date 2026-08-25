#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
label_qa.py — 标签防重叠 + 版面 QA 整合模块（sci-figure-master skill）
=================================================================================
整合来源（均 MIT）：
- adjustText (pip, https://github.com/Phylosopher/adjustText) — 真实标签斥力算法
  （对同类数据点迭代排斥 + 可选引线），解决 Cartesian 面板文字重叠/遮挡。
- scipilot-figure-skill/scripts/visual_qa.py:audit_layout — 程序自检缺字/文字越界/刻度重叠
- scipilot-figure-skill/scripts/layout_tools.py:add_panel_labels/finalize_figure
  — 统一面板编号对齐 + constrained_layout 兜底
- sciplot-figure-skill/references/AI_VISUAL_REVIEW.md — AI 读图遮挡清单（advisory）

提供 API：
1. repel_labels_cartesian(ax, xs, ys, texts, **kw)
   Cartesian 面板（volcano/bubble/network/ridge/PCoA）用 adjustText 推开标签。
2. polar_node_labels(ax, node_theta, texts, **kw)
   极坐标面板（chord/circular_dendro/radar/radial_bar）用「周长铺开 + 引线」防重叠。
3. audit_layout(fig, **kw)  —— 直接移植 scipilot 的 audit_layout（缺字/裁切/刻度重叠）。
4. add_panel_labels(fig, **kw) / finalize_figure(fig, **kw) —— 移植 scipilot 布局工具。
5. auto_declutter(fig, out_png, **kw) —— 渲染→audit→打印问题（程序层闭环；AI 读图为 advisory）。

依赖：adjustText（已 pip 安装）；其余纯 matplotlib。
用法：在 skill_test_7omics.py 顶部 `sys.path.insert(0, ASSETS); from label_qa import *`
"""
from __future__ import annotations

import io
import logging
import warnings

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.text as mtext

try:
    from adjustText import adjust_text
    HAS_ADJUSTTEXT = True
except Exception:  # pragma: no cover
    HAS_ADJUSTTEXT = False


# ══════════════════════════════════════════════════════════════════
# 1) Cartesian 标签斥力（adjustText）
# ════════════════════════════════════════════════════════════════
def repel_labels_cartesian(ax, xs, ys, texts, fontsize=6, color="#222222",
                           arrow=True, max_move=12, expand=(1.18, 1.45),
                           min_pts=4, ha="center", va="center", zorder=6, **kw):
    """在 Cartesian 轴上把 (xs,ys) 处的 texts 用 adjustText 推开，避免互相重叠/压数据。
    返回创建的 Text 对象列表（便于后续微调）。"""
    pts = [(float(x), float(y), str(t)) for x, y, t in zip(xs, ys, texts)
           if t not in (None, "") and str(t).strip() != ""]
    if not pts:
        return []
    objs = [ax.text(p[0], p[1], p[2], fontsize=fontsize, color=color,
                   ha=ha, va=va, zorder=zorder) for p in pts]
    if HAS_ADJUSTTEXT:
        try:
            adjust_text(
                objs, ax=ax,
                expand=expand,
                max_move=max_move,
                min_pts=min_pts,
                arrowprops=dict(arrowstyle="-", color="#aaaaaa", lw=0.4, alpha=0.75)
                if arrow else None,
                **kw,
            )
        except Exception:
            pass  # 斥力失败不致命，标签退回原位置
    return objs


# ══════════════════════════════════════════════════════════════════
# 2) 极坐标节点标签（周长铺开 + 引线）— 适配 chord/dendro/radar/radial
# ══════════════════════════════════════════════════════════════════
def polar_node_labels(ax, node_theta, texts, R=1.0, Rlab=1.24, fontsize=6,
                      color="#222222", leader=True, min_gap_deg=9.0):
    """极坐标轴上把节点标签沿周长铺开：角度相邻过近的标签交替外扩 + 画细引线连回节点。
    node_theta: 各节点角度（弧度）。texts: 标签字符串。R: 节点环半径；Rlab: 标签基准半径。"""
    order = sorted(range(len(texts)), key=lambda i: node_theta[i])
    radii = [Rlab] * len(texts)
    prev = order[0]
    for k in range(1, len(order)):
        i = order[k]
        gap = abs(((node_theta[i] - node_theta[prev] + np.pi) % (2 * np.pi)) - np.pi)
        if gap < np.radians(min_gap_deg):
            radii[i] = Rlab + 0.07  # 外扩一级
        prev = i
    for i, t in enumerate(texts):
        if t is None or str(t).strip() == "":
            continue
        th = node_theta[i]
        x, y = R * np.cos(th), R * np.sin(th)
        xl, yl = radii[i] * np.cos(th), radii[i] * np.sin(th)
        if leader and radii[i] != R:
            ax.plot([x, xl], [y, yl], color="#bbbbbb", lw=0.4, zorder=1)
        rot = np.degrees(th)
        ha = "left" if np.cos(th) > 0 else "right"
        ax.text(xl, yl, str(t),
                rotation=rot if abs(np.cos(th)) < 0.4 else (rot + 180 if rot > 90 else rot),
                ha=ha, va="center", fontsize=fontsize, color=color, zorder=6)
    return


# ══════════════════════════════════════════════════════════════════
# 3) audit_layout —— 移植自 scipilot-figure-skill/scripts/visual_qa.py
#    （MIT；保留原作者逻辑：缺字 via warnings+logging 双通道，文字越界，刻度重叠）
# ══════════════════════════════════════════════════════════════════
SEVERITY = {"INFO": 0, "WARN": 1, "FAIL": 2}
_GLYPH_MARKERS = ("missing from", "Glyph", "findfont")


class _GlyphLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        msg = record.getMessage()
        if any(m in msg for m in _GLYPH_MARKERS):
            self.messages.append(msg)


def _draw_and_collect_glyph_warnings(fig):
    handler = _GlyphLogHandler()
    mpl_logger = logging.getLogger("matplotlib")
    prev_level = mpl_logger.level
    mpl_logger.setLevel(logging.WARNING)
    mpl_logger.addHandler(handler)
    collected = []
    try:
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100)
            buf.close()
        for w in wlist:
            s = str(w.message)
            if any(m in s for m in _GLYPH_MARKERS):
                collected.append(s)
    finally:
        mpl_logger.removeHandler(handler)
        mpl_logger.setLevel(prev_level)
    collected.extend(handler.messages)
    seen, uniq = set(), []
    for m in collected:
        if m not in seen:
            seen.add(m)
            uniq.append(m)
    return uniq


def _visible_texts(fig):
    out = []
    for t in fig.findobj(mtext.Text):
        try:
            if t.get_visible() and t.get_text().strip():
                out.append(t)
        except Exception:
            continue
    return out


def audit_layout(fig, clip_tol_px=2.0, overlap_tol_px=1.0):
    """对 Figure 做程序自检：[(severity, msg), ...]。
    1) 缺字乱码(FAIL) 2) 文字越界裁切(WARN) 3) 刻度标签重叠(WARN)。非破坏性。"""
    issues = []
    glyph_msgs = _draw_and_collect_glyph_warnings(fig)
    if glyph_msgs:
        sample = " | ".join(glyph_msgs[:3])
        issues.append(("FAIL", f"缺字/乱码：{sample[:240]}。中文图需配 CJK 字体；负号方框设 axes.unicode_minus=False。"))

    try:
        renderer = fig.canvas.get_renderer()
    except Exception:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

    W = float(fig.bbox.width)
    H = float(fig.bbox.height)

    tick_ids = set()
    for ax in fig.axes:
        for tl in (*ax.get_xticklabels(), *ax.get_xticklabels(minor=True),
                   *ax.get_yticklabels(), *ax.get_yticklabels(minor=True)):
            tick_ids.add(id(tl))

    clipped = []
    for t in _visible_texts(fig):
        if id(t) in tick_ids:
            continue
        try:
            bb = t.get_window_extent(renderer)
        except Exception:
            continue
        if (bb.x0 < -clip_tol_px or bb.y0 < -clip_tol_px
                or bb.x1 > W + clip_tol_px or bb.y1 > H + clip_tol_px):
            txt = t.get_text().strip().replace("\n", " ")
            if txt:
                clipped.append(txt[:24])
    if clipped:
        uniq = list(dict.fromkeys(clipped))[:6]
        issues.append(("WARN", f"文字可能越界被裁切：{uniq}。用 finalize_figure 或 bbox_inches='tight' 兜底，或缩短标签。"))

    overlap_axes = 0
    for ax in fig.axes:
        if ax.get_subplotspec() is None:
            continue
        if _ticklabels_overlap(ax.get_xticklabels(), renderer, "x", overlap_tol_px):
            overlap_axes += 1
        elif _ticklabels_overlap(ax.get_yticklabels(), renderer, "y", overlap_tol_px):
            overlap_axes += 1
    if overlap_axes:
        issues.append(("WARN", f"{overlap_axes} 个子图存在刻度标签重叠。x 轴旋转刻度或减少刻度；y 轴增大子图高度。"))
    return issues


def _ticklabels_overlap(labels, renderer, axis, tol):
    boxes = []
    for l in labels:
        try:
            if l.get_visible() and l.get_text().strip():
                boxes.append(l.get_window_extent(renderer))
        except Exception:
            continue
    if len(boxes) < 2:
        return False
    if axis == "x":
        boxes.sort(key=lambda b: b.x0)
        return any(a.x1 - b.x0 > tol for a, b in zip(boxes, boxes[1:]))
    else:
        boxes.sort(key=lambda b: b.y0)
        return any(a.y1 - b.y0 > tol for a, b in zip(boxes, boxes[1:]))


def print_report(issues):
    if not issues:
        print("  [PASS] 程序自检：无缺字 / 裁切 / 刻度重叠。")
        return "PASS"
    max_sev = max(SEVERITY[s] for s, _ in issues)
    verdict = {2: "FAIL", 1: "WARN", 0: "INFO"}[max_sev]
    for sev, msg in sorted(issues, key=lambda x: -SEVERITY[x[0]]):
        print(f"  [{sev}] {msg}")
    return verdict


# ══════════════════════════════════════════════════════════════════
# 4) 布局工具 —— 移植自 scipilot-figure-skill/scripts/layout_tools.py
#    add_panel_labels（统一对齐 a/b/c）+ finalize_figure（constrained 兜底）
# ══════════════════════════════════════════════════════════════════
_PANEL_STYLES = {
    "nature": lambda s: s,
    "science": lambda s: s,
    "ieee": lambda s: f"({s})",
    "paren": lambda s: f"({s})",
    "upper": lambda s: s.upper(),
    "upper_paren": lambda s: f"({s.upper()})",
}


def _letter_sequence(n):
    letters = "abcdefghijklmnopqrstuvwxyz"
    out = []
    for i in range(n):
        if i < 26:
            out.append(letters[i])
        else:
            out.append(letters[i // 26 - 1] + letters[i % 26])
    return out


def _data_axes(fig):
    return [ax for ax in fig.axes if ax.get_subplotspec() is not None]


def add_panel_labels(fig, axes=None, labels=None, style="nature", fontsize=None,
                      fontweight="bold", x_offset_pt=-20.0, y_offset_pt=2.0,
                      ha="right", va="bottom", color="black"):
    """统一对齐的多面板 a/b/c 编号（锚点 axes fraction(0,1) + 统一 points 偏移）。"""
    if axes is None:
        axes = _data_axes(fig)
        axes = sorted(axes, key=lambda ax: (-round(ax.get_position().y1, 3),
                                            round(ax.get_position().x0, 3)))
    axes = list(axes)
    n = len(axes)
    if n == 0:
        return []
    if labels is None:
        fmt = _PANEL_STYLES.get(style)
        if fmt is None:
            raise ValueError(f"Unknown panel style: {style!r}")
        labels = [fmt(s) for s in _letter_sequence(n)]
    elif len(labels) < n:
        raise ValueError(f"labels({len(labels)}) < axes({n})")
    if fontsize is None:
        fontsize = plt.rcParams.get("axes.labelsize", 9)
    placed = []
    for ax, lab in zip(axes, labels):
        t = ax.annotate(lab, xy=(0, 1), xycoords="axes fraction",
                        xytext=(x_offset_pt, y_offset_pt), textcoords="offset points",
                        fontsize=fontsize, fontweight=fontweight, color=color,
                        ha=ha, va=va, annotation_clip=False)
        placed.append(t)
    return placed


def finalize_figure(fig, prefer="constrained"):
    """出图前兜底理顺版面（constrained_layout 优先，失败回退 tight_layout）。"""
    used = "none"
    if prefer == "constrained":
        try:
            fig.set_layout_engine("constrained")
            fig.canvas.draw()
            used = "constrained"
        except Exception:
            used = "none"
    if used == "none":
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fig.tight_layout()
            used = "tight"
        except Exception:
            used = "none"
    return used


# ══════════════════════════════════════════════════════════════════
# 5) 闭环：渲染 → 程序自检 → 打印（AI 读图为 advisory，见 sciplot AI_VISUAL_REVIEW）
# ══════════════════════════════════════════════════════════════════
def auto_declutter(fig, out_png=None, verbose=True):
    """对 fig 做 audit_layout；若给定 out_png 则先渲一张 PNG 供 AI 读图复核。
    返回 (verdict, issues)。程序层闭环：发现 FAIL/WARN 可回改重渲。"""
    issues = audit_layout(fig)
    verdict = print_report(issues) if verbose else (
        "PASS" if not issues else ("FAIL" if any(s == "FAIL" for s, _ in issues) else "WARN"))
    if out_png:
        try:
            fig.savefig(out_png, dpi=150, bbox_inches="tight")
        except Exception:
            pass
    return verdict, issues


__all__ = [
    "repel_labels_cartesian", "polar_node_labels", "audit_layout", "print_report",
    "add_panel_labels", "finalize_figure", "auto_declutter", "HAS_ADJUSTTEXT",
]
