# Computational Biology / Bioinformatics 70 领域完整工具总表

> 来源：用户深度调研（2026-08-23）。每个领域 = 完整研究过程 + 5–10 核心工具 + 画图工具。
> 筛选：优先 GitHub/GitLab 开源、顶刊主流 pipeline、社区长期维护；覆盖 数据获取→QC→预处理→核心分析→统计/建模→可视化→可复现。
> 用途：sci-figure-master 领域路由 + 按需 clone。跨领域基础设施（ggplot2/ComplexHeatmap/Cytoscape/Seurat/Scanpy/MultiQC）重复出现属正常。

## 顶刊主图优先可视化工具总表（速查）
| 图类型 | 优先工具 |
|---|---|
| QC 汇总 | MultiQC |
| 火山图 | EnhancedVolcano, ggplot2 |
| 热图 | ComplexHeatmap, pheatmap |
| PCA/UMAP/tSNE | Seurat, Scanpy, UMAP |
| 单细胞 marker | Seurat, Scanpy, scCustomize, dittoSeq |
| 轨迹/velocity | Monocle3, scVelo, CellRank |
| 细胞通讯 | CellChat, LIANA, circlize |
| 空间组学 | Squidpy, Giotto, Seurat |
| 基因组浏览 | IGV, JBrowse2, pyGenomeTracks, Gviz |
| Hi-C | HiGlass, Juicebox, cooltools |
| 瀑布图/Oncoplot | maftools, ComplexHeatmap |
| 生存曲线 | survminer, lifelines |
| ROC/PR | pROC, scikit-plot, yardstick |
| 森林图 | forestplot, metafor |
| 网络图 | Cytoscape, ggraph, igraph, networkx |
| 富集图 | clusterProfiler, enrichplot, pathview |
| 系统发育树 | ggtree, ETE Toolkit, Toytree |
| 宏基因组组成 | phyloseq, vegan, anvi'o |
| 蛋白结构 | PyMOL, ChimeraX, Mol* |
| 分子互作 | PLIP, ProLIF, PyMOL |
| MD 分析 | MDAnalysis, MDTraj |
| 知识图谱 | Neo4j, pyvis, Cytoscape |
| 数字病理 | QuPath, napari, Cellpose |

---

## 1. 测序数据质控 / NGS QC
- 过程：FASTQ → 质量评估 → 接头/低质去除 → 读长/GC/duplication → 多样本汇总 → 报告
- 核心：FastQC, MultiQC, fastp, Cutadapt, TrimGalore, BBTools, seqkit, seqtk
- 画图：MultiQC, ggplot2, seaborn, matplotlib

## 2. 短读长基因组比对
- 过程：FASTQ QC → 索引 → 比对 → SAM/BAM → 排序去重 → 质量评估 → 下游
- 核心：BWA, BWA-MEM2, Bowtie2, minimap2, samtools, Picard, sambamba, bedtools
- 画图：MultiQC, Qualimap, IGV, JBrowse2

## 3. 长读长 Nanopore/PacBio
- 过程：FAST5/POD5 → basecalling → QC → filtering → 比对/组装/变异 → 甲基化/SV
- 核心：minimap2, NanoPlot, pycoQC, Filtlong, LongQC, Flye, Canu, hifiasm
- 画图：NanoPlot, pycoQC, IGV, pyGenomeTracks

## 4. WGS/WES SNV-Indel
- 过程：QC → 比对 → 去重/BQSR → calling → joint calling → 过滤 → 注释 → 解释
- 核心：GATK, DeepVariant, bcftools, freebayes, Octopus, VEP, SnpEff, vcfanno
- 画图：IGV, CMplot, karyoploteR, ggplot2

## 5. 结构变异 SV
- 过程：WGS/long-read → 比对 → discordant/split-read → calling → 合并过滤 → 注释
- 核心：Manta, Delly, LUMPY, Sniffles, cuteSV, SVIM, SURVIVOR, svtools
- 画图：svviz2, IGV, circlize, karyoploteR

## 6. 拷贝数变异 CNV
- 过程：WGS/WES/panel → coverage → GC/批次校正 → calling → segment → 纯度/倍性校正
- 核心：CNVkit, Control-FREEC, FACETS, ichorCNA, GATK CNV, Canvas, Sequenza
- 画图：CNVkit, ComplexHeatmap, karyoploteR, circlize

