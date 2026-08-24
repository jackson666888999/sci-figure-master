#!/usr/bin/env python3
"""
chart_catalog.py - 100+ 图表类型统一注册表

整合三大来源：
  1. SciVizKit 83 种图表类型（src/chart_registry.py，Yang1Bai/SciVizKit）
  2. bioinfo_router 生物信息学特有图表（UMAP/tSNE/volcano/enrichment/KM 等 ~30 种）
  3. R 工具链图表（ComplexHeatmap/circlize/ggtree/survminer/clusterProfiler 等）

用法:
    from chart_catalog import CHART_CATALOG, list_charts, suggest_for_domain, get_chart
    list_charts()                     # 全部图表清单
    list_charts(domain="Biology")     # 按领域过滤
    suggest_for_domain("scRNA")       # 生物信息学领域推荐图表
    get_chart("volcano")              # 查询单个图表规格
"""

import json
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 1. SciVizKit 注册表（优先动态导入，失败则内置精简元数据）
# ─────────────────────────────────────────────────────────────
SCIVIZKIT_PATH = Path(__file__).parent / "SciVizKit" / "src"
if str(SCIVIZKIT_PATH) not in sys.path:
    sys.path.insert(0, str(SCIVIZKIT_PATH))

_SCIVIZKIT_REGISTRY = {}
try:
    from chart_registry import CHART_REGISTRY as _SCIVIZKIT_REGISTRY  # type: ignore
except Exception:
    pass

