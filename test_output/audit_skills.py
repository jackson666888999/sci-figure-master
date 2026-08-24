# -*- coding: utf-8 -*-
"""验证：K-Dense 163 技能映射覆盖 + mechanism_diagram 路由"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\git\sci-figure-master\assets")
import bioinfo_router as br

lines = []
def L(s): lines.append(str(s))

# 1) mechanism_diagram 路由
L("=== mechanism_diagram 路由 ===")
L(f"general/mechanism_diagram -> {br.get_native_plot_function('general', 'mechanism_diagram')}")
L(f"general/pathway -> {br.get_native_plot_function('general', 'pathway')}")
L(f"paper/graphical_abstract -> {br.get_native_plot_function('paper', 'graphical_abstract')}")

# 2) K-Dense 163 技能覆盖
L("\n=== K-Dense 163 技能 → 路由命中 ===")
skills_file = r"E:\git\sci-figure-master\scripts\kdense_skills_list.txt"
if os.path.exists(skills_file):
    with open(skills_file, encoding="utf-8") as f:
        skills = [s.strip() for s in f if s.strip()]
    L(f"技能总数: {len(skills)}")
    # 技能名 → 检查是否能路由到图型（模糊匹配：技能名含图型词）
    hit, miss = 0, []
    for sk in skills:
        skl = sk.lower()
        # 在 ROUTING_TABLE 的图型键中找子串匹配
        found = False
        for (d, p) in br._all_routing():
            pl = p.lower()
            if (skl in pl or pl in skl) and len(pl) >= 3:
                found = True
                break
        if found:
            hit += 1
        else:
            miss.append(sk)
    L(f"技能→图型词命中: {hit}/{len(skills)}")
    L(f"未命中前 20: {miss[:20]}")
else:
    L("kdense_skills_list.txt 不存在")

# 3) 22 学科 → 技能 → 图型
L("\n=== 22 学科技能→图型（KDENSE_DISCIPLINE_SKILLS）===")
try:
    from domains_70_config import KDENSE_DISCIPLINE_SKILLS
    total_sk = 0
    for disc, sklist in KDENSE_DISCIPLINE_SKILLS.items():
        total_sk += len(sklist)
        L(f"  {disc}: {len(sklist)} skills")
    L(f"总技能条目: {total_sk}")
except Exception as e:
    L(f"ERR: {e}")

with open(r"E:\XNP论文初稿\_skills_audit.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("DONE", len(lines))
