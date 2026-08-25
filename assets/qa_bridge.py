#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
qa_bridge.py — 完整集成 scipilot-figure-skill + sciplot-figure-skill 的桥接层
=================================================================================
sci-figure-master 已把两个仓库**完整**克隆进 assets/（含全部脚本/参考/样式/协议）：
  assets/scipilot-figure-skill/   (MIT, 19 文件；纯 matplotlib/seaborn/pandas/scipy，Python 3.13 可直接用)
  assets/sciplot-figure-skill/    (MIT, ~268 文件；声明 requires-python>=3.14，但代码在 3.13 可 import)

本模块把它们的**真实能力**暴露成可调用函数 + CLI，避免只是"死文件"：

scipilot（直接 import 即可用，已验证 3.13 全部 import OK）：
  - profile_csv(path, group_cols)        → EDA 剖析（列类型/样本量/分布/异常/相关/初步图型建议）
  - setup_style(journal, lang, ...)      → 期刊预设 + CJK 字体 + SciencePlots 包装
  - export_figure(fig, basename, ...)    → 多格式 + 按最终尺寸 + 灰度预览（色盲检查）
  - check_figure_file(path, ...)         → 文件合规自检（格式/DPI/字体嵌入）
  - audit_layout(fig)                    → 程序自检：缺字乱码 / 文字裁切 / 刻度重叠
  - add_panel_labels(fig, ...) / finalize_figure(fig) → 面板 a/b/c 对齐 + constrained_layout 兜底

sciplot（声明 3.14；用子进程调用其 CLI，自动定位解释器）：
  - run_sciplot(input, profile, out_dir, python_exe, subcommand)
      subcommand = run | validate | finalize | trace-pdf
      例：run_sciplot("a.csv", "standard", "out/fig") → scripts/sciplot.py run --profile standard