# ─────────────────────────────────────────────────────────────
# 2. 生物信息学特有图表（bioinfo_router 原生支持 + 领域标配）
# ─────────────────────────────────────────────────────────────
_BIOINFO_CHARTS = {
    # 单细胞
    "umap": {"id": "umap", "name": "UMAP Plot", "name_zh": "UMAP降维图",
             "category": "Single-Cell", "domains": ["scRNA", "Biology"],
             "engine": "Python(scanpy)", "description": "单细胞UMAP降维聚类可视化"},
    "tsne": {"id": "tsne", "name": "t-SNE Plot", "name_zh": "t-SNE降维图",
             "category": "Single-Cell", "domains": ["scRNA", "Biology"],
             "engine": "Python(scanpy)", "description": "单细胞t-SNE降维聚类可视化"},
    "pca": {"id": "pca", "name": "PCA Plot", "name_zh": "PCA主成分分析",
            "category": "Single-Cell", "domains": ["scRNA", "bulkRNA", "General"],
            "engine": "Python(scanpy/sklearn)", "description": "主成分分析降维可视化"},
    "dotplot": {"id": "dotplot", "name": "Dot Plot", "name_zh": "气泡点图",
                "category": "Single-Cell", "domains": ["scRNA", "Biology"],
                "engine": "Python(scanpy)", "description": "标记基因表达气泡图（大小=表达量，颜色=表达比例）"},
    "clustree": {"id": "clustree", "name": "Clustree", "name_zh": "聚类树图",
                 "category": "Single-Cell", "domains": ["scRNA"],
                 "engine": "R(clustree)", "description": "不同分辨率聚类结果的层级流转图"},
    "trajectory": {"id": "trajectory", "name": "Trajectory", "name_zh": "拟时序轨迹图",
                   "category": "Single-Cell", "domains": ["scRNA"],
                   "engine": "Python(scanpy)/R(monocle3)", "description": "细胞发育拟时序轨迹"},
    "cellchat": {"id": "cellchat", "name": "CellChat", "name_zh": "细胞通讯网络图",
                 "category": "Single-Cell", "domains": ["scRNA"],
                 "engine": "R(CellChat)", "description": "配体-受体介导的细胞间通讯网络"},
    "marker": {"id": "marker", "name": "Marker Genes", "name_zh": "标记基因图",
               "category": "Single-Cell", "domains": ["scRNA"],
               "engine": "Python(scanpy)", "description": "各聚类差异标记基因表达热图"},

    # 差异表达 / 组学
    "volcano": {"id": "volcano", "name": "Volcano Plot", "name_zh": "火山图",
                "category": "Differential", "domains": ["bulkRNA", "proteomics", "metabolomics", "microbiome", "Biology"],
                "engine": "Python(matplotlib)/R(EnhancedVolcano)",
                "description": "log2FC vs -log10(p) 差异表达显著性可视化"},
    "ma_plot": {"id": "ma_plot", "name": "MA Plot", "name_zh": "MA图",
                "category": "Differential", "domains": ["bulkRNA", "Biology"],
                "engine": "Python(matplotlib)", "description": "平均表达量 vs 差异倍数（M-A 散点）"},
    "gsea": {"id": "gsea", "name": "GSEA Enrichment", "name_zh": "GSEA富集图",
             "category": "Enrichment", "domains": ["bulkRNA", "Biology"],
             "engine": "R(clusterProfiler)", "description": "基因集富集分析 running score 曲线"},
    "kegg_pathway": {"id": "kegg_pathway", "name": "KEGG Pathway", "name_zh": "KEGG通路图",
                     "category": "Enrichment", "domains": ["bulkRNA", "metabolomics", "Biology"],
                     "engine": "R(clusterProfiler/pathview)", "description": "KEGG通路富集与通路映射"},
    "enrichment_bar": {"id": "enrichment_bar", "name": "Enrichment Bar", "name_zh": "富集柱状图",
                       "category": "Enrichment", "domains": ["bulkRNA", "microbiome", "Biology"],
                       "engine": "R(clusterProfiler)", "description": "GO/KEGG富集分析柱状图"},
    "enrichment_dot": {"id": "enrichment_dot", "name": "Enrichment Dot", "name_zh": "富集气泡图",
                       "category": "Enrichment", "domains": ["bulkRNA", "microbiome", "Biology"],
                       "engine": "R(clusterProfiler)", "description": "GO/KEGG富集分析气泡图"},

    # 宏基因组
    "alpha_diversity": {"id": "alpha_diversity", "name": "Alpha Diversity", "name_zh": "Alpha多样性箱线图",
                        "category": "Microbiome", "domains": ["microbiome"],
                        "engine": "Python/R(vegan)", "description": "Shannon/Chao1/Simpson 等多样性指数组间比较"},
    "beta_diversity": {"id": "beta_diversity", "name": "Beta Diversity", "name_zh": "Beta多样性PCoA图",
                       "category": "Microbiome", "domains": ["microbiome"],
                       "engine": "Python(sklearn)/R(vegan)", "description": "Bray-Curtis 等距离的 PCoA/NMDS 降维"},
    "composition": {"id": "composition", "name": "Composition", "name_zh": "物种组成堆叠图",
                    "category": "Microbiome", "domains": ["microbiome"],
                    "engine": "Python(matplotlib)/R(phyloseq)", "description": "门/属水平物种相对丰度堆叠柱状图"},
    "lefse": {"id": "lefse", "name": "LEfSe", "name_zh": "LEfSe差异分析图",
              "category": "Microbiome", "domains": ["microbiome"],
              "engine": "R/LEfSe", "description": "线性判别分析效应量（LDA score 柱状图）"},

    # 基因组
    "genome_browser": {"id": "genome_browser", "name": "Genome Browser", "name_zh": "基因组浏览器轨道图",
                       "category": "Genomics", "domains": ["genome"],
                       "engine": "pyGenomeTracks", "description": "基因组坐标上的信号轨道（覆盖/峰）"},
    "genome_track": {"id": "genome_track", "name": "Genome Track", "name_zh": "基因组轨道图",
                     "category": "Genomics", "domains": ["genome"],
                     "engine": "pyGenomeTracks/Gviz", "description": "多轨道基因组可视化"},
    "cnv": {"id": "cnv", "name": "CNV Plot", "name_zh": "拷贝数变异图",
            "category": "Genomics", "domains": ["genome"],
            "engine": "cnvkit", "description": "染色体拷贝数变异热图/散点"},
    "circos": {"id": "circos", "name": "Circos Plot", "name_zh": "圈图",
               "category": "Genomics", "domains": ["genome", "scRNA", "Biology"],
               "engine": "R(circlize)", "description": "环形基因组/多组学关联圈图"},
    "manhattan": {"id": "manhattan", "name": "Manhattan Plot", "name_zh": "曼哈顿图",
                  "category": "Genomics", "domains": ["genome", "Biology"],
                  "engine": "Python(matplotlib)", "description": "GWAS 全基因组关联显著性图"},

    # 系统发育
    "tree": {"id": "tree", "name": "Phylogenetic Tree", "name_zh": "系统发育树",
             "category": "Phylogeny", "domains": ["phylogeny"],
             "engine": "R(ggtree)", "description": "物种/基因系统发育进化树"},
    "circle_tree": {"id": "circle_tree", "name": "Circle Tree", "name_zh": "环形系统发育树",
                    "category": "Phylogeny", "domains": ["phylogeny"],
                    "engine": "R(ggtree)", "description": "环形布局系统发育树"},

    # 生存分析
    "km": {"id": "km", "name": "Kaplan-Meier", "name_zh": "Kaplan-Meier生存曲线",
           "category": "Survival", "domains": ["survival", "Medicine", "Biology"],
           "engine": "Python(lifelines)/R(survminer)", "description": "生存曲线 + log-rank 检验"},
    "forest": {"id": "forest", "name": "Forest Plot", "name_zh": "森林图",
               "category": "Survival", "domains": ["survival", "Medicine"],
               "engine": "Python(matplotlib)/R(forestplot)", "description": "Cox 回归/荟萃分析效应量森林图"},

    # 表观 / 代谢 / 蛋白
    "peaks": {"id": "peaks", "name": "Peak Annotation", "name_zh": "峰注释分布图",
              "category": "Epigenetics", "domains": ["epigenetic"],
              "engine": "R(ChIPseeker)", "description": "ChIP-seq 峰在基因组特征上的分布"},
    "pathway": {"id": "pathway", "name": "Metabolic Pathway", "name_zh": "代谢通路图",
                "category": "Metabolomics", "domains": ["metabolomics"],
                "engine": "Python(matplotlib)/R(MetaboAnalystR)", "description": "代谢物富集通路图"},
    "plsda": {"id": "plsda", "name": "PLS-DA", "name_zh": "偏最小二乘判别分析",
              "category": "Metabolomics", "domains": ["metabolomics"],
              "engine": "R(mixOmics)", "description": "代谢组监督判别分析得分图"},
    "oplsda": {"id": "oplsda", "name": "OPLS-DA", "name_zh": "正交偏最小二乘判别分析",
               "category": "Metabolomics", "domains": ["metabolomics"],
               "engine": "R(mixOmics)", "description": "正交偏最小二乘判别分析"},
    "venn": {"id": "venn", "name": "Venn Diagram", "name_zh": "韦恩图",
             "category": "Set", "domains": ["bulkRNA", "proteomics", "metabolomics", "General"],
             "engine": "Python(matplotlib_venn)", "description": "多组差异基因/代谢物交集"},
    "upset": {"id": "upset", "name": "UpSet Plot", "name_zh": "UpSet交集图",
              "category": "Set", "domains": ["bulkRNA", "proteomics", "General"],
              "engine": "Python(upsetplot)", "description": "3+ 组集合交集可视化"},
    "sankey": {"id": "sankey", "name": "Sankey Diagram", "name_zh": "桑基图",
               "category": "Flow", "domains": ["microbiome", "metabolomics", "General", "Biology"],
               "engine": "Python(matplotlib)/R(ggalluvial)", "description": "分类/丰度层级流转图"},
    "rna_velocity": {"id": "rna_velocity", "name": "RNA Velocity", "name_zh": "RNA速率图",
                     "category": "Single-Cell", "domains": ["scRNA"],
                     "engine": "Python(scvelo)", "description": "RNA 剪接动力学速率向量场"},
    "wgcna": {"id": "wgcna", "name": "WGCNA", "name_zh": "加权基因共表达网络",
              "category": "Network", "domains": ["bulkRNA"],
              "engine": "R(WGCNA)", "description": "模块-性状关联热图与共表达网络"},
    "motif": {"id": "motif", "name": "Motif Enrichment", "name_zh": "转录因子Motif富集图",
              "category": "Epigenetics", "domains": ["epigenetic"],
              "engine": "R/meme", "description": "转录因子结合基序富集分析"},
    "mofa": {"id": "mofa", "name": "MOFA", "name_zh": "多组学因子分析",
             "category": "Multi-omics", "domains": ["multiomics"],
             "engine": "R(MOFA2)", "description": "多组学数据因子分解与解释"},
    "spatial": {"id": "spatial", "name": "Spatial Transcriptomics", "name_zh": "空间转录组图",
                "category": "Spatial", "domains": ["spatial"],
                "engine": "Python(Squidpy)/R(SpatialVista)", "description": "组织切片上的基因表达空间分布"},
    "heatmap_complex": {"id": "heatmap_complex", "name": "Complex Heatmap", "name_zh": "ComplexHeatmap复合热图",
                        "category": "Heatmap", "domains": ["bulkRNA", "scRNA", "multiomics"],
                        "engine": "R(ComplexHeatmap)", "description": "带注释栏/聚类树的高级复合热图"},
    "chromatin_loop": {"id": "chromatin_loop", "name": "Chromatin Loop", "name_zh": "染色质环图",
                       "category": "Epigenetics", "domains": ["epigenetic"],
                       "engine": "pyGenomeTracks/HiCExplorer", "description": "Hi-C 染色质相互作用环图"},
}

