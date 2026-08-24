#!/usr/bin/env python3
"""
domains_70_config.py - 70 领域 + K-Dense 官方 22 学科路由配置（程序化生成，勿手改）

来源:
  1. references/bioinfo_70_domains_process.md（70 生信领域权威完整版）
  2. scripts/kdense_discipline_skills.json（K-Dense 官方 326 workflows → 22 学科→技能）
  3. scripts/kdense_skills_list.txt（K-Dense 官方 scientific-agent-skills 163 技能清单）
生成: scripts/gen_domains_70_config.py
领域数: 70 | K-Dense 学科: 22
"""

# 70 领域 → 图型路由（领域key: [图型列表]）
DOMAINS_70_ROUTING = {
    "ngs_qc": ["bar", "bar_sig", "box", "ecdf", "heatmap", "histogram", "line", "pairplot", "scatter", "violin"],  # 测序数据质控 / NGS QC
    "short_read_mapping": ["bar", "box", "genome_browser", "genome_track", "heatmap", "histogram", "line"],  # 短读长基因组比对
    "long_read": ["box", "genome_browser", "genome_track", "heatmap", "histogram", "line"],  # 长读长测序 Nanopore / PacBio
    "wgs_wes": ["bar", "bar_sig", "box", "circos", "genome_browser", "genome_track", "line", "manhattan", "qqplot", "scatter", "violin"],  # WGS / WES SNV-Indel 变异检测
    "sv": ["chord_diagram", "circos", "genome_browser", "genome_track"],  # 结构变异 SV
    "cnv": ["chord_diagram", "circos", "cnv", "complexheatmap", "dendrogram", "genome_track", "heatmap"],  # 拷贝数变异 CNV
    "population": ["bar", "bar_sig", "box", "circos", "line", "manhattan", "qqplot", "scatter", "stacked_bar", "violin"],  # 群体遗传 / Population Genomics
    "gwas": ["circos", "line", "manhattan", "qqplot"],  # GWAS / 复杂性状遗传学
    "phasing": ["bar", "bar_sig", "box", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "manhattan", "qqplot", "scatter", "violin"],  # 单倍型 / Phasing / Imputation
    "rnaseq": ["complexheatmap", "dendrogram", "enrichment_bar", "enrichment_dot", "enrichment_network", "heatmap", "volcano"],  # RNA-seq 差异表达
    "isoform": ["genome_browser", "genome_track", "sashimi"],  # 转录本组装 / Isoform 分析
    "splicing": ["genome_browser", "genome_track", "sashimi"],  # 可变剪接 Alternative Splicing
    "fusion": ["bar", "bar_sig", "box", "chord_diagram", "circos", "genome_browser", "genome_track", "heatmap", "line", "scatter", "violin"],  # 融合基因 / Chimeric Transcript
    "mirna": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "enrichment_bar", "enrichment_dot", "heatmap", "line", "scatter", "violin", "volcano"],  # miRNA / small RNA
    "lncrna_circrna": ["bar", "bar_sig", "box", "chord_diagram", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "network_graph", "ppi", "scatter", "violin"],  # lncRNA / circRNA
    "scrna": ["bar", "box", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞 RNA-seq 基础分析
    "scrna_qc": ["bar", "bar_sig", "box", "dotplot", "heatmap", "line", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞质控 / 去双细胞 / 去环境 RNA
    "scrna_integration": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞整合 / 批次校正
    "scrna_annotation": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞细胞类型注释
    "trajectory": ["bar", "bar_sig", "box", "dotplot", "heatmap", "line", "marker", "scatter", "trajectory", "tsne", "umap", "violin"],  # 单细胞轨迹 / Pseudotime
    "velocity": ["bar", "box", "dotplot", "ecdf", "heatmap", "histogram", "line", "marker", "scatter", "tsne", "umap", "violin"],  # RNA Velocity / Fate Mapping
    "cellchat": ["bar", "box", "cellchat", "chord_diagram", "circos", "heatmap", "network_graph", "ppi", "scatter"],  # 单细胞通讯 / Cell-cell Communication
    "grn": ["bar", "box", "chord_diagram", "complexheatmap", "dendrogram", "heatmap", "network_graph", "ppi", "scatter"],  # 单细胞调控网络 / GRN / Regulon
    "scatac": ["bar", "box", "genome_track", "heatmap", "peaks", "sashimi", "scatter", "umap"],  # scATAC-seq
    "multiome": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞 Multiome / CITE-seq / 多模态
    "spatial": ["bar", "box", "dotplot", "heatmap", "marker", "network_graph", "scatter", "spatial", "tsne", "umap", "violin"],  # 空间转录组 Spatial Transcriptomics
    "deconvolution": ["bar", "dotplot", "ecdf", "heatmap", "histogram", "line", "marker", "network_graph", "scatter", "spatial", "tsne", "umap", "violin"],  # 空间反卷积 / 细胞定位
    "spatial_niche": ["cellchat", "chord_diagram", "circos", "heatmap", "network_graph", "spatial"],  # 空间细胞邻域 / Spatial Niche / 空间通讯
    "chip": ["annotation", "genome_browser", "genome_track", "heatmap", "line", "peaks"],  # ChIP-seq
    "cuttag": ["complexheatmap", "dendrogram", "genome_browser", "genome_track", "heatmap", "line"],  # CUT&Tag / CUT&RUN
    "atac": ["bar", "box", "genome_track", "heatmap", "line", "sashimi", "scatter"],  # ATAC-seq
    "methylation": ["beta_dist", "chord_diagram", "circos", "complexheatmap", "dendrogram", "genome_track", "heatmap", "sashimi", "volcano"],  # DNA 甲基化 / Bisulfite-seq
    "hic": ["bar", "box", "genome_track", "heatmap", "scatter"],  # Hi-C / 3D Genome
    "enhancer": ["chord_diagram", "complexheatmap", "dendrogram", "genome_track", "heatmap", "network_graph", "ppi", "sashimi"],  # Enhancer-Promoter / Regulatory Linking
    "assembly": ["bar", "bar_sig", "box", "heatmap", "line", "scatter", "violin"],  # 基因组组装 Genome Assembly
    "genome_annotation": ["bar", "box", "genome_browser", "heatmap", "scatter"],  # 基因组注释 Genome Annotation
    "comparative": ["bar", "box", "chord_diagram", "circos", "heatmap", "scatter"],  # 比较基因组 / 共线性
    "pangenome": ["bar", "box", "heatmap", "scatter", "upset"],  # 泛基因组 Pangenome
    "microbiome_16s": ["alpha_diversity", "bar", "beta_diversity", "box", "circle_tree", "composition", "heatmap", "scatter", "tree"],  # 16S / Amplicon 微生物组
    "shotgun": ["alpha_diversity", "bar", "bar_sig", "beta_diversity", "box", "composition", "heatmap", "line", "scatter", "violin"],  # Shotgun Metagenomics
    "mag": ["bar", "box", "circle_tree", "complexheatmap", "dendrogram", "heatmap", "scatter", "tree"],  # MAG Binning / 宏基因组组装
    "metatranscriptomics": ["alpha_diversity", "bar", "bar_sig", "beta_diversity", "box", "complexheatmap", "composition", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 宏转录组 Metatranscriptomics
    "virome": ["bar", "box", "chord_diagram", "circle_tree", "complexheatmap", "dendrogram", "heatmap", "network_graph", "ppi", "scatter", "tree"],  # Virome / 病毒组
    "pathogen": ["bar", "box", "circle_tree", "heatmap", "scatter", "tree"],  # 病原体基因组监测 / Genomic Epidemiology
    "phylogeny": ["bar", "box", "circle_tree", "heatmap", "scatter", "tree"],  # 系统发育 / Phylogenetics
    "proteomics": ["bar", "box", "complexheatmap", "dendrogram", "heatmap", "scatter", "volcano"],  # 蛋白质组学 Proteomics
    "metabolomics": ["bar", "bar_sig", "box", "chord_diagram", "heatmap", "line", "network_graph", "pathway", "plsda", "ppi", "scatter", "violin", "volcano"],  # 代谢组学 Metabolomics
    "lipidomics": ["bar", "bar_sig", "box", "chord_diagram", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 脂质组学 Lipidomics
    "glycomics": ["bar", "bar_sig", "box", "chord_diagram", "complexheatmap", "dendrogram", "heatmap", "line", "network_graph", "ppi", "scatter", "violin"],  # 糖组学 / Glycomics / Glycoproteomics
    "structure": ["bar", "box", "heatmap", "ppi", "scatter", "structure"],  # 蛋白结构预测
    "protein_design": ["bar", "bar_sig", "box", "heatmap", "line", "ppi", "scatter", "structure", "violin"],  # 蛋白设计 / Protein Design
    "docking": ["bar", "box", "heatmap", "ppi", "scatter", "structure"],  # 分子对接 / Virtual Screening
    "md": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "ppi", "scatter"],  # 分子动力学 MD
    "cheminformatics": ["bar", "box", "heatmap", "pairplot", "radar", "scatter", "structure", "violin"],  # 化学信息学 Cheminformatics
    "pharmacogenomics": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "roc", "scatter", "violin"],  # 药物基因组学 / Drug Response
    "multiomics": ["bar", "box", "circos", "complexheatmap", "dendrogram", "heatmap", "plsda", "sankey", "scatter"],  # 多组学整合
    "enrichment": ["bar", "bar_sig", "box", "enrichment_bar", "enrichment_dot", "enrichment_network", "heatmap", "line", "scatter", "violin"],  # 通路富集 / GSEA / Functional Annotation
    "network": ["bar", "box", "chord_diagram", "heatmap", "network_graph", "ppi", "scatter"],  # 网络生物学 / Biological Networks
    "network_pharm": ["chord_diagram", "circos", "network_graph", "ppi", "structure"],  # 网络药理学
    "kg": ["bar", "box", "chord_diagram", "heatmap", "network_graph", "ppi", "scatter"],  # 生物医学知识图谱 / KG
    "cancer": ["bar", "box", "complexheatmap", "dendrogram", "forest", "heatmap", "km", "scatter"],  # 癌症基因组学 / Tumor Genomics
    "immune_deconv": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 肿瘤免疫微环境 / Immune Deconvolution
    "immune_repertoire": ["bar", "box", "heatmap", "network_graph", "scatter"],  # 免疫组库 / TCR-BCR / VDJ
    "hla": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # HLA / 新抗原 / Immunoinformatics
    "clinical": ["bar", "box", "forest", "heatmap", "km", "roc", "scatter"],  # 临床生信 / 生存分析 / 预后模型
    "mr": ["bar", "bar_sig", "box", "forest", "heatmap", "line", "scatter", "violin"],  # 因果推断 / Mendelian Randomization
    "ml": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "scatter"],  # 生物医学机器学习 / Predictive Modeling
    "foundation": ["bar", "box", "heatmap", "pairplot", "scatter", "violin"],  # 生物大模型 / Foundation Models for Biology
    "nlp": ["bar", "box", "heatmap", "scatter"],  # 生物医学 NLP / 文献挖掘
    "pathology": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "scatter"],  # 数字病理 / 显微图像 / 细胞图像分析
}

