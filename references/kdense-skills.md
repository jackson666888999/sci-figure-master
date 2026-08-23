# K-Dense 绘图/可视化/插图技能路由

> sci-figure-master 运行时可直接调用已安装的 K-Dense 技能（位于 WorkBuddy skills 目录）。
> 这些技能均基于 MIT License，商用须保留其 LICENSE 版权声明。

## 直接相关的绘图技能
| 技能名 | 用途 | 调用场景 |
|--------|------|----------|
| scientific-visualization | 通用科学可视化 | 数据图美化、面板布局 |
| matplotlib | Python 绘图底层 | 任意 matplotlib 图 |
| seaborn | 统计数据可视化 | 统计图表 |
| scientific-schematics | 科研示意图生成 | 机制图/流程图草图 |
| scientific-slides | 科研幻灯片 | 汇报用图 |
| scientific-visualization | 顶刊风格图 | Nature/Cell 风格 |
| pptx-posters | PPT/海报 | 会议海报 |
| latex-posters | LaTeX 海报 | 学术海报 |
| infographics | 信息图 | 科普/综述图 |
| generate-image | AI 生图 (FLUX.2 Pro + Gemini) | 卡通机制图底图 |
| docx / pdf / xlsx | 文档处理 | 图嵌入文档 |

## 领域绘图技能（按需）
- 单细胞：scanpy, anndata, scvi-tools, scvelo, arboreto, cellxgene-census
- 化学/分子：rdkit, datamol, deepchem, diffdock, pymatgen, molecular-dynamics
- 网络/和弦：pyCirclize (通过 pip), networkx, torch-geometric
- 热图/统计：statsmodels, scikit-learn, shap, umap-learn
- 文献/写作：literature-review, scientific-writing, citation-management

## 调用方式
在对话中提及技能名即可触发，例如：
- "用 scientific-visualization 把这张图改成 Nature 风格"
- "用 generate-image 生成肠脑轴机制图底图"
- "用 scanpy 画 UMAP"

## 合规
K-Dense 技能原始版权归 K-Dense Inc. (MIT)。本 repo 的 sci-commercial 分支含去标识版；sci-figure-master 主分支直接引用原名以保持溯源。
