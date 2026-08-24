# 学术汇报 / 组会 PPT 工具路由（Presentation Tools）

> 已接入 chart_catalog.py（149 种图表类型，含 8 种演示文稿类型），路由键 `category="Presentation"`。
> 本地克隆（E:\git，遵循磁盘红线）：marp-theme-academic / Latex-Beamer-Template / marp-slides

## 工具清单与场景匹配

| 路由键 | 工具 | 本地/远程 | ⭐ | 适用场景 | 输出 | 上手成本 |
|---|---|---|---|---|---|---|
| `quarto_slides` | **Quarto**（quarto-dev/quarto-cli） | 远程（CLI 安装） | — | **学术汇报/组会/课程标配**，R/Python 数据驱动，图表直接渲染 | HTML(revealjs)/PPTX/PDF | 中（需装 quarto CLI） |
| `reveal_slides` | **Reveal.js**（hakimel/reveal.js） | 远程 | 72k | 交互式网页演示、数学公式、代码高亮、图表嵌入 | HTML | 低（一个 HTML） |
| `reveal_md` | **reveal-md**（webpro/reveal-md） | 远程 | 3.9k | Markdown 直接出 reveal.js，组会快速版 | HTML | 极低 |
| `marp_slides` | **Marp + marp-theme-academic**（kaisugi） | ✅ E:\git | 278 | Markdown 一键转 PPT/PDF，学术主题现成（含 title/section/两栏布局） | PPTX/PDF/HTML | 极低（VS Code 插件） |
| `labmeeting_slides` | **marp-slides**（robonuggets） | ✅ E:\git | 295 | 组会汇报模板集：22 个示例 deck、SVG 图表、暗/亮主题、dashboard 组件 | PPTX/PDF | 极低 |
| `beamer_slides` | **LaTeX Beamer**（SunYanCN/Latex-Beamer-Template） | ✅ E:\git | 287 | **学术答辩/讲座标准**，中文模板，公式/定理环境完善 | PDF | 中（需 TeX Live） |
| `sustech_slides` | **SUSTC Beamer**（SUSTC/sustech-slides） | 远程 | 89 | 高校学术演示模板 | PDF | 中 |
| `slidev_slides` | **Slidev**（slidevjs/slidev） | 远程 | 48k | 开发者向演示，代码高亮/交互图表，主题生态丰富 | HTML/PDF | 中（Node） |
| `poster` | Quarto poster / beamerposter | 远程 | — | 会议海报 | PDF | 中 |

## 推荐组合（科研日常）

- **组会文献汇报**：Marp + marp-theme-academic（写 Markdown 即出 PPT，改文字即可复用）→ `marp_slides`
- **正式学术报告/答辩**：Quarto revealjs 或 LaTeX Beamer → `quarto_slides` / `beamer_slides`
- **数据密集汇报**（含图表自动渲染）：Quarto（R/Python 代码块直出图表）→ `quarto_slides`
- **网页互动汇报**：Reveal.js → `reveal_slides`

## 快速开始（Marp 学术主题示例）

```bash
# E:\git\marp-theme-academic 已克隆，内含 themes/*.css 与 example
# 使用 VS Code + Marp for VS Code 插件，或 CLI：
npx @marp-team/marp-cli slides.md -o output.pptx --theme academic
```

```markdown
---
marp: true
theme: academic
title: XNP 多组学机制汇报
---

# 乌灵菌粉（XNP）睡眠剥夺多组学机制
## 肠道菌群-嘌呤-小胶质/OPC 轴

---

## 主图面板
- 行为学：睡眠时长恢复（padj=0.019）
- 单核层：Tgfbr1（小胶质 FDR 0.0448）
- ...
```

## 与 SciVizKit 的关系

SciVizKit 出论文图（Figure），Presentation 类出汇报（Slide）。流水线：
`数据 → comprehensive_analysis → bioinfo_router 出图 → 三线表 → Quarto/Marp 组会汇报`

## 路由接入说明

- `chart_catalog.py` 新增 `_PRESENTATION_CHARTS`（8 项），`suggest_for_domain("academic"/"meeting"/"report")` 即可返回；
- 本地克隆目录：`E:\git\marp-theme-academic`、`E:\git\Latex-Beamer-Template`、`E:\git\marp-slides`；
- 其余工具（quarto/reveal/slidev）按需 `npx`/`pip`/CLI 安装，不进 E:\git 仓库。