# ─────────────────────────────────────────────────────────────
# 3. R 工具链图表（依赖 R + Bioconductor）
# ─────────────────────────────────────────────────────────────
_R_TOOL_CHARTS = {
    "r_heatmap": {"id": "r_heatmap", "name": "R ComplexHeatmap", "name_zh": "R复合热图",
                  "category": "R-Toolkit", "domains": ["bulkRNA", "scRNA", "multiomics"],
                  "engine": "R(ComplexHeatmap)", "description": "Bioconductor ComplexHeatmap 顶刊级热图"},
    "r_circlize": {"id": "r_circlize", "name": "R Circos", "name_zh": "R圈图",
                   "category": "R-Toolkit", "domains": ["genome", "multiomics"],
                   "engine": "R(circlize)", "description": "circlize 包基因组/关联圈图"},
    "r_ggtree": {"id": "r_ggtree", "name": "R Ggtree", "name_zh": "R系统发育树",
                 "category": "R-Toolkit", "domains": ["phylogeny"],
                 "engine": "R(ggtree)", "description": "ggtree 高级系统发育树可视化"},
    "r_survminer": {"id": "r_survminer", "name": "R Survminer", "name_zh": "R生存分析",
                    "category": "R-Toolkit", "domains": ["survival"],
                    "engine": "R(survminer)", "description": "survminer 出版级生存曲线"},
    "r_clusterprofiler": {"id": "r_clusterprofiler", "name": "R ClusterProfiler", "name_zh": "R富集分析",
                          "category": "R-Toolkit", "domains": ["bulkRNA", "microbiome"],
                          "engine": "R(clusterProfiler)", "description": "clusterProfiler GO/KEGG富集可视化"},
    "r_enhancedvolcano": {"id": "r_enhancedvolcano", "name": "R EnhancedVolcano", "name_zh": "R火山图",
                          "category": "R-Toolkit", "domains": ["bulkRNA", "proteomics", "metabolomics"],
                          "engine": "R(EnhancedVolcano)", "description": "EnhancedVolcano 出版级火山图"},
    "r_cellchat": {"id": "r_cellchat", "name": "R CellChat", "name_zh": "R细胞通讯",
                   "category": "R-Toolkit", "domains": ["scRNA"],
                   "engine": "R(CellChat)", "description": "CellChat 细胞通讯网络分析"},
    "r_metaboanalyst": {"id": "r_metaboanalyst", "name": "R MetaboAnalystR", "name_zh": "R代谢组分析",
                        "category": "R-Toolkit", "domains": ["metabolomics"],
                        "engine": "R(MetaboAnalystR)", "description": "MetaboAnalystR 代谢组全套分析"},
    "r_mofa": {"id": "r_mofa", "name": "R MOFA2", "name_zh": "R多组学因子分析",
               "category": "R-Toolkit", "domains": ["multiomics"],
               "engine": "R(MOFA2)", "description": "MOFA2 多组学因子分析可视化"},
    "r_mixomics": {"id": "r_mixomics", "name": "R mixOmics", "name_zh": "R多组学集成",
                   "category": "R-Toolkit", "domains": ["multiomics", "metabolomics"],
                   "engine": "R(mixOmics)", "description": "mixOmics DIABLO/sPLS-DA 多组学集成"},
    "r_chipseeker": {"id": "r_chipseeker", "name": "R ChIPseeker", "name_zh": "R峰注释",
                     "category": "R-Toolkit", "domains": ["epigenetic"],
                     "engine": "R(ChIPseeker)", "description": "ChIPseeker 峰注释与分布可视化"},
    "r_phyloseq": {"id": "r_phyloseq", "name": "R Phyloseq", "name_zh": "R宏基因组",
                   "category": "R-Toolkit", "domains": ["microbiome"],
                   "engine": "R(phyloseq)", "description": "phyloseq 微生物组生态分析可视化"},
    "r_flowcore": {"id": "r_flowcore", "name": "R flowCore", "name_zh": "R流式分析",
                   "category": "R-Toolkit", "domains": ["flow"],
                   "engine": "R(flowCore)", "description": "flowCore 流式细胞术数据分析"},
    "r_survival_forest": {"id": "r_survival_forest", "name": "R Survival Forest", "name_zh": "R生存森林图",
                          "category": "R-Toolkit", "domains": ["survival"],
                          "engine": "R(survival/survminer)", "description": "Cox 回归森林图"},
    "r_animalcules": {"id": "r_animalcules", "name": "R Animalcules", "name_zh": "R微生物组交互",
                      "category": "R-Toolkit", "domains": ["microbiome"],
                      "engine": "R(animalcules)", "description": "animalcules 微生物组交互式分析"},
    "r_ggalluvial": {"id": "r_ggalluvial", "name": "R ggalluvial", "name_zh": "R冲积图",
                     "category": "R-Toolkit", "domains": ["microbiome", "General"],
                     "engine": "R(ggalluvial)", "description": "ggalluvial 冲积图（多层级流转）"},
    "r_scpubr": {"id": "r_scpubr", "name": "R scPubR", "name_zh": "R单细胞出版图",
                 "category": "R-Toolkit", "domains": ["scRNA"],
                 "engine": "R(scPubR)", "description": "单细胞出版级 ggplot 封装"},
    "r_wgcna": {"id": "r_wgcna", "name": "R WGCNA", "name_zh": "R共表达网络",
                "category": "R-Toolkit", "domains": ["bulkRNA"],
                "engine": "R(WGCNA)", "description": "WGCNA 加权共表达网络模块分析"},
    "r_glmnet": {"id": "r_glmnet", "name": "R Lasso/Cox", "name_zh": "R Lasso回归",
                 "category": "R-Toolkit", "domains": ["bulkRNA", "Medicine"],
                 "engine": "R(glmnet)", "description": "Lasso-Cox 特征筛选与风险模型"},
    "r_deseq2": {"id": "r_deseq2", "name": "R DESeq2", "name_zh": "R差异表达",
                 "category": "R-Toolkit", "domains": ["bulkRNA"],
                 "engine": "R(DESeq2)", "description": "DESeq2 差异表达分析 MA/火山图"},
    "r_edger": {"id": "r_edger", "name": "R edgeR", "name_zh": "R差异表达",
                "category": "R-Toolkit", "domains": ["bulkRNA"],
                "engine": "R(edgeR)", "description": "edgeR 差异表达分析"},
}

