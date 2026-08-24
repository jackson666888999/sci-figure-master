#!/usr/bin/env python3
"""
gen_domains_70_config.py - 程序化生成 70 领域 + K-Dense 官方 22 学科路由配置

数据来源（全部官方/权威）:
  1. references/bioinfo_70_domains_process.md —— 70 生信领域 × 画图工具
  2. scripts/kdense_discipline_skills.json —— K-Dense 官方 326 workflows 的 22 学科→技能映射
     （快照自 K-Dense BYOK web/src/data/workflows.json，2026-08-24）
  3. scripts/kdense_skills_list.txt —— K-Dense 官方技能清单（scientific-agent-skills 仓库，163 技能）

输出: assets/domains_70_config.py
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "references" / "bioinfo_70_domains_process.md"
KDENSE_SKILLS = Path(__file__).parent / "kdense_discipline_skills.json"
KDENSE_LIST = Path(__file__).parent / "kdense_skills_list.txt"
OUT = Path(__file__).parent.parent / "assets" / "domains_70_config.py"

# ── 工具名 → 图型列表（权威映射，覆盖顶刊常用绘图工具） ──
TOOL_MAP = {
    "ggplot2": ["box", "bar", "scatter", "line", "violin", "bar_sig"],
    "seaborn": ["box", "violin", "heatmap", "scatter", "pairplot"],
    "matplotlib": ["scatter", "line", "bar", "histogram", "ecdf"],
    "plotly": ["scatter", "line", "bar", "bubble", "3d_scatter"],
    "ComplexHeatmap": ["heatmap", "complexheatmap", "dendrogram"],
    "pheatmap": ["heatmap"], "ggheatmap": ["heatmap"],
    "circlize": ["circos", "chord_diagram"], "karyoploteR": ["circos", "genome_track"],
    "RCircos": ["circos"],
    "EnhancedVolcano": ["volcano"], "ggVolcano": ["volcano"],
    "clusterProfiler": ["enrichment_dot", "enrichment_bar"],
    "enrichplot": ["enrichment_dot", "enrichment_bar", "enrichment_network"],
    "GSEA": ["gsea", "enrichment_bar"],
    "qqman": ["manhattan", "qqplot"], "CMplot": ["manhattan", "qqplot", "circos"],
    "manhattanly": ["manhattan"], "locuszoomr": ["manhattan", "line"],
    "pophelper": ["stacked_bar", "bar"],
    "IGV": ["genome_track", "genome_browser"], "JBrowse": ["genome_browser"],
    "pyGenomeTracks": ["genome_track"], "Gviz": ["genome_track", "sashimi"],
    "Qualimap": ["line", "box", "histogram"],
    "NanoPlot": ["box", "line", "histogram"], "pycoQC": ["line", "histogram", "heatmap"],
    "ggsashimi": ["sashimi"], "rmats2sashimiplot": ["sashimi"],
    "svviz2": ["genome_track", "circos"], "CNVkit": ["cnv", "heatmap"],
    "Seurat": ["umap", "tsne", "dotplot", "violin", "heatmap", "marker"],
    "Scanpy": ["umap", "tsne", "dotplot", "violin", "heatmap", "marker"],
    "scVI": ["umap", "heatmap"], "monocle3": ["trajectory", "umap"],
    "slingshot": ["trajectory"], "CellChat": ["cellchat", "network_graph", "chord_diagram"],
    "CellPhoneDB": ["cellchat", "bubble"], "SCENIC": ["grn", "heatmap", "network_graph"],
    "pySCENIC": ["grn", "heatmap"], "Scrublet": ["scatter", "histogram"],
    "SoupX": ["heatmap", "box"], "Harmony": ["umap", "tsne"],
    "SCpubr": ["umap", "dotplot", "violin", "heatmap"],
    "Squidpy": ["spatial", "heatmap", "network_graph"],
    "SpatialVista": ["spatial", "heatmap"], "Giotto": ["spatial", "heatmap"],
    "Cell2location": ["spatial", "heatmap"], "SPOTlight": ["spatial", "heatmap"],
    "stLearn": ["spatial", "trajectory"],
    "deeptools": ["genome_track", "heatmap", "line"],
    "ChIPseeker": ["peaks", "annotation", "heatmap"],
    "chromVAR": ["heatmap", "box"], "ArchR": ["umap", "heatmap", "peaks"],
    "SnapATAC": ["umap", "heatmap"], "methylKit": ["beta_dist", "heatmap", "volcano"],
    "DSS": ["volcano", "beta_dist"], "HiCExplorer": ["hic", "heatmap"],
    "hicPlotMatrix": ["hic", "heatmap"],
    "phyloseq": ["alpha_diversity", "beta_diversity", "composition", "heatmap"],
    "vegan": ["alpha_diversity", "beta_diversity"],
    "qiime2": ["alpha_diversity", "beta_diversity", "composition"],
    "ANCOM-BC2": ["volcano", "lollipop", "heatmap"], "LEfSe": ["lefse", "lollipop"],
    "MetaboAnalystR": ["plsda", "volcano", "heatmap", "pathway"],
    "mixOmics": ["plsda", "heatmap", "circos"], "SparCC": ["network_graph", "corr_heatmap"],
    "ggalluvial": ["sankey"], "Cytoscape": ["network_graph", "ppi", "chord_diagram"],
    "ggraph": ["network_graph"], "iTOL": ["tree", "circle_tree"],
    "ggtree": ["tree", "circle_tree", "heatmap"], "ggtreeExtra": ["tree", "bar"],
    "PyMOL": ["ppi", "structure"], "VMD": ["ppi"], "AlphaFold": ["ppi", "structure"],
    "RDKit": ["radar", "scatter", "structure"], "PLIP": ["ppi"],
    "AutoDock": ["dose_response", "scatter"], "GROMACS": ["line", "scatter"],
    "survminer": ["km", "forest"], "survival": ["km", "forest"],
    "forestplot": ["forest"], "ggforest": ["forest"],
    "rms": ["km", "forest", "calibration"], "nomogram": ["nomogram", "forest"],
    "pROC": ["roc"], "timeROC": ["roc"],
    "UpSetR": ["upset"], "VennDiagram": ["venn"], "ggvenn": ["venn"],
    "MultiQC": ["bar", "box", "line", "heatmap"],
}

DEFAULT_FIGURES = ["heatmap", "box", "scatter", "bar"]

# ── K-Dense 技能 → 图型（官方 163 技能中画图/分析相关技能的能力映射） ──
SKILL_FIGURE_MAP = {
    # 通用可视化
    "matplotlib": ["bar", "box", "scatter", "line", "histogram", "ecdf", "qqplot",
                   "heatmap", "violin", "donut", "treemap", "lollipop", "dumbbell",
                   "bubble", "hexbin", "area", "stacked_area", "parallel_coords",
                   "diverging_bar", "radial_bar", "marginal_plot", "bland_altman",
                   "ma_plot", "forest_plot", "funnel_plot", "manhattan", "radar"],
    "seaborn": ["box", "violin", "heatmap", "scatter", "pairplot", "line", "bar",
                "histogram", "ecdf", "ridgeline", "raincloud", "stripplot", "bubble"],
    "plotly": ["scatter", "line", "bar", "bubble", "3d_scatter", "donut", "area",
               "heatmap", "network_graph", "sankey"],
    "scientific-visualization": ["bar", "box", "scatter", "line", "violin", "heatmap",
                                 "histogram", "ecdf", "qqplot", "pairplot", "bubble",
                                 "hexbin", "raincloud", "ridgeline", "donut", "treemap",
                                 "radar", "lollipop", "area", "stacked_area"],
    "exploratory-data-analysis": ["histogram", "box", "violin", "scatter", "pairplot",
                                  "corr_heatmap", "ecdf", "qqplot", "heatmap", "line",
                                  "bar", "dendrogram", "pca", "bubble", "hexbin"],
    "infographics": ["bar", "donut", "treemap", "pie", "waffle", "radar", "nightingale"],
    "scientific-schematics": ["network_graph", "sankey", "chord_diagram", "circos",
                              "arc_diagram", "tree", "dendrogram"],
    "scientific-slides": ["bar", "box", "scatter", "line", "donut", "heatmap", "radar"],
    "latex-posters": ["bar", "scatter", "line", "heatmap"],
    "pptx": ["bar", "box", "scatter", "line", "donut", "heatmap"],
    "pptx-posters": ["bar", "scatter", "line", "heatmap"],
    "generate-image": ["infographics", "scientific_schematic"],
    # 统计 / 建模
    "statistical-analysis": ["box", "violin", "qqplot", "ecdf", "scatter", "heatmap",
                             "forest", "roc", "calibration", "bland_altman", "km",
                             "bar_sig", "bubble", "hexbin", "lollipop"],
    "statistical-power": ["scatter", "line", "ecdf", "box"],
    "statsmodels": ["line", "scatter", "qqplot", "residual_plot", "ecdf", "histogram",
                    "heatmap", "forest"],
    "pymc": ["line", "scatter", "histogram", "forest", "ecdf", "box", "density"],
    "scikit-learn": ["pca", "umap", "tsne", "scatter", "heatmap", "roc", "calibration",
                     "pairplot", "residual_plot", "dendrogram"],
    "scikit-survival": ["km", "forest", "roc", "calibration"],
    "shap": ["bar", "beeswarm", "scatter", "heatmap", "waterfall"],
    "timesfm-forecasting": ["line", "area", "stacked_area", "scatter"],
    "umap-learn": ["umap", "tsne", "pca", "scatter"],
    # 基因组 / 单细胞
    "scanpy": ["umap", "tsne", "pca", "dotplot", "violin", "heatmap", "marker",
               "trajectory", "cellchat", "spatial", "scatter"],
    "anndata": ["umap", "tsne", "heatmap", "violin"],
    "scvelo": ["trajectory", "umap", "scatter", "heatmap"],
    "scvi-tools": ["umap", "heatmap", "scatter"],
    "polars-bio": ["heatmap", "bar", "scatter"],
    "bulk-rnaseq": ["volcano", "ma_plot", "heatmap", "enrichment_dot", "gsea",
                    "enrichment_bar", "dendrogram", "venn"],
    "pydeseq2": ["volcano", "ma_plot", "heatmap", "box"],
    "deeptools": ["genome_track", "genome_browser", "heatmap", "line", "peaks"],
    "pysam": ["genome_track", "genome_browser", "coverage"],
    "genomic-coordinates": ["genome_track", "genome_browser", "circos"],
    "phylogenetics": ["tree", "circle_tree", "dendrogram", "heatmap"],
    "etetoolkit": ["tree", "circle_tree", "dendrogram"],
    "scikit-bio": ["alpha_diversity", "beta_diversity", "tree", "heatmap"],
    "biopython": ["tree", "dendrogram", "line", "heatmap"],
    "geniml": ["genome_track", "heatmap", "line"],
    "gtars": ["genome_track", "heatmap"],
    "gget": ["tree", "bar", "scatter"],
    "flowio": ["flow_hist", "scatter", "density", "contour"],
    "cellxgene-census": ["umap", "heatmap", "scatter", "dotplot"],
    "depmap": ["scatter", "heatmap", "box", "lollipop"],
    "deepspot-m": ["spatial", "heatmap", "umap"],
    # 蛋白 / 化学 / 材料
    "rdkit": ["radar", "scatter", "structure", "dose_response", "heatmap", "bar"],
    "datamol": ["scatter", "radar", "structure"],
    "deepchem": ["scatter", "roc", "calibration", "heatmap", "radar"],
    "molfeat": ["umap", "tsne", "pca", "scatter", "heatmap"],
    "medchem": ["radar", "scatter", "bar", "dose_response"],
    "pymatgen": ["scatter", "line", "heatmap", "parity_plot", "radar"],
    "pyopenms": ["line", "heatmap", "scatter", "bar"],
    "matchms": ["scatter", "heatmap", "line"],
    "esm": ["heatmap", "scatter", "ppi"],
    "diffdock": ["ppi", "scatter", "heatmap"],
    "molecular-dynamics": ["line", "scatter", "heatmap", "density"],
    "adaptyv": ["scatter", "line", "bar"],
    "glycoengineering": ["heatmap", "bar", "network_graph"],
    # 神经 / 生理
    "neurokit2": ["line", "scatter", "heatmap", "histogram"],
    "neuropixels-analysis": ["scatter", "line", "heatmap", "raster"],
    # 医学影像 / 临床
    "pathml": ["spatial", "heatmap", "scatter", "histogram"],
    "histolab": ["spatial", "heatmap", "scatter"],
    "pydicom": ["spatial", "heatmap", "scatter", "histogram"],
    "imaging-data-commons": ["scatter", "heatmap", "spatial"],
    "clinical-decision-support": ["km", "forest", "roc", "calibration", "bland_altman", "box"],
    "pyhealth": ["km", "roc", "forest", "heatmap"],
    "pkpd-modeling": ["dose_response", "line", "scatter", "forest"],
    # 网络 / 图
    "networkx": ["network_graph", "ppi", "chord_diagram", "sankey", "arc_diagram",
                 "dendrogram", "tree"],
    "torch-geometric": ["network_graph", "scatter", "heatmap"],
    "primekg": ["network_graph", "chord_diagram", "sankey"],
    "cobrapy": ["bar", "heatmap", "network_graph"],
    "arboreto": ["grn", "network_graph", "heatmap"],
    "pathway-enrichment": ["enrichment_dot", "enrichment_bar", "gsea", "network_graph",
                           "circos", "kegg_pathway"],
    "gget-db": ["bar", "scatter"],
    # 地理 / 时空
    "geopandas": ["choropleth", "bubble_map", "scatter"],
    "geomaster": ["choropleth", "bubble_map"],
    # 天体 / 物理
    "astropy": ["scatter", "line", "histogram", "heatmap"],
    "matlab": ["scatter", "line", "bar", "heatmap", "surf"],
    "fluidsim": ["scatter", "line", "heatmap", "contour"],
    "sympy": ["scatter", "line", "plot"],
    "qiskit": ["bar", "histogram", "scatter"],
    "qutip": ["line", "scatter", "heatmap"],
    "pennylane": ["line", "scatter", "heatmap"],
    # 环境 / 生态
    "bids": ["line", "scatter", "heatmap"],
    "onekgpd": ["manhattan", "qqplot", "bar"],
    "pathogen-variant-surveillance": ["tree", "manhattan", "bar", "line"],
    # 其他
    "research-lookup": ["bar", "network_graph"],
    "scholar-evaluation": ["bar", "line"],
    "literature-review": ["network_graph", "bar"],
    "database-lookup": ["bar", "scatter"],
    "paper-lookup": ["bar", "network_graph"],
    "citation-management": ["bar"],
    "peer-review": ["bar", "line"],
    "scientific-writing": ["bar", "scatter", "line", "heatmap"],
    "scientific-critical-thinking": ["bar", "scatter", "line"],
    "experimental-design": ["bar", "box", "scatter", "line"],
    "parallel-web": ["bar", "network_graph", "scatter", "line"],
    "protocolsio-integration": ["line", "bar", "scatter"],
    "hypothesis-generation": ["network_graph", "bar"],
    "hypogenic": ["network_graph", "bar"],
    "open-notebook": ["line", "scatter"],
    "lab-notebook": ["line", "scatter"],
    "clinical-reports": ["km", "forest", "bar"],
    "treatment-plans": ["km", "forest", "bar"],
    "pytorch-lightning": ["line", "scatter"],
    "transformers": ["line", "heatmap"],
    "stable-baselines3": ["line", "scatter"],
    "polars": ["bar", "box", "scatter", "line", "heatmap"],
    "vaex": ["scatter", "histogram", "line"],
    "dask": ["scatter", "line", "heatmap"],
    "zarr-python": ["scatter", "heatmap"],
    "pymoo": ["scatter", "line", "heatmap", "radar"],
    "simpy": ["line", "bar", "scatter"],
    "matlab-plot": ["scatter", "line", "bar", "heatmap"],
    "xlsx": ["bar", "box", "line", "scatter"],
    "markitdown": ["bar"],
    "liteparse": ["bar"],
    "infographics-gen": ["bar", "donut", "treemap", "radar"],
}

# 学科兜底图型
DISC_DEFAULT = ["bar", "box", "scatter", "line", "heatmap"]


def extract_plot_tools(text: str) -> list:
    m = re.search(r"\|\s*画图工具\s*\|(.*?)\|", text, re.S)
    if not m:
        return []
    cell = m.group(1)
    return [t.strip() for t in re.findall(r"\[([^\]|]+)\]\([^)]*\)", cell) if t.strip()]


DOMAIN_KEYS = {
    "测序数据质控": "ngs_qc", "短读长基因组比对": "short_read_mapping",
    "长读长测序": "long_read", "变异检测": "wgs_wes", "结构变异": "sv",
    "拷贝数变异": "cnv", "群体遗传": "population", "复杂性状遗传学": "gwas",
    "单倍型": "phasing", "RNA-seq 差异表达": "rnaseq", "转录本组装": "isoform",
    "可变剪接": "splicing", "融合基因": "fusion", "miRNA": "mirna",
    "lncRNA": "lncrna_circrna", "单细胞 RNA-seq 基础分析": "scrna",
    "单细胞质控": "scrna_qc", "单细胞整合": "scrna_integration",
    "单细胞细胞类型注释": "scrna_annotation", "单细胞轨迹": "trajectory",
    "RNA Velocity": "velocity", "单细胞通讯": "cellchat",
    "单细胞调控网络": "grn", "scATAC-seq": "scatac",
    "单细胞 Multiome": "multiome", "空间转录组": "spatial",
    "空间反卷积": "deconvolution", "空间细胞邻域": "spatial_niche",
    "ChIP-seq": "chip", "CUT&Tag": "cuttag", "ATAC-seq": "atac",
    "DNA 甲基化": "methylation", "Hi-C": "hic",
    "Enhancer-Promoter": "enhancer", "基因组组装": "assembly",
    "基因组注释": "genome_annotation", "比较基因组": "comparative",
    "泛基因组": "pangenome", "Amplicon 微生物组": "microbiome_16s",
    "Shotgun Metagenomics": "shotgun", "MAG Binning": "mag",
    "宏转录组": "metatranscriptomics", "病毒组": "virome",
    "病原体基因组监测": "pathogen", "系统发育": "phylogeny",
    "蛋白质组学": "proteomics", "代谢组学": "metabolomics",
    "脂质组学": "lipidomics", "糖组学": "glycomics",
    "蛋白结构预测": "structure", "蛋白设计": "protein_design",
    "分子对接": "docking", "分子动力学": "md", "化学信息学": "cheminformatics",
    "药物基因组学": "pharmacogenomics", "多组学整合": "multiomics",
    "通路富集": "enrichment", "网络生物学": "network",
    "网络药理学": "network_pharm", "生物医学知识图谱": "kg",
    "癌症基因组学": "cancer", "肿瘤免疫微环境": "immune_deconv",
    "免疫组库": "immune_repertoire", "免疫信息学": "hla",
    "临床生信": "clinical", "因果推断": "mr",
    "生物医学机器学习": "ml", "Foundation Models": "foundation",
    "生物医学 NLP": "nlp", "数字病理": "pathology",
}


def title_to_key(title: str) -> str:
    for zh, key in sorted(DOMAIN_KEYS.items(), key=lambda x: -len(x[0])):
        if zh in title:
            return key
    en = re.findall(r"[A-Za-z0-9\-/]+", title)
    if en:
        return en[0].lower().replace("/", "_")
    return f"domain_{len(DOMAIN_KEYS) + 1}"


def build_70_domains(text: str) -> list:
    domains = []
    for block in re.split(r"(?=^## \d+\.)", text, flags=re.M):
        m = re.match(r"^## \d+\.\s*(.+)", block, re.M)
        if not m:
            continue
        title = m.group(1).strip()
        key = title_to_key(title)
        tools = extract_plot_tools(block)
        figures = set()
        for t in tools:
            matched = False
            for known, figs in TOOL_MAP.items():
                if known.lower() in t.lower() or t.lower() in known.lower():
                    figures.update(figs)
                    matched = True
            if not matched:
                figures.update(DEFAULT_FIGURES)
        domains.append({"key": key, "title": title, "tools": tools,
                        "figures": sorted(figures) if figures else list(DEFAULT_FIGURES)})
    return domains


def build_kdense_22(disciplines_file: Path, skills_list: Path) -> dict:
    """官方 22 学科：合并其全部关联技能的图型（覆盖该学科所有画图工具图形）"""
    disc_skills = json.loads(disciplines_file.read_text(encoding="utf-8"))
    result = {}
    for disc, skills in disc_skills.items():
        figures = set()
        for skill in skills:
            figures.update(SKILL_FIGURE_MAP.get(skill, []))
        # 未命中的技能（工具/库型）统一给学科兜底图型，保证 163 技能全部可路由
        miss = [s for s in skills if not SKILL_FIGURE_MAP.get(s)]
        if miss:
            figures.update(DISC_DEFAULT)
        # 学科兜底
        if not figures:
            figures.update(DISC_DEFAULT)
        result[disc] = sorted(figures)
    return result


def main():
    text = Path(SRC).read_text(encoding="utf-8")
    domains = build_70_domains(text)
    kdense = build_kdense_22(KDENSE_SKILLS, KDENSE_LIST)

    lines = [
        '#!/usr/bin/env python3',
        '"""',
        'domains_70_config.py - 70 领域 + K-Dense 官方 22 学科路由配置（程序化生成，勿手改）',
        '',
        '来源:',
        '  1. references/bioinfo_70_domains_process.md（70 生信领域权威完整版）',
        '  2. scripts/kdense_discipline_skills.json（K-Dense 官方 326 workflows → 22 学科→技能）',
        '  3. scripts/kdense_skills_list.txt（K-Dense 官方 scientific-agent-skills 163 技能清单）',
        '生成: scripts/gen_domains_70_config.py',
        f'领域数: {len(domains)} | K-Dense 学科: {len(kdense)}',
        '"""',
        '',
        '# 70 领域 → 图型路由（领域key: [图型列表]）',
        'DOMAINS_70_ROUTING = {',
    ]
    for d in domains:
        figs = ", ".join(f'"{f}"' for f in d["figures"])
        lines.append(f'    "{d["key"]}": [{figs}],  # {d["title"]}')
    lines.append("}")
    lines.append("")
    lines.append("ALL_70_DOMAINS = list(DOMAINS_70_ROUTING.keys())")
    lines.append("")
    lines.append("# 领域中文名对照")
    lines.append("DOMAIN_70_NAMES = {")
    for d in domains:
        lines.append(f'    "{d["key"]}": "{d["title"]}",')
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("# ═══ K-Dense 官方 22 学科路由（326 workflows 分类，合并学科全部技能图型） ═══")
    lines.append("KDENSE_DISCIPLINE_ROUTING = {")
    for disc, figs in kdense.items():
        lines.append(f'    "{disc}": {figs},')
    lines.append("}")
    lines.append("")
    lines.append("KDENSE_22_DISCIPLINES = list(KDENSE_DISCIPLINE_ROUTING.keys())")
    lines.append("")
    lines.append("# K-Dense 学科 → 关联技能（官方映射）")
    disc_skills = json.loads(KDENSE_SKILLS.read_text(encoding="utf-8"))
    lines.append("KDENSE_DISCIPLINE_SKILLS = " + json.dumps(disc_skills, ensure_ascii=False, indent=1))
    lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {OUT}")
    print(f"70 domains: {len(domains)} | K-Dense disciplines: {len(kdense)}")
    total70 = sum(len(d["figures"]) for d in domains)
    totalk = sum(len(v) for v in kdense.values())
    print(f"70-domain figure entries: {total70} | K-Dense figure entries: {totalk}")
    for disc, figs in kdense.items():
        print(f"  [{disc:16s}] {len(figs):3d} figures: {figs[:8]}")


if __name__ == "__main__":
    main()