ALL_70_DOMAINS = list(DOMAINS_70_ROUTING.keys())

# 领域中文名对照
DOMAIN_70_NAMES = {
    "ngs_qc": "测序数据质控 / NGS QC",
    "short_read_mapping": "短读长基因组比对",
    "long_read": "长读长测序 Nanopore / PacBio",
    "wgs_wes": "WGS / WES SNV-Indel 变异检测",
    "sv": "结构变异 SV",
    "cnv": "拷贝数变异 CNV",
    "population": "群体遗传 / Population Genomics",
    "gwas": "GWAS / 复杂性状遗传学",
    "phasing": "单倍型 / Phasing / Imputation",
    "rnaseq": "RNA-seq 差异表达",
    "isoform": "转录本组装 / Isoform 分析",
    "splicing": "可变剪接 Alternative Splicing",
    "fusion": "融合基因 / Chimeric Transcript",
    "mirna": "miRNA / small RNA",
    "lncrna_circrna": "lncRNA / circRNA",
    "scrna": "单细胞 RNA-seq 基础分析",
    "scrna_qc": "单细胞质控 / 去双细胞 / 去环境 RNA",
    "scrna_integration": "单细胞整合 / 批次校正",
    "scrna_annotation": "单细胞细胞类型注释",
    "trajectory": "单细胞轨迹 / Pseudotime",
    "velocity": "RNA Velocity / Fate Mapping",
    "cellchat": "单细胞通讯 / Cell-cell Communication",
    "grn": "单细胞调控网络 / GRN / Regulon",
    "scatac": "scATAC-seq",
    "multiome": "单细胞 Multiome / CITE-seq / 多模态",
    "spatial": "空间转录组 Spatial Transcriptomics",
    "deconvolution": "空间反卷积 / 细胞定位",
    "spatial_niche": "空间细胞邻域 / Spatial Niche / 空间通讯",
    "chip": "ChIP-seq",
    "cuttag": "CUT&Tag / CUT&RUN",
    "atac": "ATAC-seq",
    "methylation": "DNA 甲基化 / Bisulfite-seq",
    "hic": "Hi-C / 3D Genome",
    "enhancer": "Enhancer-Promoter / Regulatory Linking",
    "assembly": "基因组组装 Genome Assembly",
    "genome_annotation": "基因组注释 Genome Annotation",
    "comparative": "比较基因组 / 共线性",
    "pangenome": "泛基因组 Pangenome",
    "microbiome_16s": "16S / Amplicon 微生物组",
    "shotgun": "Shotgun Metagenomics",
    "mag": "MAG Binning / 宏基因组组装",
    "metatranscriptomics": "宏转录组 Metatranscriptomics",
    "virome": "Virome / 病毒组",
    "pathogen": "病原体基因组监测 / Genomic Epidemiology",
    "phylogeny": "系统发育 / Phylogenetics",
    "proteomics": "蛋白质组学 Proteomics",
    "metabolomics": "代谢组学 Metabolomics",
    "lipidomics": "脂质组学 Lipidomics",
    "glycomics": "糖组学 / Glycomics / Glycoproteomics",
    "structure": "蛋白结构预测",
    "protein_design": "蛋白设计 / Protein Design",
    "docking": "分子对接 / Virtual Screening",
    "md": "分子动力学 MD",
    "cheminformatics": "化学信息学 Cheminformatics",
    "pharmacogenomics": "药物基因组学 / Drug Response",
    "multiomics": "多组学整合",
    "enrichment": "通路富集 / GSEA / Functional Annotation",
    "network": "网络生物学 / Biological Networks",
    "network_pharm": "网络药理学",
    "kg": "生物医学知识图谱 / KG",
    "cancer": "癌症基因组学 / Tumor Genomics",
    "immune_deconv": "肿瘤免疫微环境 / Immune Deconvolution",
    "immune_repertoire": "免疫组库 / TCR-BCR / VDJ",
    "hla": "HLA / 新抗原 / Immunoinformatics",
    "clinical": "临床生信 / 生存分析 / 预后模型",
    "mr": "因果推断 / Mendelian Randomization",
    "ml": "生物医学机器学习 / Predictive Modeling",
    "foundation": "生物大模型 / Foundation Models for Biology",
    "nlp": "生物医学 NLP / 文献挖掘",
    "pathology": "数字病理 / 显微图像 / 细胞图像分析",
}


