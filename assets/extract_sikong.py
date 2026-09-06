# -*- coding: utf-8 -*-
"""提取司空工作室 R 模板包到 sci-figure-master 仓库（含过滤规则）"""
import zipfile, os, sys, time
from pathlib import Path

SRC = Path(r"E:\sci_figure_master")
REPO = Path(r"E:\git\sci-figure-master")
MAX_SIZE = 20 * 1024 * 1024          # 单文件 >20MB 排除（含 GitHub 风险文件）
EXCLUDE_EXT = {".mp4", ".rhistory", ".ds_store", ".zip", ".exe", ".dll", ".bat"}
EXCLUDE_NAME = {"__MACOSX"}

def excluded(name: str, size: int) -> bool:
    parts = name.split("/")
    if any(p in EXCLUDE_NAME for p in parts):
        return True
    p = Path(name)
    if p.suffix.lower() in EXCLUDE_EXT:
        return True
    if size > MAX_SIZE:
        return True
    # .RData/.rda 一律排除（均为二进制工作区快照，最大 2.2GB）
    if p.suffix.lower() in {".rdata", ".rda"}:
        return True
    return False

def extract(zip_path: Path, base_prefix: str, dest: Path, label: str):
    dest.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(zip_path)
    names = [n for n in z.namelist() if n.startswith(base_prefix) and not n.endswith("/")]
    total = len(names)
    done = skipped = 0
    t0 = time.time()
    for i, n in enumerate(names):
        rel = n[len(base_prefix):]
        info = z.getinfo(n)
        if excluded(n, info.file_size):
            skipped += 1
            continue
        target = dest / rel
        if ".." in rel or rel.startswith(("/", "\\")):
            continue  # 防路径穿越
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size == info.file_size:
            done += 1
            continue
        with z.open(n) as src, open(target, "wb") as out:
            out.write(src.read())
        done += 1
        if (i + 1) % 200 == 0:
            el = time.time() - t0
            print(f"[{label}] {done}/{total} (skip {skipped}) {el:.0f}s", flush=True)
    print(f"[{label}] DONE: extracted={done} skipped={skipped} time={time.time()-t0:.0f}s", flush=True)

# 1) 50套 —— 全量（除垃圾文件）
z50 = SRC / "【司空工作室】R语言科研绘图50套-2025更新.zip"
b50 = "【司空工作室】R语言科研绘图50套-2025更新/"
extract(z50, b50, REPO / "assets" / "sikong_50", "50套")

# 2) 360套 —— 内层 zip
z360 = SRC / "【司空工作室】R语言科研绘图360套-2026更新.zip" / "【司空工作室】R语言科研绘图360套-2026更新.zip"
b360 = "【司空工作室】R语言科研绘图360套-2026更新/35-R语言SCI 360+Nature 绘图模板/"
extract(z360, b360, REPO / "assets" / "sikong_360", "360套")

print("ALL DONE", flush=True)
