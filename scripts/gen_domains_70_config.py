#!/usr/bin/env python3
"""
gen_domains_70_config.py - 从 bioinfo_70_domains_process.md 程序化生成 70 领域路由配置

解析 70 领域文档的"画图工具"列 → 工具名 → 图型映射 → 每个领域路由条目
输出: assets/domains_70_config.py (DOMAINS_70_ROUTING)
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "references" / "bioinfo_70_domains_process.md"
OUT = Path(__file__).parent.parent / "assets" / "domains_70_config.py"

# ── 工具名 → 图型列表（权威映射，覆盖顶刊常用绘图工具） ──
TOOL_MAP = {
    # 通用
    "ggplot2": ["box", "bar", "scatter", "line", "violin", "bar_sig"],
    "seaborn": ["box", "violin", "heatmap", "scatter", "pairplot"],
    "matplotlib": ["scatter", "line", "bar", "histogram", "ecdf"],
    "plotly": ["scatter", "line", "bar", "bubble", "3d_scatter"],
    # 热图 / 注释
    "ComplexHeatmap": ["heatmap", "complexheatmap", "dendrogram"],
    "pheatmap": ["heatmap"],
    "ggheatmap": ["heatmap"],
    # 圈图 / 基因组
    "circlize": ["circos", "chord_diagram"],
    "karyoploteR": ["circos", "genome_track"],
    "RCircos": ["circos"],
    # 火山 / 差异
    "EnhancedVolcano": ["volcano"],
    "ggVolcano": ["volcano"],
    # 富集
    "clusterProfiler": ["enrichment_dot", "enrichment_bar"],
    "enrichplot": ["enrichment_dot", "enrichment_bar", "enrichment_network"],
    "GSEA": ["gsea", "enrichment_bar"],
    # GWAS / 群体
    "qqman": ["manhattan", "qqplot"],
    "CMplot": ["manhattan", "qqplot", "circos"],
    "manhattanly": ["manhattan"],
    "locuszoomr": ["manhattan", "line"],
    "pophelper": ["stacked_bar", "bar"],
    # 基因组浏览器 / 轨道
    "IGV": ["genome_track", "genome_browser"],
    "JBrowse": ["genome_browser"],
    "pyGenomeTracks": ["genome_track"],
    "Gviz": ["genome_track", "sashimi"],
    "Qualimap": ["line", "box", "histogram"],
    # 长读长 QC
    "NanoPlot": ["box", "line", "histogram"],
    "pycoQC": ["line", "histogram", "heatmap"],
    # 剪接 / 融合
    "ggsashimi": ["sashimi"],
    "rmats2sashimiplot": ["sashimi"],
    "svviz2": ["genome_track", "circos"],
    # CNV
    "CNVkit": ["cnv", "heatmap"],
    # 单细胞
    "Seurat": ["umap", "tsne", "dotplot", "violin", "heatmap", "marker"],
    "Scanpy": ["umap", "tsne", "dotplot", "violin", "heatmap", "marker"],
    "scVI": ["umap", "heatmap"],
    "monocle3": ["trajectory", "umap"],
    "slingshot": ["trajectory"],
    "CellChat": ["cellchat", "network_graph", "chord_diagram"],
    "CellPhoneDB": ["cellchat", "bubble"],
    "SCENIC": ["grn", "heatmap", "network_graph"],
    "pySCENIC": ["grn", "heatmap"],
    "Scrublet": ["scatter", "histogram"],
    "SoupX": ["heatmap", "box"],
    "Harmony": ["umap", "tsne"],
    "scVI-tools": ["umap"],
    "SCpubr": ["umap", "dotplot", "violin", "heatmap"],
    "Azimuth": ["umap", "dotplot"],
    # 空间
    "Squidpy": ["spatial", "heatmap", "network_graph"],
    "SpatialVista": ["spatial", "heatmap"],
    "Giotto": ["spatial", "heatmap"],
    "Cell2location": ["spatial", "heatmap"],
    "SPOTlight": ["spatial", "heatmap"],
    "stLearn": ["spatial", "trajectory"],
    # 表观
    "deeptools": ["genome_track", "heatmap", "line"],
    "ChIPseeker": ["peaks", "annotation", "heatmap"],
    "chromVAR": ["heatmap", "box"],
    "ArchR": ["umap", "heatmap", "peaks"],
    "SnapATAC": ["umap", "heatmap"],
    "methylKit": ["beta_dist", "heatmap", "volcano"],
    "MethylKit": ["beta_dist", "heatmap", "volcano"],
    "DSS": ["volcano", "beta_dist"],
    "HiCExplorer": ["hic", "heatmap"],
    "hicPlotMatrix": ["hic", "heatmap"],
    "Juicebox": ["hic"],
    "washU": ["genome_track", "hic"],
    # 微生物组
    "phyloseq": ["alpha_diversity", "beta_diversity", "composition", "heatmap"],
    "vegan": ["alpha_diversity", "beta_diversity"],
    "qiime2": ["alpha_diversity", "beta_diversity", "composition"],
    "ANCOM-BC2": ["volcano", "lollipop", "heatmap"],
    "LEfSe": ["lefse", "lollipop"],
    "MetaboAnalystR": ["plsda", "volcano", "heatmap", "pathway"],
    "mixOmics": ["plsda", "heatmap", "circos"],
    "SparCC": ["network_graph", "corr_heatmap"],
    "ggalluvial": ["sankey"],
    "Cytoscape": ["network_graph", "ppi", "chord_diagram"],
    "ggraph": ["network_graph"],
    "iTOL": ["tree", "circle_tree"],
    "ggtree": ["tree", "circle_tree", "heatmap"],
    "ggtreeExtra": ["tree", "bar"],
    "Evolview": ["tree"],
    # 蛋白 / 结构 / 药物
    "PyMOL": ["ppi", "structure"],
    "VMD": ["ppi"],
    "AlphaFold": ["ppi", "structure"],
    "RDKit": ["radar", "scatter", "structure"],
    "PLIP": ["ppi"],
    "AutoDock": ["dose_response", "scatter"],
    "GROMACS": ["line", "scatter"],
    "LIGPLOT": ["ppi"],
    "ChimeraX": ["ppi"],
    # 生存 / 临床
    "survminer": ["km", "forest"],
    "survival": ["km", "forest"],
    "forestplot": ["forest"],
    "ggforest": ["forest"],
    "rms": ["km", "forest", "calibration"],
    "nomogram": ["nomogram", "forest"],
    "pROC": ["roc"],
    "timeROC": ["roc"],
    # 集合 / 网络药理学
    "UpSetR": ["upset"],
    "VennDiagram": ["venn"],
    "ggvenn": ["venn"],
    "ggVennDiagram": ["venn"],
    "clusterProfiler-circle": ["circos", "enrichment_dot"],
    # 通用兜底
    "MultiQC": ["bar", "box", "line", "heatmap"],
    "seaborn-matplotlib": ["box", "heatmap", "scatter"],
    "ggplot2-ComplexHeatmap": ["heatmap", "box", "bar"],
    "shiny": ["scatter", "line", "bar"],
    "R-shiny": ["scatter", "line"],
    "plotly-ggplot2": ["scatter", "line", "bar"],
}

# 无明确工具时的兜底图型
DEFAULT_FIGURES = ["heatmap", "box", "scatter", "bar"]

# 领域标题 → 英文路由键
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


def extract_plot_tools(text: str) -> list:
    """从领域块提取画图工具名（markdown 链接文本）"""
    m = re.search(r"\|\s*画图工具\s*\|(.*?)\|", text, re.S)
    if not m:
        return []
    cell = m.group(1)
    tools = re.findall(r"\[([^\]|]+)\]\([^)]*\)", cell)
    return [t.strip() for t in tools if t.strip()]


def title_to_key(title: str) -> str:
    """标题 → 路由键（最长 key 优先匹配，避免子串冲突如 基因组组装/宏基因组组装）"""
    for zh, key in sorted(DOMAIN_KEYS.items(), key=lambda x: -len(x[0])):
        if zh in title:
            return key
    # 取标题中的英文部分
    en = re.findall(r"[A-Za-z0-9\-/]+", title)
    if en:
        return en[0].lower().replace("/", "_")
    return f"domain_{len(DOMAIN_KEYS) + 1}"


def main():
    text = Path(SRC).read_text(encoding="utf-8")
    blocks = re.split(r"(?=^## \d+\.)", text, flags=re.M)
    domains = []
    for block in blocks:
        m = re.match(r"^## \d+\.\s*(.+)", block, re.M)
        if not m:
            continue
        title = m.group(1).strip()
        key = title_to_key(title)
        tools = extract_plot_tools(block)
        figures = set()
        for t in tools:
            # 归一化工具名匹配
            matched = False
            for known, figs in TOOL_MAP.items():
                if known.lower() in t.lower() or t.lower() in known.lower():
                    figures.update(figs)
                    matched = True
            if not matched:
                figures.update(DEFAULT_FIGURES)
        domains.append({"key": key, "title": title, "tools": tools,
                        "figures": sorted(figures) if figures else list(DEFAULT_FIGURES)})

    # 生成 Python 配置
    lines = [
        '#!/usr/bin/env python3',
        '"""',
        'domains_70_config.py - 70 领域路由配置（程序化生成，勿手改）',
        '',
        '来源: references/bioinfo_70_domains_process.md',
        '生成: scripts/gen_domains_70_config.py',
        f'领域数: {len(domains)}',
        '"""',
        '',
        '# 70 领域 → 图型路由（领域key: [图型列表]）',
        'DOMAINS_70_ROUTING = {',
    ]
    for d in domains:
        figs = ", ".join(f'"{f}"' for f in d["figures"])
        lines.append(f'    "{d["key"]}": [{figs}],  # {d["title"]} ({d["tools"][:3]})')
    lines.append("}")
    lines.append("")
    lines.append("# 领域中文名对照")
    lines.append("DOMAIN_70_NAMES = {")
    for d in domains:
        lines.append(f'    "{d["key"]}": "{d["title"]}",')
    lines.append("}")
    lines.append("")
    lines.append("ALL_70_DOMAINS = list(DOMAINS_70_ROUTING.keys())")
    lines.append("")
    lines.append("")
    lines.append("# ═══ K-Dense 22 学科绘图能力映射（官方 149 skills 分类） ═══")
    lines.append("KDENSE_DISCIPLINE_ROUTING = {")
    kdense = {
        "genomics": ["manhattan", "circos", "heatmap", "genome_track", "cnv"],
        "transcriptomics": ["volcano", "heatmap", "ma_plot", "enrichment_dot", "gsea"],
        "single-cell": ["umap", "tsne", "dotplot", "violin", "heatmap", "trajectory", "cellchat"],
        "spatial": ["spatial", "heatmap", "umap", "deconvolution"],
        "epigenomics": ["genome_track", "heatmap", "peaks", "motif", "beta_dist", "hic"],
        "metagenomics": ["alpha_diversity", "beta_diversity", "composition", "sankey", "lefse"],
        "proteomics": ["volcano", "heatmap", "venn", "ppi", "lollipop"],
        "metabolomics": ["plsda", "volcano", "heatmap", "pathway", "bland_altman"],
        "lipidomics": ["plsda", "volcano", "heatmap", "bar"],
        "glycomics": ["heatmap", "bar", "volcano"],
        "drug-discovery": ["dose_response", "ic50", "radar", "scatter", "heatmap"],
        "medicinal-chemistry": ["radar", "scatter", "structure", "dose_response"],
        "materials-science": ["scatter", "line", "heatmap", "parity_plot", "radar"],
        "chemistry": ["scatter", "line", "radar", "parity_plot"],
        "physics": ["scatter", "line", "contour_2d", "heatmap"],
        "structural-biology": ["ppi", "structure", "heatmap"],
        "clinical": ["km", "forest", "roc", "calibration", "nomogram"],
        "epidemiology": ["manhattan", "forest", "km", "bar"],
        "neuroscience": ["umap", "heatmap", "scatter", "line"],
        "plant-science": ["manhattan", "qqplot", "heatmap", "circos"],
        "immunology": ["clonotype", "umap", "heatmap", "diversity", "volcano"],
        "microbiology": ["alpha_diversity", "beta_diversity", "composition", "tree"],
    }
    for disc, figs in kdense.items():
        lines.append(f'    "{disc}": {figs},')
    lines.append("}")
    lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {OUT}")
    print(f"Domains: {len(domains)}")
    total_figs = sum(len(d["figures"]) for d in domains)
    print(f"Total figure entries: {total_figs}")
    for d in domains[:10]:
        print(f"  {d['key']:22s} <- {d['title']} -> {d['figures'][:5]}")


if __name__ == "__main__":
    main()
