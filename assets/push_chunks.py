# -*- coding: utf-8 -*-
"""分块提交+推送剩余 sikong_360 模板，每块约 80MB，推送失败自动重试"""
import subprocess, time, os

REPO = r"E:\git\sci-figure-master"
CHUNK_BYTES = 80 * 1024 * 1024

def run(args, **kw):
    return subprocess.run(args, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)

def untracked_dirs():
    r = run(["git", "status", "--porcelain"])
    dirs = []
    for line in r.stdout.splitlines():
        if line.startswith("?? "):
            p = line[3:].strip().strip('"')
            full = os.path.join(REPO, p)
            if os.path.isdir(full) and p.startswith("assets/sikong_360"):
                dirs.append(p)
    return dirs

def dir_size(p):
    total = 0
    for root, _, files in os.walk(os.path.join(REPO, p)):
        for f in files:
            try: total += os.path.getsize(os.path.join(root, f))
            except OSError: pass
    return total

def push_with_retry(max_try=12):
    for i in range(1, max_try + 1):
        r = run(["git", "push", "origin", "main"], timeout=1200)
        out = (r.stdout + r.stderr).strip()
        if "main -> main" in out or "Everything up-to-date" in out:
            print(f"  PUSH OK (attempt {i})", flush=True)
            return True
        print(f"  push attempt {i} failed: {out.splitlines()[-1] if out else '?'}", flush=True)
        time.sleep(15)
    return False

dirs = untracked_dirs()
print(f"untracked dirs: {len(dirs)}", flush=True)
chunk, size = [], 0
chunk_no = 0
for d in dirs:
    s = dir_size(d)
    chunk.append(d); size += s
    if size >= CHUNK_BYTES:
        chunk_no += 1
        print(f"[chunk {chunk_no}] {len(chunk)} dirs, {size/1e6:.0f}MB: {chunk[0].split('/')[-1][:30]} .. {chunk[-1].split('/')[-1][:30]}", flush=True)
        run(["git", "add", "--"] + chunk)
        c = run(["git", "commit", "-q", "-m", f"feat: 集成司空360套模板 分块{chunk_no} ({size/1e6:.0f}MB)"])
        if c.returncode != 0:
            print("  commit failed:", c.stderr[:200], flush=True)
            continue
        if not push_with_retry():
            print("PUSH FAILED — stopping, commits remain local", flush=True)
            raise SystemExit(1)
        chunk, size = [], 0
if chunk:
    chunk_no += 1
    print(f"[chunk {chunk_no}] {len(chunk)} dirs, {size/1e6:.0f}MB (final)", flush=True)
    run(["git", "add", "--"] + chunk)
    run(["git", "commit", "-q", "-m", f"feat: 集成司空360套模板 分块{chunk_no} ({size/1e6:.0f}MB, 尾块)"])
    if not push_with_retry():
        print("PUSH FAILED — stopping, commits remain local", flush=True)
        raise SystemExit(1)
print("ALL CHUNKS PUSHED", flush=True)