## 7. 群体遗传
- 过程：VCF → QC → PCA/IBD → 群体结构 → 选择信号 → 分化 → 多样性
- 核心：PLINK2, VCFtools, ANGSD, EIGENSOFT, ADMIXTURE, selscan, pcadapt, tskit
- 画图：pophelper, qqman, CMplot, ggplot2

## 8. GWAS
- 过程：genotype/phenotype → QC → imputation → 关联 → 群体校正 → meta → fine-mapping
- 核心：PLINK2, SAIGE, regenie, BOLT-LMM, GCTA, METAL, FINEMAP, SuSiE
- 画图：qqman, CMplot, manhattanly, locuszoomr

## 9. 单倍型/Phasing/Imputation
- 过程：VCF → QC → phasing → imputation → dosage filtering → 下游
- 核心：SHAPEIT5, Beagle, Eagle, Minimac4, GLIMPSE, bcftools, PLINK2
- 画图：ggplot2, CMplot, ComplexHeatmap

## 10. RNA-seq 差异表达
- 过程：QC → 比对/准比对 → quantification → normalization → DEG → enrichment → 主图
- 核心：STAR, HISAT2, Salmon, kallisto, featureCounts, DESeq2, edgeR, limma, tximport
- 画图：EnhancedVolcano, ComplexHeatmap, clusterProfiler, enrichplot

## 11. 转录本组装/Isoform
- 过程：RNA-seq/long-read → alignment → assembly → quantification → novel annotation → DTU
- 核心：StringTie, RSEM, Cufflinks, TALON, FLAIR, SQANTI3, IsoQuant
- 画图：ggsashimi, IGV, Gviz, pyGenomeTracks

## 12. 可变剪接
- 过程：RNA-seq → junction → event detection → PSI → diff splicing → sashimi → 功能
- 核心：rMATS-turbo, MAJIQ, SUPPA2, LeafCutter, DEXSeq, IsoformSwitchAnalyzeR
- 画图：rmats2sashimiplot, ggsashimi, IGV, Gviz

## 13. 融合基因
- 过程：RNA-seq → chimeric align → calling → filter → annotation → IGV → circos/schematic
- 核心：STAR-Fusion, Arriba, FusionCatcher, pizzly, deFuse, JAFFA, FusionInspector
- 画图：Arriba, IGV, circlize, ggplot2

## 14. miRNA/small RNA
- 过程：small RNA → adapter trim → length dist → mapping → quantification → diff → target
- 核心：miRDeep2, sRNAbench, ShortStack, Cutadapt, Bowtie, DESeq2, multiMiR
- 画图：ggplot2, ComplexHeatmap, EnhancedVolcano, clusterProfiler

## 15. lncRNA/circRNA
- 过程：RNA-seq → assembly/back-splice → coding potential → quantification → diff → network
- 核心：StringTie, CIRI, CIRCexplorer2, find_circ, CPAT, FEELnc, DESeq2
- 画图：circlize, ComplexHeatmap, Cytoscape, ggplot2

## 16. 单细胞 RNA-seq 基础
- 过程：matrix/FASTQ → QC → normalization → feature selection → PCA → batch → clustering → marker → UMAP
- 核心：Seurat, Scanpy, AnnData, SingleCellExperiment, scater, scran, Harmony, scVI-tools
- 画图：Seurat, Scanpy, scCustomize, dittoSeq

## 17. 单细胞质控/去双细胞/去环境RNA
- 过程：matrix → mt/ribo QC → doublet → ambient RNA → empty droplet → QC report
- 核心：DoubletFinder, Scrublet, scDblFinder, SoupX, DecontX, DropletUtils, CellBender
- 画图：Seurat, Scanpy, scater, ggplot2

## 18. 单细胞整合/批次校正
- 过程：多批次 → batch detect → integration → signal preserve → clustering → marker
- 核心：Harmony, scVI-tools, Seurat, LIGER, BBKNN, Scanorama, MNN Correct
- 画图：Seurat, Scanpy, scIB, ComplexHeatmap

## 19. 单细胞细胞类型注释
- 过程：clusters → marker → reference mapping → auto annotation → curation → heatmap/dotplot
- 核心：SingleR, CellTypist, Azimuth, scmap, Garnett, scPred, Seurat
- 画图：Seurat DotPlot, Scanpy, dittoSeq, ComplexHeatmap

