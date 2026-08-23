# 生物信息学 / Computational Biology 全领域 Git 工具地图（去重版）

> 来源：用户深度调研（2026-08-23，去重精炼）。按 0–18 共 19 大类，含通用基础 + 各领域核心工具 + 画图工具 + A 级顶刊优先级。
> 筛选：顶刊/高影响常见、社区活跃、可复现流程常用、GitHub/开源优先。
> 用途：sci-figure-master 领域路由 + 选题/工具选型速查。
> 完整仓库 URL 索引（对话提及的全部 GitHub 仓库去重全量）见 `references/REPO_DRAWING_FULL.md` 附录。

## 0. 全领域通用基础
- 工作流/可复现：Nextflow, nf-core, Snakemake, CWL, WDL, Galaxy, Bioconda, Docker, Apptainer, MultiQC, Quarto, R Markdown, DVC, MLflow
- 格式处理：samtools/htslib/bcftools/pysam, bedtools/BEDOPS/pybedtools/GenomicRanges, seqkit/seqtk/BBTools, Biopython/scikit-bio, Bioconductor/SingleCellExperiment
- 通用画图：ggplot2/ComplexHeatmap/pheatmap/ggrepel/ggpubr/patchwork/cowplot；matplotlib/seaborn/plotnine/Altair/Plotly；Cytoscape/igraph/ggraph/networkx；Shiny/Dash/Bokeh/Panel；EnhancedVolcano/clusterProfiler/enrichplot/circlize/UpSetR/ComplexUpset

## 1. DNA-seq/WGS/WES/变异检测
- 核心：FastQC, MultiQC, fastp, Cutadapt, BWA, BWA-MEM2, Bowtie2, minimap2, samtools, Picard, GATK, DeepVariant, freebayes, bcftools, Mutect2/Strelka/VarDict, Manta/Delly/LUMPY, CNVkit/Control-FREEC, VEP/SnpEff/vcfanno, PLINK/VCFtools/ADMIXTURE/ANGSD
- 画图：qqman, CMplot, manhattanly, maftools, karyoploteR, circlize, svviz2, IGV, JBrowse2, Gviz

## 2. RNA-seq/转录组/差异表达/可变剪接
- 核心：STAR, HISAT2, featureCounts, Salmon, kallisto, RSEM, tximport, DESeq2, edgeR, limma, sleuth, sva/RUVSeq/ComBat-seq, rMATS/MAJIQ/SUPPA2/leafcutter, STAR-Fusion/Arriba/FusionCatcher, StringTie/CIRI2/CIRCexplorer2
- 画图：EnhancedVolcano, ggplot2, ComplexHeatmap, pheatmap, ggfortify, clusterProfiler/enrichplot/GSEApy, rmats2sashimiplot/ggsashimi

## 3. 单细胞组学 scRNA/scATAC/multiome
- 核心：Seurat, Scanpy, AnnData, SingleCellExperiment, nf-core/scrnaseq, STARsolo, alevin-fry, DoubletFinder/Scrublet/scDblFinder, SoupX/DecontX, Harmony/LIGER/scVI-tools/BBKNN, PHATE/UMAP, Monocle3/Slingshot/PAGA/scVelo/Palantir, CellChat/CellPhoneDB/NicheNet/LIANA, SCENIC/pySCENIC/CellOracle, inferCNV/CopyKAT/HoneyBADGER, Signac/ArchR/SnapATAC2/chromVAR, MOFA2/muon/totalVI/MultiVI
- 画图：Seurat/Scanpy/scCustomize, ComplexHeatmap/dittoSeq, Monocle3/scVelo/CellRank, CellChat/LIANA/circlize/Cytoscape

## 4. 空间组学
- 核心：Squidpy, Giotto, stLearn, Seurat, BayesSpace/SpaGCN/PRECAST, cell2location/Tangram/RCTD/Stereoscope, COMMOT, SPARK/SPARK-X/SpatialDE
- 画图：Squidpy/Giotto/Seurat（切片叠图、邻域、域、空间通讯）

## 5. 表观组学 ChIP/ATAC/CUT&Tag/Hi-C
- 核心：MACS3/SEACR/SICER2, Genrich/HMMRATAC/TOBIAS, deepTools, DiffBind/csaw, MEME/chromVAR/motifmatchr, ChIPseeker/ChIPpeakAnno, HiC-Pro/Juicer/cooler/HiGlass/HiCExplorer
- 画图：ChIPseeker/ChIPpeakAnno, deepTools, pyGenomeTracks/Gviz/IGV, HiGlass/Juicebox/cooltools, ggseqlogo/Logomaker

