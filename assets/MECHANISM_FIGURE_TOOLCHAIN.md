# 机制图 / 学术配图工具链全景（4 条路径全覆盖）

> 覆盖：`plot_mechanism_diagram`（原生路由） + `biorender-pro` skill + `PaperBanana`（dwzhu-pku）+ `biorender-mechanism-figures-skill`（yiyanli123）
> 全部按磁盘红线克隆至 `E:\git`：PaperBanana / biorender-mechanism-figures-skill

## 路径总览

| # | 工具 | 定位 | 输入 | 输出 | 路由键 | 本地位置 |
|---|---|---|---|---|---|---|
| 1 | **plot_mechanism_diagram**（原生） | 确定性可编辑机制图（无需 API） | dict{entities,relations} 或 DataFrame | SVG/PDF/PNG300/TIFF600 可编辑矢量 | `general/mechanism_diagram`、`academic/pathway_diagram`、`paper/graphical_abstract`、`flowchart` | `assets/bioinfo_router.py` |
| 2 | **biorender-pro**（整合 skill） | 科研卡通图 5 步流水线（解析→证据分级→反AI感→PaperBanana→SVG导出） | 中文科研描述 | PNG 草稿 → SVG/PDF 矢量 | 触发词"画机制图/机制图/图形摘要" | `~/.workbuddy/skills/biorender-pro/` |
| 3 | **PaperBanana**（dwzhu-pku） | 多智能体学术配图自动生成（Retriever→Planner→Stylist→Visualizer→Critic） | 论文段落/机制描述 | 出版级配图 | 经 biorender-pro bridge 调用 | `E:\git\PaperBanana\` |
| 4 | **biorender-mechanism-figures-skill**（yiyanli123） | BioRender 风格**图像生成 prompt 构建器** | 机制/通路/摘要描述 | 结构化 prompt → GPT Image/其他生图 | 独立 skill（可迁移 Codex/Claude/OpenCode） | `E:\git\biorender-mechanism-figures-skill\` |

## 路由接入（已配置）

`ROUTING_TABLE` 新增机制图条目（13 个键 → plot_mechanism_diagram）：
```
("general","mechanism_diagram") / ("general","mechanism") / ("general","graphical_abstract")
("general","pathway_diagram") / ("general","pathway") / ("general","flowchart") / ("general","flow_chart")
("academic","mechanism_diagram"/"graphical_abstract"/"pathway_diagram"/"flowchart")
("paper","mechanism_diagram") / ("paper","graphical_abstract") / ("paper","figure")
```
`chart_catalog` Presentation 类注册：mechanism_diagram / graphical_abstract / pathway_diagram / flowchart（共 12 种演示文稿图型，153 总图型）。

## 4 条路径选择建议

- **快速可编辑机制图**（组会/初稿）：路径 1（原生，零依赖、确定性布局、可改代码重画）
- **顶刊级卡通示意图**（投稿）：路径 2（biorender-pro：中文描述 → 证据分级 + PaperBanana 多 Agent + 反 AI 感 SVG 导出）
- **论文图形摘要 GA**：路径 2 的 `ga` 模式，或路径 4 生成 prompt → 高质量生图
- **无 API 环境兜底**：路径 1（纯 matplotlib，不依赖任何外部服务）

## PaperBanana（dwzhu-pku）要点

- 仓库：`E:\git\PaperBanana`（多 Agent 流水线：agents/ + prompts/ + style_guides/ + visualize/）
- 本地 biorender-pro `integration/paperbanana_bridge.py` 支持 3 模式：`auto` / `paperbanana`（本地）/ `openrouter`（API）/ `fallback`
- 需要 API key：`OPENROUTER_API_KEY` 或 `GEMINI_API_KEY`（环境变量）

## yiyanli123 要点（biorender-mechanism-figures-skill）

- 仓库：`E:\git\biorender-mechanism-figures-skill`
- 核心：`scripts/build_prompt.py` 把机制描述 → 出版级生图 prompt（17 参数：topic/figure-type/audience/canvas/elements/flow/labels...）
- gallery 含 6 个示例：**gut-microbiome-metabolite-axis.md（肠脑轴）**、neuroinflammation-cascade、single-cell-multiomics-workflow 等
- 跨平台：SKILL.md 纯 Markdown，可装到 Codex/Claude Code/OpenCode

## 与 K-Dense / 70 领域路由的关系

- 机制图作为**跨领域通用图型**（Presentation 类）挂在 ROUTING_TABLE，任何领域（70 生信领域 / 22 K-Dense 学科）请求 mechanism/pathway/GA 图型都会命中；
- 22 学科（paper/visual/cellbio/neuro/...）的图型列表（970 条）中已包含 infographics/scientific-schematics/slides 等配图技能映射。
