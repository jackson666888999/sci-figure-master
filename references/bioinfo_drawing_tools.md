# 生物信息学科研绘图 GitHub 资源库（深度调研 100+ 工具）

> 来源：用户深度调研（2026-08-23），按研究方向（多组学/单细胞/网络药理学/知识图谱/肠脑轴）分类。
> 用途：sci-figure-master 按需 clone / 参考。高星标、活跃维护优先。

## 一、综合性资源库（必看）
- cmdcolin/awesome-genome-visualization — 346+ 基因组可视化工具
- danielecook/Awesome-Bioinformatics — 最全生信工具（含可视化专区）
- seandavi/awesome-single-cell — 单细胞全技术栈
- mikelove/awesome-multi-omics — 多组学整合方法大全

## 二、单细胞分析可视化
- scverse/scanpy — Python 单细胞标准（UMAP/tSNE/点图/小提琴）
- satijalab/seurat — R 单细胞标准（DimPlot/FeaturePlot/DotPlot）
- smorabit/hdWGCNA — 单细胞加权基因共表达网络
- sqjin/CellChat (jinworks/CellChat) — 细胞通讯网络（和弦/气泡/层级）
- cole-trapnell-lab/monocle3 — 伪时序推断
- kstreet13/slingshot — 轨迹分叉路径
- dynverse/dynmethods — 50+ 轨迹方法整合
- scverse/scvelo — RNA 速度流场/相图
- vmorabit/velocyto.R — 原始 RNA 速度
- GreenleafLab/ArchR — scATAC 全流程
- timothy-barry/signac — Seurat 生态 scATAC

## 三、多组学整合与可视化
- biofam/MOFA2 — 因子分析整合多组学（内置可视化）
- mixOmics/mixOmics — DIABLO 监督整合 + 网络图
- Trhova/Multi-omics — VAE/DIABLO/DIVAS 比较
- pmartR/pmartR — 蛋白/代谢/脂质组 QC+统计+可视化
- cafferychen777/POMAShiny — 代谢组 Web 可视化
- cafferychen777/ggpicrust2 — 微生物功能预测+可视化

## 四、基因组学可视化
- schneebergerlab/plotsr — 物种间共线性可视化
- moshi4/MGCplotter — 微生物基因组环状图（Circos 风格）
- ComparativeGenomicsToolkit/cactus — 泛基因组图（Minigraph-Cactus/PGGB）
- colindaven/awesome-pangenomes — 泛基因组资源
- rrwick/Bandage — 组装图可视化
- ShujiaHuang/geneview — Python 曼哈顿/QQ 图
- stephenturner/qqman — R GWAS 标准可视化

## 五、差异表达与富集分析
- DESeq2 / edgeR / limma — 火山图/MA图/热图
- fernandoguerra/GeneTonic — RNA-seq 互动可视化
- UMMs-Biocore/debrowser — 在线差异分析+可视化
- YuLab-SMU/clusterProfiler + enrichplot — GO/KEGG 气泡/点图/网络
- EnrichmentMap (Cytoscape 插件) — 富集通路网络

## 六、网络药理学与知识图谱
- cytoscape/cytoscape — 标准网络可视化（StringApp/EnrichmentMap/CellChat）
- reimandlab/ActivePathways — 多组学通路整合
- yboulaamane/awesome-drug-discovery — 药物发现工具集
- rdkit/rdkit — 化学信息学标准库
- STRING-db + Cytoscape — 蛋白互作网络

## 七、蛋白质结构与对接
- pymol-open-source / ChimeraX — 结构可视化标准
- jvogan/proteus — AI 驱动结构生物学工作流

## 八、表观遗传学与调控
- deeptools/deepTools — ChIP-seq/ATAC-seq 热图/profile
- mdozmorov/ChIP-seq_notes — 工具汇总
- al2na/methylKit — DNA 甲基化差异+可视化
- open2c/cooler + Juicebox — Hi-C 标准可视化
- mdozmorov/HiC_tools — Hi-C 工具集
- aertslab/scenicplus — pySCENIC/SCENIC+ 单细胞 GRN
- dchen-lab/CellOracle — 细胞命运+GRN 可视化