## 20. 单细胞轨迹/Pseudotime
- 过程：embedding → lineage → trajectory → pseudotime → branch DEG → fate
- 核心：Monocle3, Slingshot, PAGA/Scanpy, Palantir, dynverse, TSCAN, tradeSeq
- 画图：Monocle3, Scanpy, tradeSeq, ggplot2

## 21. RNA Velocity/Fate
- 过程：spliced/unspliced → velocity → latent time → transition → fate → driver
- 核心：scVelo, velocyto.py, CellRank, dynamo, VeloVAE
- 画图：scVelo, CellRank, matplotlib, Scanpy

## 22. 单细胞通讯
- 过程：annotated scRNA/spatial → LR db → scoring → sender/receiver → pathway → validation
- 核心：CellChat, CellPhoneDB, NicheNet, LIANA, COMMOT, NATMI, Connectome
- 画图：CellChat, LIANA, circlize, Cytoscape

## 23. 单细胞调控网络/GRN
- 过程：scRNA/scATAC → TF motif → co-expression → regulon → TF activity → network
- 核心：SCENIC, pySCENIC, CellOracle, GENIE3, GRNBoost2, DoRothEA, decoupleR
- 画图：Cytoscape, ComplexHeatmap, ggraph, igraph

## 24. scATAC-seq
- 过程：fragments/BAM → QC/TSS → peak → matrix → dim red → motif dev → gene activity → integration
- 核心：Signac, ArchR, SnapATAC2, chromVAR, Cicero, MACS3, TOBIAS
- 画图：Signac, ArchR, pyGenomeTracks, Gviz

## 25. 单细胞 Multiome/CITE-seq
- 过程：RNA+ATAC/ADT → modality QC → weighted integration → joint embedding → analysis
- 核心：Seurat WNN, scVI-tools totalVI/MultiVI, muon, MOFA2, LIGER, Cobolt, GLUE
- 画图：Seurat, muon, Scanpy, ComplexHeatmap

## 26. 空间转录组
- 过程：count+image → QC → normalization → spatial clustering → SVGs → domain → histology overlay
- 核心：Squidpy, Giotto, Seurat, stLearn, BayesSpace, SpaGCN, PRECAST
- 画图：Squidpy, Giotto, Seurat, napari

## 27. 空间反卷积/细胞定位
- 过程：spatial spot + scRNA ref → mapping → proportion → spatial abundance → niche
- 核心：cell2location, Tangram, spacexr/RCTD, Stereoscope, DestVI, CARD, SPOTlight
- 画图：Squidpy, Giotto, Seurat, matplotlib

## 28. 空间细胞邻域/空间通讯
- 过程：coordinates → neighborhood graph → co-localization → LR spatial → niche programs → disease
- 核心：Squidpy, Giotto, COMMOT, CellChat, LIANA, MISTy, stLearn
- 画图：Squidpy, Giotto, CellChat, circlize

## 29. ChIP-seq
- 过程：FASTQ → QC → align → dedup → peak → annotation → motif → diff binding → profile
- 核心：Bowtie2, BWA, MACS3, deepTools, DiffBind, csaw, ChIPseeker, MEME
- 画图：deepTools, pyGenomeTracks, ChIPseeker, IGV

## 30. CUT&Tag/CUT&RUN
- 过程：FASTQ → trim → align → spike-in norm → peak → heatmap → diff enrichment
- 核心：Bowtie2, MACS3, SEACR, deepTools, DiffBind, ChIPseeker, samtools
- 画图：deepTools, pyGenomeTracks, ComplexHeatmap, IGV

## 31. ATAC-seq
- 过程：FASTQ → QC → align → Tn5 shift → peak → FRiP/TSS → motif dev → diff accessibility
- 核心：Genrich, HMMRATAC, MACS3, TOBIAS, chromVAR, DiffBind, deepTools
- 画图：deepTools, TOBIAS, pyGenomeTracks, Gviz

## 32. DNA甲基化/Bisulfite
- 过程：FASTQ → bisulfite align → extraction → CpG filter → DMR → annotation → heatmap/tracks
- 核心：Bismark, methylKit, DSS, bsseq, MethPipe, bwa-meth, DMRcate
- 画图：methylKit, Gviz, ComplexHeatmap, circlize

## 33. Hi-C/3D Genome
- 过程：Hi-C FASTQ → mapping → contact matrix → norm → compartments/TADs/loops → diff → browser
- 核心：HiC-Pro, Juicer, cooler, cooltools, HiCExplorer, FitHiC, HiGlass
- 画图：HiGlass, Juicebox, cooltools, pyGenomeTracks