## 6. 基因组组装/注释/比较基因组
- 核心：SPAdes/MEGAHIT/SKESA, Flye/Canu/Shasta/hifiasm, Unicycler/MaSuRCA, QUAST/BUSCO/Merqury, Prokka/Bakta/DFAST, AUGUSTUS/BRAKER/MAKER/Funannotate, Roary/Panaroo/PPanGGOLiN/PanTools, MUMmer/MCScanX/SyRI
- 画图：QUAST/Bandage, jcvi/MCScanX/plotsr, Panaroo/PPanGGOLiN/UpSetR, circlize/Circos/gggenomes

## 7. 宏基因组/微生物组/16S/宏转录组
- 核心：QIIME2/DADA2/mothur/vsearch, Kraken2/Bracken/MetaPhlAn/Centrifuge, HUMAnN/eggNOG-mapper/DRAM, MEGAHIT/metaSPAdes/metaFlye, MetaBAT2/MaxBin2/CONCOCT/VAMB, CheckM/CheckM2/GTDB-Tk, phyloseq/vegan/microbiome/mia, anvi'o
- 画图：phyloseq/vegan/microbiomeutilities, microbiomeMarker/MaAsLin2/ANCOMBC, anvi'o/circlize, ggtree/ETE/iTOL

## 8. 蛋白质组/代谢组/质谱
- 核心：OpenMS/pyOpenMS/ProteoWizard, Crux/Comet/MS-GF+/DIA-NN, MSstats/DEP, XCMS/MZmine, matchms/SIRIUS/GNPS, spec2vec
- 画图：DEP/MSstats/EnhancedVolcano, pyteomics, ropls/MetaboAnalystR, Cytoscape/networkx

## 9. 多组学整合/网络生物学/系统生物学
- 核心：MOFA2/mofapy2/iClusterPlus, mixOmics/DIABLO/scikit-learn/PyTorch, WGCNA/igraph/networkx/Cytoscape, clusterProfiler/ReactomePA/GSEApy/fgsea, ARACNe/GENIE3/SCENIC/DoRothEA, COBRApy/COBRA Toolbox/cameo/memote
- 画图：MOFA2/mixOmics, WGCNA/ComplexHeatmap, Cytoscape/ggraph/igraph/networkx, pathview/ReactomePA/enrichplot, ggalluvial/networkD3

## 10. 蛋白结构/分子设计/模拟/药物发现
- 核心：AlphaFold2/3, ColabFold, RoseTTAFold, ESMFold, Boltz, Chai-1, RFdiffusion/ProteinMPNN/ColabDesign/Rosetta, AutoDock Vina/smina/GNINA/DiffDock, GROMACS/OpenMM/MDAnalysis/MDTraj, RDKit/DeepChem/Open Babel, DeepPurpose/TDC/Chemprop/Uni-Mol
- 画图：PyMOL/ChimeraX/NGL/Mol*, MDAnalysis/MDTraj/VMD, PLIP/ProLIF, RDKit/CDK Depict, ggplot2/seaborn

## 11. 系统发育/进化/群体基因组
- 核心：MAFFT/Clustal Omega/MUSCLE, IQ-TREE/RAxML-NG/FastTree, BEAST2/TreeTime, PLINK/ANGSD/msprime/tskit, selscan/iSAFE/pcadapt
- 画图：ggtree/ETE/Toytree, ggtreeExtra/treeio, pophelper/pong, ggplot2/CMplot

## 12. 免疫组库/TCR-BCR/HLA/免疫信息学
- 核心：MiXCR/IgBlast/Change-O/Immcantation, scirpy/scRepertoire/dandelion, OptiType/arcasHLA/HLA-HD, pVACtools/MHCflurry, VDJtools/immunarch
- 画图：scRepertoire/immunarch/scirpy, VJ usage (immunarch/VDJtools), TCR network (igraph/ggraph/Cytoscape), Seurat/Scanpy/scirpy

## 13. 癌症基因组/肿瘤多组学
- 核心：maftools, SigProfilerExtractor/MatrixGenerator/MutationalPatterns, FACETS/CNVkit/ABSOLUTE, PyClone/SciClone/ichorCNA, CIBERSORTx/MCPcounter/xCell/ESTIMATE, PharmacoGx/oncoPredict/pRRophetic
- 画图：maftools/ComplexHeatmap, MutationalPatterns/SigProfilerPlotting, CNVkit/karyoploteR, survminer/survival, ggplot2/ggpubr

