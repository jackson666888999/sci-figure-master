# -*- coding: utf-8 -*-
"""路由覆盖审计：70领域 / K-Dense 22学科 / 163技能 / PaperBanana"""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\git\sci-figure-master\assets")

import bioinfo_router as br
import domains_70_config as d70
import chart_catalog as cc

lines = []
def L(s): lines.append(str(s))

L("=== 1. 路由总条目 ===")
all_r = br._all_routing()
L(f"total routing entries: {len(all_r)}")

L("\n=== 2. 70 领域配置 ===")
L(f"DOMAINS_70_ROUTING: {len(d70.DOMAINS_70_ROUTING)} entries")
L(f"DOMAIN_70_NAMES: {len(d70.DOMAIN_70_NAMES)} domains")
L(f"sample domains: {list(d70.DOMAIN_70_NAMES.values())[:10]}")

L("\n=== 3. K-Dense 22 学科 ===")
kd = getattr(d70, "KDENSE_DISCIPLINE_ROUTING", {})
L(f"KDENSE_DISCIPLINE_ROUTING: {len(kd)} entries")
disc = getattr(d70, "KDENSE_DISCIPLINE_NAMES", None)
if disc is None:
    disc = getattr(d70, "KDENSE_DISCIPLINES", None)
L(f"disciplines: {list(disc.values()) if isinstance(disc, dict) else disc}")

L("\n=== 4. K-Dense 163 技能 → 图型映射 ===")
L(f"KDENSE_DISCIPLINE_SKILLS: {len(getattr(d70, 'KDENSE_DISCIPLINE_SKILLS', {}))} disciplines")

L("\n=== 5. chart_catalog 总图型 ===")
n = cc.count_charts()
L(f"total: {n['total']}, sources: {n['by_source']}")

L("\n=== 6. PaperBanana / 机制图接入 ===")
L(f"mechanism_diagram in catalog: {'mechanism_diagram' in cc.CHART_CATALOG}")
L(f"graphical_abstract in catalog: {'graphical_abstract' in cc.CHART_CATALOG}")
L(f"plot_mechanism_diagram native: {br.get_native_plot_function('general','mechanism_diagram')}")

L("\n=== 7. 22 学科 × 图型 抽查（每学科 top 图型）===")
try:
    from domains_70_config import KDENSE_DISCIPLINE_ROUTING
    for disc_key, entries in list(KDENSE_DISCIPLINE_ROUTING.items())[:22]:
        L(f"  {disc_key}: {len(entries)} figure entries")
except Exception as e:
    L(f"  ERR: {e}")

with open(r"E:\XNP论文初稿\_routing_audit.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("AUDIT DONE", len(lines))