# ─────────────────────────────────────────────────────────────
# 4. 学术演示/汇报图表（Quarto/Reveal.js/Marp/Beamer/Slidev）
# ─────────────────────────────────────────────────────────────
_PRESENTATION_CHARTS = {
    "academic_ppt": {"id": "academic_ppt", "name": "Academic PPT (Quarto/Beamer)", "name_zh": "学术汇报PPT",
                     "category": "Presentation", "domains": ["academic", "report", "meeting", "General"],
                     "engine": "Quarto/Beamer", "description": "学术汇报/组会演示文稿（Quarto revealjs/pptx 或 LaTeX Beamer）"},
    "quarto_slides": {"id": "quarto_slides", "name": "Quarto Slides", "name_zh": "Quarto幻灯片",
                      "category": "Presentation", "domains": ["academic", "report"],
                      "engine": "Quarto", "description": "R/Python 数据驱动学术幻灯片（revealjs/pptx/pdf 多输出），组会/课程标配"},
    "reveal_slides": {"id": "reveal_slides", "name": "Reveal.js Slides", "name_zh": "Reveal.js网页演示",
                      "category": "Presentation", "domains": ["academic", "report", "web"],
                      "engine": "Reveal.js", "description": "HTML5 演示框架（hakimel/reveal.js 72k★），交互图表、数学公式、代码高亮"},
    "marp_slides": {"id": "marp_slides", "name": "Marp Slides", "name_zh": "Marp幻灯片",
                    "category": "Presentation", "domains": ["academic", "report"],
                    "engine": "Marp", "description": "Markdown 一键转 PPT/PDF（kaisugi/marp-theme-academic 学术主题 278★）"},
    "beamer_slides": {"id": "beamer_slides", "name": "LaTeX Beamer", "name_zh": "LaTeX Beamer演示",
                      "category": "Presentation", "domains": ["academic", "report"],
                      "engine": "LaTeX", "description": "学术讲座/答辩标准模板（SunYanCN/Latex-Beamer-Template 中文模板 287★）"},
    "slidev_slides": {"id": "slidev_slides", "name": "Slidev", "name_zh": "Slidev演示",
                      "category": "Presentation", "domains": ["report", "web"],
                      "engine": "Slidev", "description": "Markdown 驱动的开发者演示框架（slidevjs/slidev 48k★），代码/图表友好"},
    "labmeeting_slides": {"id": "labmeeting_slides", "name": "Lab Meeting Slides", "name_zh": "组会汇报模板",
                          "category": "Presentation", "domains": ["meeting", "academic"],
                          "engine": "Marp/Quarto", "description": "组会/文献汇报模板（robonuggets/marp-slides 22 示例 deck，含数据面板）"},
    "poster": {"id": "poster", "name": "Academic Poster", "name_zh": "学术海报",
               "category": "Presentation", "domains": ["academic", "conference"],
               "engine": "Quarto/LaTeX/HTML", "description": "会议海报（Quarto poster / beamerposter / reveal.js poster）"},
}