## 九、微生物组与宏基因组（肠脑轴相关）
- joey711/phyloseq — 微生物组标准分析+可视化
- cafferychen777/ggpicrust2 — 微生物功能通路可视化
- fbreitwieser/pavian — 宏基因组互动可视化
- merenlab/anvio — 综合可视化（基因组/分箱/功能）
- MetaBAT2 + Anvi'o — 分箱可视化

## 十、系统生物学与代谢
- escher/escher — 代谢通路互动可视化 + FBA
- opencobra/cobrapy — 约束代谢模型

## 十一、序列分析专用
- moshi4/pyMSAviz — 多序列比对可视化
- ViennaRNA/forgi — RNA 二级结构

## 十二、系统发育树
- YuLab-SMU/ggtree — 进化树可视化+注释
- paradispe/ape + phytools — 系统发育分析

## 十三、统计与机器学习可视化
- YingfanWang/PaCMAP — 改进版 UMAP 降维
- shap/shap — 模型可解释性
- kassambara/survminer — KM 曲线
- CamDavidsonPilon/lifelines — Python 生存分析
- xrobin/pROC — ROC 曲线

## 十四、通用绘图框架
- jokergoo/ComplexHeatmap — 复杂热图标准
- raivokolde/pheatmap — 简洁热图
- bernatgel/karyoploteR — 染色体核型图
- jtlovell/RIdeogram — 基因组映射
- upsetjs/upsetjs (UpSetR) — 集合可视化
- jverzani/VennDiagram — 韦恩图
- corybrunson/ggalluvial — 冲积/桑基图
- chris-prener/networkD3 — 互动网络
- taiyun/corrplot — 相关矩阵热图

## 十五、专科领域
- immunomind-immunology/immunarch — TCR/BCR 可视化
- WhiteWS/FlowKit — Python 流式分析
- bpteague/cytoflow — 定量流式
- cBioPortal/cbioportal — TCGA 互动
- PoisonAlien/maftools — MAF/OncoPrint/瀑布图
- liulab-dfci/MAGeCK-VISPR — CRISPR 筛选
- wdecoster/NanoPlot — 长读长质控
- cryoSPARC/RELION — Cryo-EM
- etal/cnvkit — CNV 检测+可视化
- XSLiu-Lab/LeafCutter — 可变剪接
- trhidev-arriba/arriba — 融合基因
- ImmunoLINC/Harmony — 批次校正
- igvteam/igv + gmod/jbrowse — 基因组浏览器
- PoisonAlien/trackplot — IGV 风格轨道图

## 十六、顶刊风格推荐组合（你的需求）
- 多组学 Fig2：MOFA2 因子热图 + UMAP + corrplot 网络
- 多组学 Fig3：ComplexHeatmap + clusterProfiler 气泡 + Cytoscape
- 单细胞 Fig2：Monocle3 轨迹 + scVelo 速度场 + ComplexHeatmap
- 单细胞 Fig3：CellChat 和弦 + pySCENIC 网络
- 网络药理 Fig1：Cytoscape 药物-成分-靶点 + GO/KEGG 气泡
- 网络药理 Fig3：PyMOL 分子对接 + 能量柱状图

## 十七、肠脑轴机制推荐工具链
1. 微生物组：phyloseq + ggpicrust2
2. 宿主转录组：DESeq2 + clusterProfiler
3. 多组学整合：MOFA2
4. 通路网络：Cytoscape + EnrichmentMap
5. 单细胞（肠/脑）：Seurat + CellChat
6. 时间序列：Monocle3 + scVelo

## 十八、反AI感 + 证据分级规范（强制）
- 采用：白底/强留白/真实数据驱动/非对称多面板/色盲友好(viridis,ColorBrewer)/线宽0.5-1pt
- 禁止：蓝紫渐变/霓虹发光/圆角卡片/装饰气泡/过度3D
- 证据分级：实验验证(实线★★★) / 公开数据库(虚线★★) / 预测(点线★) / 假说(灰虚线?)

## 十九、必装包
R: ggplot2, ComplexHeatmap, Seurat, clusterProfiler, MOFA2, mixOmics, ggtree, survminer
Python: scanpy, scvelo, cellrank, networkx, pyvis, shap, scikit-learn, pymol-open-source, biopython, pymsaviz, matplotlib, seaborn, plotly