## 34. Enhancer-Promoter/Regulatory Linking
- 过程：ATAC/ChIP/Hi-C/scMultiome → peak-gene linkage → motif/TF → network → activity
- 核心：Cicero, Signac, ArchR, ABC model, TOBIAS, chromVAR, CellOracle
- 画图：pyGenomeTracks, Gviz, Cytoscape, ComplexHeatmap

## 35. 基因组组装
- 过程：reads → QC → assembly → polishing → contamination removal → completeness → graph viz
- 核心：SPAdes, MEGAHIT, Flye, Canu, hifiasm, Shasta, QUAST, BUSCO
- 画图：QUAST, Bandage, gfatools, ggplot2

## 36. 基因组注释
- 过程：assembly → repeat mask → gene pred → evidence integration → functional → QC
- 核心：Prokka, Bakta, AUGUSTUS, BRAKER, MAKER, Funannotate, eggNOG-mapper, InterProScan
- 画图：gggenes, gggenomes, Artemis, JBrowse2

## 37. 比较基因组/共线性
- 过程：assemblies → ortholog → synteny → rearrangement → gene family → comparative viz
- 核心：MUMmer, SyRI, MCScanX, jcvi, OrthoFinder, minimap2, plotsr
- 画图：plotsr, jcvi, gggenomes, circlize

## 38. 泛基因组
- 过程：assemblies → annotation → ortholog clustering → core/accessory → graph → phenotype
- 核心：Roary, Panaroo, PPanGGOLiN, PanTools, PanPhlAn, ggCaller, vg
- 画图：Panaroo, PPanGGOLiN, UpSetR, complex-upset

## 39. 16S/Amplicon 微生物组
- 过程：FASTQ → primer trim → denoising/ASV → taxonomy → alpha/beta → diff taxa → ecology
- 核心：QIIME2, DADA2, mothur, vsearch, phyloseq, vegan, DECIPHER
- 画图：phyloseq, microbiomeMarker, vegan, ggtree

## 40. Shotgun Metagenomics
- 过程：FASTQ QC → host removal → taxonomic → functional → assembly/binning → diff
- 核心：Kraken2, Bracken, MetaPhlAn, HUMAnN, Centrifuge, MEGAHIT, anvi'o, MaAsLin2
- 画图：anvi'o, phyloseq, vegan, ggplot2

## 41. MAG Binning
- 过程：reads → assembly → binning → refinement → completeness/contam → taxonomy → metabolism
- 核心：MEGAHIT, metaSPAdes, MetaBAT2, CONCOCT, VAMB, CheckM2, GTDB-Tk, DRAM
- 画图：anvi'o, Bandage, ggtree, ComplexHeatmap

## 42. 宏转录组
- 过程：RNA QC → rRNA removal → host removal → profiling → norm → pathway
- 核心：SortMeRNA, HUMAnN, MetaPhlAn, Salmon, Kraken2, eggNOG-mapper, DESeq2
- 画图：phyloseq, ComplexHeatmap, ggplot2, MaAsLin2

## 43. Virome/病毒组
- 过程：reads → host/bacterial depletion → viral contig → taxonomy → abundance → viral-host → functional
- 核心：VirSorter2, VIBRANT, CheckV, DeepVirFinder, Kraken2, MEGAHIT, DRAM-v
- 画图：ggtree, anvi'o, ComplexHeatmap, Cytoscape

## 44. 病原体基因组监测
- 过程：FASTQ/consensus → QC → lineage → mutation → phylogeny → transmission/tracking
- 核心：Nextclade, Augur, Auspice, iVar, V-pipe, Snippy, IQ-TREE2
- 画图：Auspice, ggtree, ETE Toolkit, Microreact

## 45. 系统发育
- 过程：sequences → MSA → trim → model → tree → bootstrap → annotation
- 核心：MAFFT, MUSCLE, IQ-TREE2, RAxML-NG, FastTree, BEAST2, TreeTime, trimAl
- 画图：ggtree, ggtreeExtra, ETE Toolkit, Toytree

## 46. 蛋白质组学
- 过程：raw MS → mzML → ID → protein inference → quant → diff → pathway/network
- 核心：OpenMS, ProteoWizard, Crux, Comet, DIA-NN, MSstats, DEP, pyteomics
- 画图：DEP, MSstats, EnhancedVolcano, ComplexHeatmap