# ═══ K-Dense 官方 22 学科路由（326 workflows 分类，合并学科全部技能图型） ═══
KDENSE_DISCIPLINE_ROUTING = {
    "paper": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'donut', 'ecdf', 'forest', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'network_graph', 'pairplot', 'qqplot', 'radar', 'raincloud', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'treemap', 'violin'],
    "visual": ['3d_scatter', 'arc_diagram', 'area', 'bar', 'bland_altman', 'box', 'bubble', 'bubble_map', 'chord_diagram', 'choropleth', 'circos', 'corr_heatmap', 'dendrogram', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'infographics', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'nightingale', 'pairplot', 'parallel_coords', 'pca', 'pie', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'sankey', 'scatter', 'scientific_schematic', 'stacked_area', 'stripplot', 'tree', 'treemap', 'violin', 'waffle'],
    "data": ['3d_scatter', 'arc_diagram', 'area', 'bar', 'bar_sig', 'beeswarm', 'bland_altman', 'box', 'bubble', 'calibration', 'chord_diagram', 'corr_heatmap', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'stripplot', 'tree', 'treemap', 'tsne', 'umap', 'violin', 'waterfall'],
    "literature": ['arc_diagram', 'area', 'bar', 'bland_altman', 'box', 'bubble', 'chord_diagram', 'dendrogram', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'sankey', 'scatter', 'stacked_area', 'tree', 'treemap', 'violin'],
    "grants": ['area', 'bar', 'bland_altman', 'box', 'bubble', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'infographics', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'scatter', 'scientific_schematic', 'stacked_area', 'treemap', 'violin'],
    "scicomm": ['bar', 'bland_altman', 'box', 'calibration', 'forest', 'heatmap', 'km', 'line', 'network_graph', 'roc', 'scatter'],
    "genomics": ['alpha_diversity', 'arc_diagram', 'area', 'bar', 'bar_sig', 'beta_diversity', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'cellchat', 'chord_diagram', 'choropleth', 'circle_tree', 'coverage', 'dendrogram', 'diverging_bar', 'donut', 'dotplot', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'genome_browser', 'genome_track', 'grn', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'marker', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'peaks', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'roc', 'sankey', 'scatter', 'spatial', 'stacked_area', 'trajectory', 'tree', 'treemap', 'tsne', 'umap', 'violin', 'volcano'],
    "proteomics": ['arc_diagram', 'area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'chord_diagram', 'dendrogram', 'density', 'donut', 'dose_response', 'ecdf', 'forest', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'network_graph', 'pairplot', 'ppi', 'qqplot', 'radar', 'raincloud', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'structure', 'tree', 'treemap', 'violin'],
    "cellbio": ['arc_diagram', 'area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'cellchat', 'chord_diagram', 'choropleth', 'circle_tree', 'contour', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dotplot', 'dumbbell', 'ecdf', 'flow_hist', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'marker', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'roc', 'sankey', 'scatter', 'spatial', 'stacked_area', 'trajectory', 'tree', 'treemap', 'tsne', 'umap', 'violin'],
    "chemistry": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'dendrogram', 'diverging_bar', 'donut', 'dose_response', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'structure', 'treemap', 'tsne', 'umap', 'violin'],
    "drugdiscovery": ['arc_diagram', 'area', 'bar', 'bar_sig', 'beeswarm', 'bland_altman', 'box', 'bubble', 'calibration', 'chord_diagram', 'dendrogram', 'diverging_bar', 'donut', 'dose_response', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'structure', 'tree', 'treemap', 'tsne', 'umap', 'violin', 'waterfall'],
    "physics": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'contour', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'pairplot', 'parallel_coords', 'parity_plot', 'pca', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'surf', 'treemap', 'tsne', 'umap', 'violin'],
    "materials": ['area', 'bar', 'bland_altman', 'box', 'bubble', 'calibration', 'diverging_bar', 'donut', 'dose_response', 'dumbbell', 'ecdf', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'parity_plot', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'structure', 'treemap', 'violin'],
    "clinical": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'spatial', 'stacked_area', 'treemap', 'tsne', 'umap', 'violin'],
    "neuro": ['arc_diagram', 'area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'chord_diagram', 'choropleth', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'plot', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'raster', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'spatial', 'stacked_area', 'tree', 'treemap', 'tsne', 'umap', 'violin'],
    "ecology": ['alpha_diversity', 'arc_diagram', 'area', 'bar', 'bar_sig', 'beta_diversity', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'chord_diagram', 'choropleth', 'circle_tree', 'corr_heatmap', 'dendrogram', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'plot', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'tree', 'treemap', 'tsne', 'umap', 'violin', 'volcano'],
    "finance": ['area', 'bar', 'bar_sig', 'beeswarm', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'choropleth', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'infographics', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'scientific_schematic', 'stacked_area', 'treemap', 'tsne', 'umap', 'violin', 'waterfall'],
    "social": ['3d_scatter', 'arc_diagram', 'area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'bubble_map', 'calibration', 'chord_diagram', 'choropleth', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'tree', 'treemap', 'tsne', 'umap', 'violin'],
    "math": ['3d_scatter', 'arc_diagram', 'area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'chord_diagram', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'plot', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'surf', 'tree', 'treemap', 'tsne', 'umap', 'violin'],
    "ml": ['arc_diagram', 'area', 'bar', 'bar_sig', 'beeswarm', 'bland_altman', 'box', 'bubble', 'calibration', 'chord_diagram', 'corr_heatmap', 'dendrogram', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'network_graph', 'pairplot', 'parallel_coords', 'pca', 'ppi', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'sankey', 'scatter', 'stacked_area', 'tree', 'treemap', 'tsne', 'umap', 'violin', 'waterfall'],
    "engineering": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'contour', 'dendrogram', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'pairplot', 'parallel_coords', 'pca', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'surf', 'treemap', 'tsne', 'umap', 'violin'],
    "astro": ['area', 'bar', 'bar_sig', 'bland_altman', 'box', 'bubble', 'calibration', 'dendrogram', 'density', 'diverging_bar', 'donut', 'dumbbell', 'ecdf', 'forest', 'forest_plot', 'funnel_plot', 'heatmap', 'hexbin', 'histogram', 'km', 'line', 'lollipop', 'ma_plot', 'manhattan', 'marginal_plot', 'pairplot', 'parallel_coords', 'pca', 'plot', 'qqplot', 'radar', 'radial_bar', 'raincloud', 'residual_plot', 'ridgeline', 'roc', 'scatter', 'stacked_area', 'treemap', 'tsne', 'umap', 'violin'],
}

KDENSE_22_DISCIPLINES = list(KDENSE_DISCIPLINE_ROUTING.keys())

# K-Dense 学科 → 关联技能（官方映射）
KDENSE_DISCIPLINE_SKILLS = {
 "paper": [
  "citation-management",
  "literature-review",
  "parallel-web",
  "peer-review",
  "protocolsio-integration",
  "pyzotero",
  "research-lookup",
  "scientific-critical-thinking",
  "scientific-visualization",
  "scientific-writing",
  "statistical-analysis",
  "venue-templates"
 ],
 "visual": [
  "exploratory-data-analysis",
  "generate-image",
  "geomaster",
  "geopandas",
  "infographics",
  "latex-posters",
  "matplotlib",
  "networkx",
  "plotly",
  "pptx",
  "pptx-posters",
  "scientific-schematics",
  "scientific-slides",
  "scientific-visualization",
  "seaborn"
 ],
 "data": [
  "exploratory-data-analysis",
  "matplotlib",
  "networkx",
  "plotly",
  "polars",
  "pymc",
  "scientific-critical-thinking",
  "scientific-visualization",
  "scikit-learn",
  "scikit-survival",
  "seaborn",
  "shap",
  "statistical-analysis",
  "statsmodels",
  "timesfm-forecasting",
  "umap-learn"
 ],
 "literature": [
  "database-lookup",
  "literature-review",
  "market-research-reports",
  "matplotlib",
  "networkx",
  "paper-lookup",
  "parallel-web",
  "peer-review",
  "research-lookup",
  "scholar-evaluation",
  "scientific-critical-thinking",
  "scientific-visualization",
  "scientific-writing"
 ],
 "grants": [
  "generate-image",
  "matplotlib",
  "parallel-web",
  "research-grants",
  "research-lookup",
  "scientific-visualization",
  "scientific-writing",
  "what-if-oracle"
 ],
 "scicomm": [
  "clinical-decision-support",
  "parallel-web",
  "protocolsio-integration",
  "research-lookup",
  "scientific-writing"
 ],
 "genomics": [
  "anndata",
  "arboreto",
  "biopython",
  "database-lookup",
  "deeptools",
  "etetoolkit",
  "geopandas",
  "gget",
  "matplotlib",
  "networkx",
  "phylogenetics",
  "polars-bio",
  "pydeseq2",
  "pysam",
  "scanpy",
  "scientific-visualization",
  "scikit-bio",
  "scvelo",
  "statistical-analysis",
  "umap-learn"
 ],
 "proteomics": [
  "adaptyv",
  "biopython",
  "bioservices",
  "database-lookup",
  "diffdock",
  "esm",
  "molecular-dynamics",
  "networkx",
  "pyopenms",
  "rdkit",
  "rowan",
  "scientific-visualization",
  "statistical-analysis"
 ],
 "cellbio": [
  "anndata",
  "biopython",
  "cellxgene-census",
  "cobrapy",
  "database-lookup",
  "depmap",
  "etetoolkit",
  "flowio",
  "geopandas",
  "glycoengineering",
  "matplotlib",
  "networkx",
  "scanpy",
  "scientific-visualization",
  "scvelo",
  "scvi-tools",
  "statistical-analysis",
  "umap-learn"
 ],
 "chemistry": [
  "database-lookup",
  "datamol",
  "deepchem",
  "matchms",
  "matplotlib",
  "medchem",
  "molfeat",
  "parallel-web",
  "pymoo",
  "pyopenms",
  "rdkit",
  "rowan",
  "scientific-visualization",
  "scientific-writing",
  "scikit-learn",
  "statistical-analysis",
  "sympy",
  "umap-learn"
 ],
 "drugdiscovery": [
  "clinical-decision-support",
  "database-lookup",
  "deepchem",
  "diffdock",
  "market-research-reports",
  "matplotlib",
  "medchem",
  "molfeat",
  "networkx",
  "parallel-web",
  "primekg",
  "pytdc",
  "rdkit",
  "scientific-visualization",
  "scientific-writing",
  "scikit-learn",
  "shap",
  "statistical-analysis",
  "statsmodels"
 ],
 "physics": [
  "astropy",
  "cirq",
  "fluidsim",
  "matlab",
  "matplotlib",
  "molecular-dynamics",
  "pennylane",
  "pymatgen",
  "pytorch-lightning",
  "qiskit",
  "qutip",
  "scientific-visualization",
  "scikit-learn",
  "statistical-analysis",
  "sympy"
 ],
 "materials": [
  "deepchem",
  "literature-review",
  "matplotlib",
  "pymatgen",
  "pymoo",
  "rdkit",
  "scientific-visualization",
  "scientific-writing",
  "sympy",
  "what-if-oracle"
 ],
 "clinical": [
  "clinical-decision-support",
  "clinical-reports",
  "database-lookup",
  "histolab",
  "imaging-data-commons",
  "literature-review",
  "matplotlib",
  "parallel-web",
  "pathml",
  "polars",
  "pydicom",
  "pyhealth",
  "pymc",
  "pytorch-lightning",
  "research-lookup",
  "scientific-visualization",
  "scientific-writing",
  "scikit-learn",
  "scikit-survival",
  "simpy",
  "statistical-analysis",
  "statsmodels"
 ],
 "neuro": [
  "geopandas",
  "matplotlib",
  "networkx",
  "neurokit2",
  "neuropixels-analysis",
  "pydicom",
  "pymc",
  "pytorch-lightning",
  "scientific-visualization",
  "scikit-learn",
  "statistical-analysis",
  "statsmodels",
  "sympy"
 ],
 "ecology": [
  "biopython",
  "etetoolkit",
  "exploratory-data-analysis",
  "geomaster",
  "geopandas",
  "matplotlib",
  "networkx",
  "parallel-web",
  "phylogenetics",
  "pydeseq2",
  "research-lookup",
  "scientific-visualization",
  "scientific-writing",
  "scikit-bio",
  "scikit-learn",
  "statistical-analysis",
  "statsmodels",
  "sympy",
  "xlsx"
 ],
 "finance": [
  "database-lookup",
  "generate-image",
  "geopandas",
  "market-research-reports",
  "matplotlib",
  "parallel-web",
  "polars",
  "pymc",
  "pymoo",
  "scientific-critical-thinking",
  "scientific-visualization",
  "scientific-writing",
  "scikit-learn",
  "shap",
  "statistical-analysis",
  "statsmodels",
  "sympy",
  "timesfm-forecasting",
  "transformers",
  "usfiscaldata",
  "what-if-oracle",
  "xlsx"
 ],
 "social": [
  "database-lookup",
  "geopandas",
  "matplotlib",
  "networkx",
  "parallel-web",
  "plotly",
  "polars",
  "pymc",
  "scientific-visualization",
  "scikit-learn",
  "statistical-analysis",
  "statsmodels",
  "transformers"
 ],
 "math": [
  "matlab",
  "matplotlib",
  "networkx",
  "plotly",
  "pymc",
  "pymoo",
  "scientific-visualization",
  "scikit-learn",
  "statistical-analysis",
  "statsmodels",
  "sympy"
 ],
 "ml": [
  "exploratory-data-analysis",
  "matplotlib",
  "networkx",
  "polars",
  "pufferlib",
  "pytorch-lightning",
  "scientific-visualization",
  "scikit-learn",
  "shap",
  "stable-baselines3",
  "statistical-analysis",
  "torch-geometric",
  "transformers"
 ],
 "engineering": [
  "fluidsim",
  "matlab",
  "matplotlib",
  "neurokit2",
  "polars",
  "pymoo",
  "scientific-visualization",
  "scikit-learn",
  "scikit-survival",
  "simpy",
  "statistical-analysis",
  "sympy"
 ],
 "astro": [
  "astropy",
  "matplotlib",
  "pymc",
  "pytorch-lightning",
  "scientific-visualization",
  "scikit-learn",
  "statistical-analysis",
  "sympy"
 ]
}