## 14. 药物基因组/网络药理学/知识图谱
- 核心：PharmacoGx/oncoPredict/DeepPurpose, DeepChem/TDC/Chemprop, RDKit/Open Babel, Neo4j/PyKEEN/DGL-KE/AmpliGraph, scispaCy/BioBERT/PubTator, OmniPath/decoupleR/DoRothEA
- 画图：Cytoscape/cytoscape.js/ggraph, Neo4j Bloom/pyvis/networkx, clusterProfiler/enrichplot/pathview, RDKit/seaborn

## 15. ML/DL/AI for Biology
- 核心：scikit-learn/xgboost/LightGBM/catboost, PyTorch/TensorFlow/JAX/Keras, PyG/DGL/Spektral, SHAP/captum/lime, ESM/DNABERT/Nucleotide Transformer, scVI-tools/CellTypist/scGPT, AutoGluon/Optuna/Ray Tune
- 画图：scikit-plot/yellowbrick/matplotlib, SHAP, UMAP/openTSNE/seaborn, networkx/PyG/Cytoscape

## 16. 生物医学文本/NLP/文献挖掘
- 核心：scispaCy/BioBERT/PubMedBERT/BioGPT, BERN2/PubTator, OpenNRE/DeepKE, metapub/Biopython Entrez, Neo4j/PyKEEN/RDFLib
- 画图：Cytoscape/networkx/VOSviewer, Neo4j/pyvis/cytoscape.js, BERTopic/pyLDAvis

## 17. 临床生信/医学统计/生存分析
- 核心：survival/survminer/lifelines/scikit-survival, rms/caret/tidymodels/mlr3, pROC/yardstick/CalibrationCurves, metafor/meta/netmeta, DoWhy/EconML/MatchIt/WeightIt
- 画图：survminer/lifelines, pROC/yardstick/PRROC, rms/DynNom nomogram, forestplot/metafor, rmda/ggDCA

## 18. 图像组学/数字病理/细胞图像
- 核心：CellProfiler/Fiji-ImageJ/scikit-image, Cellpose/StarDist/ilastik/napari, Squidpy/Giotto/QuPath, TIAToolbox/MONAI/HistomicsTK
- 画图：napari/Cellpose/QuPath, TIAToolbox/HistomicsTK, Squidpy/Giotto

## 19. A 级顶刊优先级（选型速查）
- WGS/WES: BWA-MEM2, minimap2, samtools, bcftools, GATK, DeepVariant, VEP, maftools
- RNA-seq: STAR, Salmon, kallisto, featureCounts, DESeq2, edgeR, limma, clusterProfiler
- 单细胞: Seurat, Scanpy, scVI-tools, Harmony, Monocle3, scVelo, CellChat, NicheNet, Signac, ArchR
- 空间: Squidpy, Giotto, Seurat, cell2location, Tangram, BayesSpace
- 表观: MACS3, deepTools, DiffBind, ChIPseeker, chromVAR, HiC-Pro, cooler, HiGlass
- 宏基因: QIIME2, DADA2, Kraken2, MetaPhlAn, HUMAnN, MEGAHIT, CheckM2, GTDB-Tk, anvi'o
- 结构/药物: AlphaFold2/3, ColabFold, Boltz, Chai-1, RFdiffusion, ProteinMPNN, AutoDock Vina, GROMACS, RDKit
- 多组学: MOFA2, mixOmics, WGCNA, Cytoscape, clusterProfiler, ReactomePA
- 临床: survival, survminer, rms, pROC, scikit-survival, lifelines
- 图像: CellProfiler, Cellpose, StarDist, QuPath, napari, MONAI

## 后续可扩展 4 表（用户建议）
1. 全领域 GitHub 工具总表：领域/子任务/工具/GitHub/语言/输入/输出/论文/顶刊常见/维护状态
2. 投稿友好可视化工具表：领域/主图类型/工具/主图或补图/统计标注/矢量支持
3. 专项表：多组学/单细胞/网络药理学/知识图谱（用户核心方向细化）
4. 顶刊图形模板提示词表：火山/UMAP/空间/网络/弦/桑基/对接/机制/森林/生存 的中文化提示词