## 47. 代谢组学
- 过程：raw MS/NMR → peak picking → align → norm → annotation → diff → pathway/network
- 核心：XCMS, MZmine, OpenMS, matchms, SIRIUS, MetaboAnalystR, MSnbase, CAMERA
- 画图：MetaboAnalystR, ropls, ggplot2, Cytoscape

## 48. 脂质组学
- 过程：LC-MS → peak → lipid annotation → class quant → diff → pathway/network
- 核心：LipidMS, MS-DIAL, LipidFinder, LipidSigR, XCMS, MZmine, matchms
- 画图：LipidSigR, ComplexHeatmap, ggplot2, circlize

## 49. 糖组学/Glycomics
- 过程：MS → peptide/glycan search → FDR → site localization → diff glycosylation → viz
- 核心：OpenMS, pyteomics, GlycoPAT, GlycoGlyph, FragPipe
- 画图：GlycoGlyph, ggplot2, ComplexHeatmap, Cytoscape

## 50. 蛋白结构预测
- 过程：seq/complex → MSA/template → prediction → confidence → interface → viz
- 核心：AlphaFold, AlphaFold3, ColabFold, RoseTTAFold, ESM, OpenFold, Boltz, Chai-1
- 画图：PyMOL, ChimeraX, Mol*, NGL Viewer

## 51. 蛋白设计
- 过程：target/backbone → generative → sequence → validation → interface → prioritization
- 核心：RFdiffusion, ProteinMPNN, ColabDesign, Rosetta, OpenFold, ESM
- 画图：PyMOL, ChimeraX, Mol*, ggplot2

## 52. 分子对接/Virtual Screening
- 过程：protein/ligand prep → pocket → docking → rescoring → interaction → hit → viz
- 核心：AutoDock Vina, smina, GNINA, DiffDock, RDKit, Open Babel, Meeko, PLIP
- 画图：PyMOL, ChimeraX, PLIP, ProLIF

## 53. 分子动力学 MD
- 过程：setup → force field → min → equil → production → RMSD/RMSF/Rg/H-bond/FEL → viz
- 核心：GROMACS, OpenMM, MDAnalysis, MDTraj, PLUMED, ParmEd, ProLIF
- 画图：MDAnalysis, MDTraj, VMD Python, matplotlib

## 54. 化学信息学
- 过程：library → standardization → descriptor/fp → similarity → QSAR/ML → clustering → chem space
- 核心：RDKit, Open Babel, DeepChem, Chemprop, TDC, Mordred, scikit-learn
- 画图：RDKit drawing, CDK Depict, seaborn, UMAP

## 55. 药物基因组学/Drug Response
- 过程：expr/mut/CNV + IC50 → batch → feature → response model → biomarker → validation
- 核心：PharmacoGx, oncoPredict, pRRophetic, DeepPurpose, TDC, scikit-learn, xgboost
- 画图：ggplot2, ComplexHeatmap, pROC, SHAP

## 56. 多组学整合
- 过程：transcriptome/proteome/metabolome/epigenome → norm → batch → match → latent/network → phenotype
- 核心：MOFA2, mofapy2, mixOmics, iClusterPlus, DIABLO, WGCNA, scikit-learn
- 画图：MOFA2, mixOmics, ComplexHeatmap, ggalluvial

## 57. 通路富集/GSEA
- 过程：gene/list → ID convert → ORA/GSEA/GSVA → redundancy reduce → pathway → plots
- 核心：clusterProfiler, enrichplot, ReactomePA, fgsea, GSEApy, GSVA, pathview, msigdbr
- 画图：enrichplot, clusterProfiler, pathview, ggplot2

## 58. 网络生物学
- 过程：nodes → edge db/inference → network → module → hub → hypothesis
- 核心：Cytoscape, igraph, networkx, WGCNA, STRINGdb, OmniPath, ggraph
- 画图：Cytoscape, ggraph, igraph, cytoscape.js

## 59. 网络药理学
- 过程：compound → targets → disease → intersection/network → PPI/module → enrichment → docking → figure
- 核心：RDKit, Open Babel, Cytoscape, OmniPath, clusterProfiler, AutoDock Vina, DeepPurpose, networkx
- 画图：Cytoscape, ggraph, circlize, PyMOL