# ─────────────────────────────────────────────────────────────
# 5. 汇总注册表（SciVizKit + Bioinfo + R 工具链 + Presentation）
# ─────────────────────────────────────────────────────────────
CHART_CATALOG = {}

# 合并 SciVizKit（标记 engine/来源）
for cid, meta in _SCIVIZKIT_REGISTRY.items():
    meta = dict(meta)
    meta["id"] = cid
    meta.setdefault("engine", "SciVizKit(Python)")
    meta["source"] = "SciVizKit"
    CHART_CATALOG[cid] = meta

# 合并 bioinfo 特有
for cid, meta in _BIOINFO_CHARTS.items():
    meta = dict(meta)
    meta["id"] = cid
    meta["source"] = "bioinfo-router"
    CHART_CATALOG[cid] = meta

# 合并 R 工具链
for cid, meta in _R_TOOL_CHARTS.items():
    meta = dict(meta)
    meta["id"] = cid
    meta["source"] = "R-toolkit"
    CHART_CATALOG[cid] = meta

# 合并演示文稿
for cid, meta in _PRESENTATION_CHARTS.items():
    meta = dict(meta)
    meta["id"] = cid
    meta["source"] = "presentation"
    CHART_CATALOG[cid] = meta


# ─────────────────────────────────────────────────────────────
# 5. 查询 API
# ─────────────────────────────────────────────────────────────
def list_charts(domain: str = None, category: str = None) -> list:
    """列出图表（可按领域/类别过滤），返回 id 列表"""
    out = []
    for cid, meta in CHART_CATALOG.items():
        if domain:
            doms = [d.lower() for d in meta.get("domains", [])]
            if domain.lower() not in doms:
                continue
        if category:
            if meta.get("category", "").lower() != category.lower():
                continue
        out.append(cid)
    return sorted(out)