设计原则：所有 import 惰性 + try/except，缺依赖时给出清晰指引，不致命。
label_qa.py 只是把 scipilot 的 audit_layout + layout_tools 做的"最小自包含提取"（出图脚本零依赖即可调）；
完整能力请用本桥接层或 assets/ 下原仓库。
"""
from __future__ import annotations

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
SCIPILOT = ASSETS / "scipilot-figure-skill"
SCIPILOT_SCRIPTS = SCIPILOT / "scripts"
SCIPILOT_OK = SCIPILOT.exists()
SCIPILOT_PY = os.environ.get("SCIPILOT_PY", "")  # 可选：指定运行 sciplot 的 Python（如 3.14 venv）


def _load_scipilot(modname):
    """惰性 import scipilot 的某脚本模块；失败抛清晰异常。"""
    if not SCIPILOT_OK:
        raise RuntimeError("未找到 assets/scipilot-figure-skill/（完整仓库未克隆？）")
    if str(SCIPILOT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCIPILOT_SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        modname, SCIPILOT_SCRIPTS / f"{modname}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ───────────────────────────────────────────────────────────────────────────
# scipilot 包装（直接 import，3.13 可跑）
# ───────────────────────────────────────────────────────────────────────────
def profile_csv(path, group_cols=None, **kw):
    """EDA 剖析。group_cols: list[str] 或 str。返回剖析报告 dict。"""
    m = _load_scipilot("profile_data")
    return m.profile_data(path, group_cols=group_cols, **kw)


def setup_style(journal="nature", lang="en", use_sciplots=True, serif_for_zh=False, **kw):
    """期刊样式 + CJK 字体（Noto/Source Han/SimHei/YaHei）+ SciencePlots 包装。"""
    m = _load_scipilot("setup_style")
    return m.setup_style(journal=journal, lang=lang, use_sciplots=use_sciplots,
                         serif_for_zh=serif_for_zh, **kw)


def export_figure(fig, basename, formats=("pdf", "svg", "png"), dpi=300,
                  size_inches=None, grayscale_preview=False, **kw):
    """多格式导出 + 按最终尺寸 + 灰度预览。basename 不含扩展名。"""
    m = _load_scipilot("export_figure")
    return m.export_figure(fig, basename=basename, formats=list(formats), dpi=dpi,
                           size_inches=size_inches, grayscale_preview=grayscale_preview, **kw)


def check_figure_file(path, min_dpi=300, target_inches=None, **kw):
    """文件级合规自检（格式/DPI/字体嵌入）。"""
    m = _load_scipilot("check_figure")
    return m.check_figure(path, min_dpi=min_dpi, target_inches=target_inches, **kw)


def audit_layout(fig, **kw):
    """程序自检：缺字乱码 / 文字裁切 / 刻度重叠 → [(severity, msg), ...]"""
    m = _load_scipilot("visual_qa")
    return m.audit_layout(fig, **kw)


def add_panel_labels(fig, **kw):
    """统一对齐的多面板 a/b/c 编号（锚点 axes fraction(0,1) + 统一偏移）。"""
    m = _load_scipilot("layout_tools")
    return m.add_panel_labels(fig, **kw)


def finalize_figure(fig, prefer="constrained"):
    """出图前兜底理顺版面（constrained_layout 优先，失败回退 tight_layout）。"""
    m = _load_scipilot("layout_tools")
    return m.finalize_figure(fig, prefer=prefer)


# ───────────────────────────────────────────────────────────────────────────
# sciplot 包装（子进程调用其 CLI；声明需 3.14，但 3.13 多可跑，缺依赖会清晰报错）
# ───────────────────────────────────────────────────────────────────────────
def _resolve_sciplot_python():
    if SCIPILOT_PY:
        return SCIPILOT_PY
    # 默认用当前解释器；若 sciplot 需要 3.14 特性再改用 3.14 venv
    return sys.executable


def run_sciplot(input=None, profile="standard", out_dir="out/figure",
                python_exe=None, subcommand="run", extra_args=None, **kw):
    """调用 sciplot-figure-skill 的 CLI。

    subcommand: run | validate | finalize | trace-pdf
    profile:    quick | standard | audit | auto
    返回 subprocess.CompletedProcess。
    """
    scripts = ASSETS / "sciplot-figure-skill" / "scripts" / "sciplot.py"
    if not scripts.exists():
        raise RuntimeError("未找到 assets/sciplot-figure-skill/scripts/sciplot.py（完整仓库未克隆？）")
    py = python_exe or _resolve_sciplot_python()
    cmd = [py, str(scripts), subcommand]
    if subcommand == "run":
        cmd += ["--input", str(input), "--profile", profile, "--out-dir", str(out_dir)]
    elif subcommand in ("validate", "finalize"):
        cmd += ["--project", str(out_dir)]
        if subcommand == "finalize":
            cmd += ["--profile", profile]
    elif subcommand == "trace-pdf":
        pass
    if extra_args:
        cmd += list(extra_args)
    print(f"  [sciplot] {subcommand} profile={profile}\n    $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=False, capture_output=False)


# ───────────────────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────────────────
def _cli(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "profile":
        if not rest:
            print("用法: qa_bridge.py profile <csv> [--group col1,col2]"); return 1
        path = rest[0]
        groups = None
        if "--group" in rest:
            i = rest.index("--group"); groups = rest[i + 1].split(",")
        rep = profile_csv(path, group_cols=groups)
        import json
        print(json.dumps(rep, ensure_ascii=False, indent=2, default=str)[:4000])
        return 0
    if cmd == "check":
        if not rest:
            print("用法: qa_bridge.py check <figure_path>"); return 1
        print(check_figure_file(rest[0])); return 0
    if cmd == "sciplot":
        # qa_bridge.py sciplot <input.csv> --profile standard [--out-dir D] [--py PY]
        if not rest:
            print("用法: qa_bridge.py sciplot <input.csv> --profile standard [--out-dir D]"); return 1
        inp = rest[0]
        profile = "standard"; out = "out/figure"; py = None
        if "--profile" in rest: profile = rest[rest.index("--profile") + 1]
        if "--out-dir" in rest: out = rest[rest.index("--out-dir") + 1]
        if "--py" in rest: py = rest[rest.index("--py") + 1]
        run_sciplot(input=inp, profile=profile, out_dir=out, python_exe=py)
        return 0
    print(f"未知命令: {cmd}\n可用: profile / check / sciplot"); return 1


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))


__all__ = [
    "profile_csv", "setup_style", "export_figure", "check_figure_file",
    "audit_layout", "add_panel_labels", "finalize_figure",
    "run_sciplot", "SCIPILOT_OK",
]
