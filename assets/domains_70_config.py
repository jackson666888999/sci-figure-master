#!/usr/bin/env python3
"""
domains_70_config.py - 70 领域路由配置（程序化生成，勿手改）

来源: references/bioinfo_70_domains_process.md
生成: scripts/gen_domains_70_config.py
领域数: 70
"""

# 70 领域 → 图型路由（领域key: [图型列表]）
DOMAINS_70_ROUTING = {
    "ngs_qc": ["bar", "bar_sig", "box", "ecdf", "heatmap", "histogram", "line", "pairplot", "scatter", "violin"],  # 测序数据质控 / NGS QC (['MultiQC', 'ggplot2', 'seaborn'])
    "short_read_mapping": ["bar", "box", "genome_browser", "genome_track", "heatmap", "histogram", "line"],  # 短读长基因组比对 (['MultiQC', 'Qualimap', 'IGV'])
    "long_read": ["box", "genome_browser", "genome_track", "heatmap", "histogram", "line"],  # 长读长测序 Nanopore / PacBio (['NanoPlot', 'pycoQC', 'IGV'])
    "wgs_wes": ["bar", "bar_sig", "box", "circos", "genome_browser", "genome_track", "heatmap", "line", "manhattan", "qqplot", "scatter", "violin"],  # WGS / WES SNV-Indel 变异检测 (['IGV', 'CMplot', 'karyoploteR'])
    "sv": ["chord_diagram", "circos", "genome_browser", "genome_track"],  # 结构变异 SV (['svviz2', 'IGV', 'circlize'])
    "cnv": ["bar", "box", "chord_diagram", "circos", "cnv", "complexheatmap", "dendrogram", "genome_track", "heatmap"],  # 拷贝数变异 CNV (['CNVkit', 'ComplexHeatmap', 'karyoploteR'])
    "population": ["bar", "bar_sig", "box", "circos", "heatmap", "line", "manhattan", "qqplot", "scatter", "stacked_bar", "violin"],  # 群体遗传 / Population Genomics (['pophelper', 'qqman', 'CMplot'])
    "gwas": ["circos", "line", "manhattan", "qqplot"],  # GWAS / 复杂性状遗传学 (['qqman', 'CMplot', 'manhattanly'])
    "phasing": ["bar", "bar_sig", "box", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "manhattan", "qqplot", "scatter", "violin"],  # 单倍型 / Phasing / Imputation (['ggplot2', 'CMplot', 'ComplexHeatmap'])
    "rnaseq": ["bar", "box", "circos", "complexheatmap", "dendrogram", "enrichment_bar", "enrichment_dot", "enrichment_network", "heatmap", "volcano"],  # RNA-seq 差异表达 (['EnhancedVolcano', 'ComplexHeatmap', 'clusterProfiler'])
    "isoform": ["genome_browser", "genome_track", "sashimi"],  # 转录本组装 / Isoform 分析 (['ggsashimi', 'IGV', 'Gviz'])
    "splicing": ["genome_browser", "genome_track", "sashimi"],  # 可变剪接 Alternative Splicing (['rmats2sashimiplot', 'ggsashimi', 'IGV'])
    "fusion": ["bar", "bar_sig", "box", "chord_diagram", "circos", "genome_browser", "genome_track", "heatmap", "line", "scatter", "violin"],  # 融合基因 / Chimeric Transcript (['Arriba', 'IGV', 'circlize'])
    "mirna": ["bar", "bar_sig", "box", "circos", "complexheatmap", "dendrogram", "enrichment_bar", "enrichment_dot", "heatmap", "line", "scatter", "violin", "volcano"],  # miRNA / small RNA (['ggplot2', 'ComplexHeatmap', 'EnhancedVolcano'])
    "lncrna_circrna": ["bar", "bar_sig", "box", "chord_diagram", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "network_graph", "ppi", "scatter", "violin"],  # lncRNA / circRNA (['circlize', 'ComplexHeatmap', 'Cytoscape'])
    "scrna": ["bar", "box", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞 RNA-seq 基础分析 (['Seurat', 'Scanpy', 'scCustomize'])
    "scrna_qc": ["bar", "bar_sig", "box", "dotplot", "heatmap", "line", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞质控 / 去双细胞 / 去环境 RNA (['Seurat', 'Scanpy', 'scater'])
    "scrna_integration": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞整合 / 批次校正 (['Seurat', 'Scanpy', 'scIB'])
    "scrna_annotation": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞细胞类型注释 (['Seurat DotPlot', 'Scanpy', 'dittoSeq'])
    "trajectory": ["bar", "bar_sig", "box", "dotplot", "heatmap", "line", "marker", "scatter", "trajectory", "tsne", "umap", "violin"],  # 单细胞轨迹 / Pseudotime (['Monocle3', 'Scanpy', 'tradeSeq'])
    "velocity": ["bar", "box", "dotplot", "ecdf", "heatmap", "histogram", "line", "marker", "scatter", "tsne", "umap", "violin"],  # RNA Velocity / Fate Mapping (['scVelo', 'CellRank', 'matplotlib'])
    "cellchat": ["bar", "box", "cellchat", "chord_diagram", "circos", "heatmap", "network_graph", "ppi", "scatter"],  # 单细胞通讯 / Cell-cell Communication (['CellChat', 'LIANA', 'circlize'])
    "grn": ["bar", "box", "chord_diagram", "complexheatmap", "dendrogram", "heatmap", "network_graph", "ppi", "scatter"],  # 单细胞调控网络 / GRN / Regulon (['Cytoscape', 'ComplexHeatmap', 'ggraph'])
    "scatac": ["bar", "box", "genome_track", "heatmap", "peaks", "sashimi", "scatter", "umap"],  # scATAC-seq (['Signac', 'ArchR', 'pyGenomeTracks'])
    "multiome": ["bar", "box", "complexheatmap", "dendrogram", "dotplot", "heatmap", "marker", "scatter", "tsne", "umap", "violin"],  # 单细胞 Multiome / CITE-seq / 多模态 (['Seurat', 'muon', 'Scanpy'])
    "spatial": ["bar", "box", "dotplot", "heatmap", "marker", "network_graph", "scatter", "spatial", "tsne", "umap", "violin"],  # 空间转录组 Spatial Transcriptomics (['Squidpy', 'Giotto', 'Seurat'])
    "deconvolution": ["bar", "box", "dotplot", "ecdf", "heatmap", "histogram", "line", "marker", "network_graph", "scatter", "spatial", "tsne", "umap", "violin"],  # 空间反卷积 / 细胞定位 (['Squidpy', 'Giotto', 'Seurat'])
    "spatial_niche": ["cellchat", "chord_diagram", "circos", "heatmap", "network_graph", "spatial"],  # 空间细胞邻域 / Spatial Niche / 空间通讯 (['Squidpy', 'Giotto', 'CellChat'])
    "chip": ["annotation", "genome_browser", "genome_track", "heatmap", "line", "peaks"],  # ChIP-seq (['deepTools', 'pyGenomeTracks', 'ChIPseeker'])
    "cuttag": ["bar", "box", "complexheatmap", "dendrogram", "genome_browser", "genome_track", "heatmap", "line"],  # CUT&Tag / CUT&RUN (['deepTools', 'pyGenomeTracks', 'ComplexHeatmap'])
    "atac": ["bar", "box", "genome_track", "heatmap", "line", "sashimi", "scatter"],  # ATAC-seq (['deepTools', 'TOBIAS', 'pyGenomeTracks'])
    "methylation": ["bar", "beta_dist", "box", "chord_diagram", "circos", "complexheatmap", "dendrogram", "genome_track", "heatmap", "sashimi", "volcano"],  # DNA 甲基化 / Bisulfite-seq (['methylKit', 'Gviz', 'ComplexHeatmap'])
    "hic": ["bar", "box", "genome_track", "heatmap", "hic", "scatter"],  # Hi-C / 3D Genome (['HiGlass', 'Juicebox', 'cooltools'])
    "enhancer": ["bar", "box", "chord_diagram", "complexheatmap", "dendrogram", "genome_track", "heatmap", "network_graph", "ppi", "sashimi"],  # Enhancer-Promoter / Regulatory Linking (['pyGenomeTracks', 'Gviz', 'Cytoscape'])
    "assembly": ["bar", "bar_sig", "box", "heatmap", "line", "scatter", "violin"],  # 基因组组装 Genome Assembly (['QUAST', 'Bandage', 'gfatools'])
    "genome_annotation": ["bar", "box", "genome_browser", "heatmap", "scatter"],  # 基因组注释 Genome Annotation (['gggenes', 'gggenomes', 'Artemis'])
    "comparative": ["bar", "box", "chord_diagram", "circos", "heatmap", "scatter"],  # 比较基因组 / 共线性 (['plotsr', 'jcvi', 'gggenomes'])
    "pangenome": ["bar", "box", "heatmap", "scatter", "upset"],  # 泛基因组 Pangenome (['Panaroo', 'PPanGGOLiN', 'UpSetR'])
    "microbiome_16s": ["alpha_diversity", "bar", "beta_diversity", "box", "circle_tree", "composition", "heatmap", "scatter", "tree"],  # 16S / Amplicon 微生物组 (['phyloseq', 'microbiomeMarker', 'vegan'])
    "shotgun": ["alpha_diversity", "bar", "bar_sig", "beta_diversity", "box", "composition", "heatmap", "line", "scatter", "violin"],  # Shotgun Metagenomics (["anvi'o", 'phyloseq', 'vegan'])
    "mag": ["bar", "box", "circle_tree", "complexheatmap", "dendrogram", "heatmap", "scatter", "tree"],  # MAG Binning / 宏基因组组装 (["anvi'o", 'Bandage', 'ggtree'])
    "metatranscriptomics": ["alpha_diversity", "bar", "bar_sig", "beta_diversity", "box", "complexheatmap", "composition", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 宏转录组 Metatranscriptomics (['phyloseq', 'ComplexHeatmap', 'ggplot2'])
    "virome": ["bar", "box", "chord_diagram", "circle_tree", "complexheatmap", "dendrogram", "heatmap", "network_graph", "ppi", "scatter", "tree"],  # Virome / 病毒组 (['ggtree', "anvi'o", 'ComplexHeatmap'])
    "pathogen": ["bar", "box", "circle_tree", "heatmap", "scatter", "tree"],  # 病原体基因组监测 / Genomic Epidemiology (['Auspice', 'ggtree', 'ETE Toolkit'])
    "phylogeny": ["bar", "box", "circle_tree", "heatmap", "scatter", "tree"],  # 系统发育 / Phylogenetics (['ggtree', 'ggtreeExtra', 'ETE Toolkit'])
    "proteomics": ["bar", "box", "complexheatmap", "dendrogram", "heatmap", "scatter", "volcano"],  # 蛋白质组学 Proteomics (['DEP', 'MSstats', 'EnhancedVolcano'])
    "metabolomics": ["bar", "bar_sig", "box", "chord_diagram", "heatmap", "line", "network_graph", "pathway", "plsda", "ppi", "scatter", "violin", "volcano"],  # 代谢组学 Metabolomics (['MetaboAnalystR', 'ropls', 'ggplot2'])
    "lipidomics": ["bar", "bar_sig", "box", "chord_diagram", "circos", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 脂质组学 Lipidomics (['LipidSigR', 'ComplexHeatmap', 'ggplot2'])
    "glycomics": ["bar", "bar_sig", "box", "chord_diagram", "complexheatmap", "dendrogram", "heatmap", "line", "network_graph", "ppi", "scatter", "violin"],  # 糖组学 / Glycomics / Glycoproteomics (['GlycoGlyph', 'ggplot2', 'ComplexHeatmap'])
    "structure": ["bar", "box", "heatmap", "ppi", "scatter", "structure"],  # 蛋白结构预测 (['PyMOL open-source', 'ChimeraX', 'Mol*'])
    "protein_design": ["bar", "bar_sig", "box", "heatmap", "line", "ppi", "scatter", "structure", "violin"],  # 蛋白设计 / Protein Design (['PyMOL', 'ChimeraX', 'Mol*'])
    "docking": ["bar", "box", "heatmap", "ppi", "scatter", "structure"],  # 分子对接 / Virtual Screening (['PyMOL', 'ChimeraX', 'PLIP'])
    "md": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "ppi", "scatter"],  # 分子动力学 MD (['MDAnalysis', 'MDTraj', 'VMD Python'])
    "cheminformatics": ["bar", "box", "heatmap", "pairplot", "radar", "scatter", "structure", "violin"],  # 化学信息学 Cheminformatics (['RDKit drawing', 'CDK Depict', 'seaborn'])
    "pharmacogenomics": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "roc", "scatter", "violin"],  # 药物基因组学 / Drug Response (['ggplot2', 'ComplexHeatmap', 'pROC'])
    "multiomics": ["bar", "box", "circos", "complexheatmap", "dendrogram", "heatmap", "plsda", "sankey", "scatter"],  # 多组学整合 (['MOFA2', 'mixOmics', 'ComplexHeatmap'])
    "enrichment": ["bar", "bar_sig", "box", "circos", "enrichment_bar", "enrichment_dot", "enrichment_network", "heatmap", "line", "scatter", "violin"],  # 通路富集 / GSEA / Functional Annotation (['enrichplot', 'clusterProfiler', 'pathview'])
    "network": ["bar", "box", "chord_diagram", "heatmap", "network_graph", "ppi", "scatter"],  # 网络生物学 / Biological Networks (['Cytoscape', 'ggraph', 'igraph'])
    "network_pharm": ["chord_diagram", "circos", "network_graph", "ppi", "structure"],  # 网络药理学 (['Cytoscape', 'ggraph', 'circlize'])
    "kg": ["bar", "box", "chord_diagram", "heatmap", "network_graph", "ppi", "scatter"],  # 生物医学知识图谱 / KG (['Neo4j', 'pyvis', 'Cytoscape'])
    "cancer": ["bar", "box", "complexheatmap", "dendrogram", "forest", "heatmap", "km", "scatter"],  # 癌症基因组学 / Tumor Genomics (['maftools', 'ComplexHeatmap', 'SigProfilerPlotting'])
    "immune_deconv": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # 肿瘤免疫微环境 / Immune Deconvolution (['ComplexHeatmap', 'ggplot2', 'ggpubr'])
    "immune_repertoire": ["bar", "box", "heatmap", "network_graph", "scatter"],  # 免疫组库 / TCR-BCR / VDJ (['scRepertoire', 'immunarch', 'scirpy'])
    "hla": ["bar", "bar_sig", "box", "complexheatmap", "dendrogram", "heatmap", "line", "scatter", "violin"],  # HLA / 新抗原 / Immunoinformatics (['pVACtools', 'ggplot2', 'ComplexHeatmap'])
    "clinical": ["bar", "box", "forest", "heatmap", "km", "roc", "scatter"],  # 临床生信 / 生存分析 / 预后模型 (['survminer', 'forestplot', 'pROC'])
    "mr": ["bar", "bar_sig", "box", "forest", "heatmap", "line", "scatter", "violin"],  # 因果推断 / Mendelian Randomization (['TwoSampleMR', 'forestplot', 'ggplot2'])
    "ml": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "scatter"],  # 生物医学机器学习 / Predictive Modeling (['SHAP', 'yellowbrick', 'scikit-plot'])
    "foundation": ["bar", "box", "heatmap", "pairplot", "scatter", "violin"],  # 生物大模型 / Foundation Models for Biology (['UMAP', 'openTSNE', 'seaborn'])
    "nlp": ["bar", "box", "heatmap", "scatter"],  # 生物医学 NLP / 文献挖掘 (['pyvis', 'networkx', 'BERTopic'])
    "pathology": ["bar", "box", "ecdf", "heatmap", "histogram", "line", "scatter"],  # 数字病理 / 显微图像 / 细胞图像分析 (['QuPath', 'napari', 'Cellpose'])
}

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

ALL_70_DOMAINS = list(DOMAINS_70_ROUTING.keys())


# ═══ K-Dense 22 学科绘图能力映射（官方 149 skills 分类） ═══
KDENSE_DISCIPLINE_ROUTING = {
    "genomics": ['manhattan', 'circos', 'heatmap', 'genome_track', 'cnv'],
    "transcriptomics": ['volcano', 'heatmap', 'ma_plot', 'enrichment_dot', 'gsea'],
    "single-cell": ['umap', 'tsne', 'dotplot', 'violin', 'heatmap', 'trajectory', 'cellchat'],
    "spatial": ['spatial', 'heatmap', 'umap', 'deconvolution'],
    "epigenomics": ['genome_track', 'heatmap', 'peaks', 'motif', 'beta_dist', 'hic'],
    "metagenomics": ['alpha_diversity', 'beta_diversity', 'composition', 'sankey', 'lefse'],
    "proteomics": ['volcano', 'heatmap', 'venn', 'ppi', 'lollipop'],
    "metabolomics": ['plsda', 'volcano', 'heatmap', 'pathway', 'bland_altman'],
    "lipidomics": ['plsda', 'volcano', 'heatmap', 'bar'],
    "glycomics": ['heatmap', 'bar', 'volcano'],
    "drug-discovery": ['dose_response', 'ic50', 'radar', 'scatter', 'heatmap'],
    "medicinal-chemistry": ['radar', 'scatter', 'structure', 'dose_response'],
    "materials-science": ['scatter', 'line', 'heatmap', 'parity_plot', 'radar'],
    "chemistry": ['scatter', 'line', 'radar', 'parity_plot'],
    "physics": ['scatter', 'line', 'contour_2d', 'heatmap'],
    "structural-biology": ['ppi', 'structure', 'heatmap'],
    "clinical": ['km', 'forest', 'roc', 'calibration', 'nomogram'],
    "epidemiology": ['manhattan', 'forest', 'km', 'bar'],
    "neuroscience": ['umap', 'heatmap', 'scatter', 'line'],
    "plant-science": ['manhattan', 'qqplot', 'heatmap', 'circos'],
    "immunology": ['clonotype', 'umap', 'heatmap', 'diversity', 'volcano'],
    "microbiology": ['alpha_diversity', 'beta_diversity', 'composition', 'tree'],
}