## 60. 生物医学知识图谱
- 过程：entity → relation → ontology → graph db → embedding/link pred → subgraph → viz
- 核心：Neo4j, PyKEEN, DGL-KE, AmpliGraph, RDFLib, scispaCy, BioBERT, networkx
- 画图：Neo4j, pyvis, Cytoscape, cytoscape.js

## 61. 癌症基因组学
- 过程：tumor-normal → mutation/CNV/SV/fusion → MAF → driver/signature → subtype → survival/drug
- 核心：maftools, GATK, Mutect2, SigProfilerExtractor, MutationalPatterns, FACETS, CNVkit, TCGAbiolinks
- 画图：maftools, ComplexHeatmap, SigProfilerPlotting, survminer

## 62. 肿瘤免疫微环境
- 过程：bulk/scRNA/spatial → immune estimation → checkpoint/cytokine → survival/drug → validation
- 核心：MCPcounter, xCell, ESTIMATE, immunedeconv, CIBERSORTx, GSVA, IOBR
- 画图：ComplexHeatmap, ggplot2, ggpubr, corrplot

## 63. 免疫组库/TCR-BCR/VDJ
- 过程：VDJ reads → clonotype → V/J usage → expansion → diversity → specificity/network → phenotype
- 核心：MiXCR, Immcantation, Change-O, scirpy, scRepertoire, immunarch, VDJtools
- 画图：scRepertoire, immunarch, scirpy, ggraph

## 64. HLA/新抗原/Immunoinformatics
- 过程：WES/RNA/TCR → HLA typing → somatic → peptide → binding pred → expr filter → prioritization
- 核心：OptiType, arcasHLA, HLA-HD, pVACtools, MHCflurry, netMHCpan, MixMHCpred
- 画图：pVACtools, ggplot2, ComplexHeatmap, maftools

## 65. 临床生信/生存分析/预后模型
- 过程：clinical+omics → cohort QC → feature → survival model → risk score → ROC/calibration/DCA → validation
- 核心：survival, survminer, lifelines, scikit-survival, rms, pROC, glmnet, tidymodels
- 画图：survminer, forestplot, pROC, ggDCA

## 66. 因果推断/Mendelian Randomization
- 过程：exposure+outcome GWAS → instrument → harmonize → MR → sensitivity → pleiotropy → diagram
- 核心：TwoSampleMR, MendelianRandomization, MR-PRESSO, DoWhy, EconML, MatchIt, WeightIt, dagitty
- 画图：TwoSampleMR, forestplot, ggplot2, dagitty

## 67. 生物医学机器学习
- 过程：feature matrix → split → preprocess → train → tune → validate → explain → report
- 核心：scikit-learn, xgboost, LightGBM, catboost, PyTorch, TensorFlow, Optuna, SHAP
- 画图：SHAP, yellowbrick, scikit-plot, matplotlib

## 68. 生物大模型/Foundation Models
- 过程：bio data → embedding → fine-tune → pred/generation → interpretation → validation
- 核心：ESM, scGPT, Geneformer, Nucleotide Transformer, DNABERT, Evo, BioGPT, Transformers
- 画图：UMAP, openTSNE, seaborn, SHAP

## 69. 生物医学 NLP/文献挖掘
- 过程：PubMed/full text → NER → relation → topic → evidence graph → KG/summary → figure/table
- 核心：scispaCy, BioBERT, PubMedBERT, BioGPT, BERN2, metapub, BERTopic, spaCy
- 画图：pyvis, networkx, BERTopic, pyLDAvis

## 70. 数字病理/显微图像/细胞图像
- 过程：WSI/image → preprocess → segmentation → feature → spatial/stat model → classification/survival → overlay
- 核心：QuPath, CellProfiler, Cellpose, StarDist, napari, scikit-image, TIAToolbox, MONAI
- 画图：QuPath, napari, Cellpose, matplotlib

---

## 投稿/项目使用建议（顶刊式研究图结构）
1. 数据来源图：cohort / sample / assay / public database
2. QC 图：MultiQC, UMAP QC, 测序深度, TSS enrichment, FRiP, mapping rate
3. 核心发现图：DEG, marker, mutation, CNV, pathway, trajectory, spatial niche, network module
4. 机制支持图：TF, LR, pathway, structure, docking, MD, KG evidence
5. 验证图：外部队列, 实验验证, 临床结局, 模型评估
6. 主图只放强证据；预测性网络/无验证机制图放补图并标证据等级