def get_chart(chart_id: str) -> dict:
    """查询单个图表规格（大小写不敏感）"""
    cid = chart_id.lower().strip()
    if cid in CHART_CATALOG:
        return CHART_CATALOG[cid]
    for k, v in CHART_CATALOG.items():
        if k.lower() == cid:
            return v
    return None


def suggest_for_domain(domain: str, top_n: int = 10) -> list:
    """按生物信息学领域推荐图表（智能推荐决策树的一级路由）"""
    domain = domain.lower().strip()
    mapping = {
        "scrna": ["umap", "tsne", "dotplot", "violin", "marker", "heatmap",
                  "trajectory", "cellchat", "rna_velocity", "spatial", "r_cellchat"],
        "bulkrna": ["volcano", "ma_plot", "gsea", "kegg_pathway", "heatmap",
                    "enrichment_bar", "wgcna", "venn", "r_deseq2", "r_clusterprofiler"],
        "microbiome": ["alpha_diversity", "beta_diversity", "composition", "lefse",
                       "sankey", "heatmap", "volcano", "r_phyloseq", "r_animalcules", "r_ggalluvial"],
        "metabolomics": ["plsda", "oplsda", "volcano", "pathway", "sankey", "heatmap",
                         "r_metaboanalyst", "r_mixomics", "venn"],
        "proteomics": ["volcano", "heatmap", "venn", "upset", "r_enhancedvolcano", "r_clusterprofiler"],
        "genome": ["genome_browser", "genome_track", "cnv", "circos", "manhattan", "r_circlize"],
        "phylogeny": ["tree", "circle_tree", "r_ggtree", "heatmap"],
        "survival": ["km", "forest", "r_survminer", "r_survival_forest", "r_glmnet"],
        "enrichment": ["enrichment_bar", "enrichment_dot", "gsea", "kegg_pathway", "r_clusterprofiler"],
        "epigenetic": ["peaks", "motif", "chromatin_loop", "r_chipseeker"],
        "multiomics": ["mofa", "heatmap_complex", "r_mofa", "r_mixomics", "circos", "r_circlize"],
        "spatial": ["spatial", "umap", "heatmap"],
        "flow": ["r_flowcore"],
        "general": ["histogram", "kde", "boxplot", "violin", "scatter", "line",
                    "bar", "heatmap", "corr_heatmap", "radar"],
    }
    # 全目录匹配（SciVizKit domains 含 Biology 等）
    if domain in mapping:
        return mapping[domain][:top_n]
    # 尝试在 SciVizKit 领域名中匹配
    for cid, meta in CHART_CATALOG.items():
        if any(domain in d.lower() for d in meta.get("domains", [])):
            return list_charts()[:top_n]
    return list_charts()[:top_n]


def count_charts() -> dict:
    """统计图表总数（按来源分类）"""
    stats = {"total": len(CHART_CATALOG), "by_source": {}, "by_category": {}}
    for cid, meta in CHART_CATALOG.items():
        src = meta.get("source", "unknown")
        stats["by_source"][src] = stats["by_source"].get(src, 0) + 1
        cat = meta.get("category", "Other")
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
    return stats


def to_json(path: str = None) -> str:
    """导出 JSON（可选写文件）"""
    text = json.dumps(CHART_CATALOG, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    stats = count_charts()
    print("=" * 60)
    print("Chart Catalog Summary")
    print("=" * 60)
    print(f"Total chart types: {stats['total']}")
    print(f"By source: {stats['by_source']}")
    print(f"By category: {stats['by_category']}")
    print("\nSample domains:")
    for dom in ["scRNA", "bulkRNA", "microbiome", "metabolomics", "survival"]:
        rec = suggest_for_domain(dom, top_n=6)
        print(f"  {dom:15s} -> {rec}")
    print("\nAll chart ids:")
    print(", ".join(list_charts()))
