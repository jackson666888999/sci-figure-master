# Computational Biology / Bioinformatics 70 领域完整工具总表（研究过程 × 核心工具 × 画图工具）

> 来源：用户深度调研（2026-08-23），完整版不加精炼。
> 工具来源参考：nf-core pipelines（100+ 标准化 Nextflow 流程）、Awesome Bioinformatics、Awesome Single Cell、GitHub bioinformatics / computational-biology topics。
> 筛选原则：
> 1. 优先 GitHub / GitLab / 开源工具；
> 2. 优先顶刊、高影响文章、主流 pipeline、社区长期维护工具；
> 3. 覆盖完整研究过程：数据获取 → QC → 预处理 → 核心分析 → 统计/建模 → 可视化 → 可复现；
> 4. 每个领域列 5–10 个核心工具，画图工具单独列；
> 5. 跨领域基础设施（ggplot2 / ComplexHeatmap / Cytoscape / Seurat / Scanpy / MultiQC 等）会重复出现。
>
> 表格说明：
> **研究过程** = 一个领域从原始数据到文章主图的标准流程。
> **核心工具** = 分析工具。
> **画图工具** = 结果展示工具，优先顶刊常用、可导出矢量图、可复现。

---

## 1. 测序数据质控 / NGS QC

| 项目 | 内容 |
|---|---|
| 完整研究过程 | 原始 FASTQ → 质量评估 → 接头/低质碱基去除 → 读长/GC/duplication 检查 → 多样本 QC 汇总 → 报告 |
| 核心工具 | [FastQC](https://github.com/s-andrews/FastQC), [MultiQC](https://github.com/MultiQC/MultiQC), [fastp](https://github.com/OpenGene/fastp), [Cutadapt](https://github.com/marcelm/cutadapt), [Trim Galore](https://github.com/FelixKrueger/TrimGalore), [BBTools](https://github.com/BioInfoTools/BBMap), [seqkit](https://github.com/shenwei356/seqkit), [seqtk](https://github.com/lh3/seqtk) |
| 画图工具 | [MultiQC](https://github.com/MultiQC/MultiQC), [ggplot2](https://github.com/tidyverse/ggplot2), [seaborn](https://github.com/mwaskom/seaborn), [matplotlib](https://github.com/matplotlib/matplotlib) |

---

## 2. 短读长基因组比对

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ QC → 参考基因组索引 → 比对 → SAM/BAM 转换 → 排序去重复 → 比对质量评估 → 下游变异/覆盖度分析 |
| 核心工具 | [BWA](https://github.com/lh3/bwa), [BWA-MEM2](https://github.com/bwa-mem2/bwa-mem2), [Bowtie2](https://github.com/BenLangmead/bowtie2), [minimap2](https://github.com/lh3/minimap2), [samtools](https://github.com/samtools/samtools), [Picard](https://github.com/broadinstitute/picard), [sambamba](https://github.com/biod/sambamba), [bedtools](https://github.com/arq5x/bedtools2) |
| 画图工具 | [MultiQC](https://github.com/MultiQC/MultiQC), [Qualimap](https://github.com/bioconda/bioconda-recipes/tree/master/recipes/qualimap), [IGV](https://github.com/igvteam/igv), [JBrowse 2](https://github.com/GMOD/jbrowse-components) |

---

## 3. 长读长测序 Nanopore / PacBio

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FAST5/POD5/BAM/FASTQ → basecalling → read QC → filtering → 比对/组装/变异检测 → 甲基化/结构变异分析 |
| 核心工具 | [minimap2](https://github.com/lh3/minimap2), [NanoPlot](https://github.com/wdecoster/NanoPlot), [pycoQC](https://github.com/a-slide/pycoQC), [Filtlong](https://github.com/rrwick/Filtlong), [LongQC](https://github.com/yfukasawa/LongQC), [Flye](https://github.com/fenderglass/Flye), [Canu](https://github.com/marbl/canu), [hifiasm](https://github.com/chhylp123/hifiasm) |
| 画图工具 | [NanoPlot](https://github.com/wdecoster/NanoPlot), [pycoQC](https://github.com/a-slide/pycoQC), [IGV](https://github.com/igvteam/igv), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) |

---

## 4. WGS / WES SNV-Indel 变异检测

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ QC → 比对 → 去重复/BQSR → SNV/Indel calling → joint calling → 过滤 → 注释 → 临床/功能解释 → 可视化 |
| 核心工具 | [GATK](https://github.com/broadinstitute/gatk), [DeepVariant](https://github.com/google/deepvariant), [bcftools](https://github.com/samtools/bcftools), [freebayes](https://github.com/freebayes/freebayes), [Octopus](https://github.com/luntergroup/octopus), [VEP](https://github.com/Ensembl/ensembl-vep), [SnpEff](https://github.com/pcingola/SnpEff), [vcfanno](https://github.com/brentp/vcfanno) |
| 画图工具 | [IGV](https://github.com/igvteam/igv), [CMplot](https://github.com/YinLiLin/CMplot), [karyoploteR](https://github.com/bernatgel/karyoploteR), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 5. 结构变异 SV

| 项目 | 内容 |
|---|---|
| 完整研究过程 | WGS/long-read → 比对 → discordant/split-read 检测 → SV calling → 合并/过滤 → 注释 → 基因/调控区影响解释 |
| 核心工具 | [Manta](https://github.com/Illumina/manta), [Delly](https://github.com/dellytools/delly), [LUMPY](https://github.com/arq5x/lumpy-sv), [Sniffles](https://github.com/fritzsedlazeck/Sniffles), [cuteSV](https://github.com/tjiangHIT/cuteSV), [SVIM](https://github.com/eldariont/svim), [SURVIVOR](https://github.com/fritzsedlazeck/SURVIVOR), [svtools](https://github.com/hall-lab/svtools) |
| 画图工具 | [svviz2](https://github.com/nspies/svviz2), [IGV](https://github.com/igvteam/igv), [circlize](https://github.com/jokergoo/circlize), [karyoploteR](https://github.com/bernatgel/karyoploteR) |

---

## 6. 拷贝数变异 CNV

| 项目 | 内容 |
|---|---|
| 完整研究过程 | WGS/WES/panel → coverage 计算 → GC/批次校正 → CNV calling → segment 合并 → 肿瘤纯度/倍性校正 → 可视化 |
| 核心工具 | [CNVkit](https://github.com/etal/cnvkit), [Control-FREEC](https://github.com/BoevaLab/FREEC), [FACETS](https://github.com/mskcc/facets), [ichorCNA](https://github.com/broadinstitute/ichorCNA), [GATK CNV](https://github.com/broadinstitute/gatk), [Canvas](https://github.com/Illumina/canvas), [Sequenza](https://github.com/cran/sequenza) |
| 画图工具 | [CNVkit](https://github.com/etal/cnvkit), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [karyoploteR](https://github.com/bernatgel/karyoploteR), [circlize](https://github.com/jokergoo/circlize) |

---

## 7. 群体遗传 / Population Genomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | VCF/基因型数据 → 样本/位点 QC → PCA/IBD/亲缘关系 → 群体结构 → 选择信号 → 分化指数 → 遗传多样性解释 |
| 核心工具 | [PLINK2](https://github.com/chrchang/plink-ng), [VCFtools](https://github.com/vcftools/vcftools), [ANGSD](https://github.com/ANGSD/angsd), [EIGENSOFT](https://github.com/DReichLab/EIG), [ADMIXTURE](https://github.com/stevenliuyi/admix), [selscan](https://github.com/szpiech/selscan), [pcadapt](https://github.com/bcm-uga/pcadapt), [tskit](https://github.com/tskit-dev/tskit) |
| 画图工具 | [pophelper](https://github.com/royfrancis/pophelper), [qqman](https://github.com/stephenturner/qqman), [CMplot](https://github.com/YinLiLin/CMplot), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 8. GWAS / 复杂性状遗传学

| 项目 | 内容 |
|---|---|
| 完整研究过程 | genotype/phenotype → QC → imputation → association testing → population correction → meta-analysis → fine-mapping → locus interpretation |
| 核心工具 | [PLINK2](https://github.com/chrchang/plink-ng), [SAIGE](https://github.com/weizhouUMICH/SAIGE), [regenie](https://github.com/rgcgithub/regenie), [BOLT-LMM](https://github.com/PalamaraLab/bolt), [GCTA](https://github.com/jianyangqt/gcta), [METAL](https://github.com/statgen/METAL), [FINEMAP](http://www.christianbenner.com/), [SuSiE](https://github.com/stephenslab/susieR) |
| 画图工具 | [qqman](https://github.com/stephenturner/qqman), [CMplot](https://github.com/YinLiLin/CMplot), [manhattanly](https://github.com/sahirbhatnagar/manhattanly), [locuszoomr](https://github.com/myles-lewis/locuszoomr) |

---

## 9. 单倍型 / Phasing / Imputation

| 项目 | 内容 |
|---|---|
| 完整研究过程 | genotype/VCF → QC → reference panel 准备 → phasing → imputation → dosage filtering → 下游 GWAS/群体分析 |
| 核心工具 | [SHAPEIT5](https://github.com/odelaneau/shapeit5), [Beagle](https://github.com/beagle-dev/beagle-lib), [Eagle](https://github.com/poruloh/Eagle), [Minimac4](https://github.com/statgen/Minimac4), [GLIMPSE](https://github.com/odelaneau/GLIMPSE), [bcftools](https://github.com/samtools/bcftools), [PLINK2](https://github.com/chrchang/plink-ng) |
| 画图工具 | [ggplot2](https://github.com/tidyverse/ggplot2), [CMplot](https://github.com/YinLiLin/CMplot), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 10. RNA-seq 差异表达

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ QC → 比对/准比对 → gene/transcript quantification → normalization → DEG → pathway enrichment → 主图 |
| 核心工具 | [STAR](https://github.com/alexdobin/STAR), [HISAT2](https://github.com/DaehwanKimLab/hisat2), [Salmon](https://github.com/COMBINE-lab/salmon), [kallisto](https://github.com/pachterlab/kallisto), [featureCounts/Subread](https://github.com/ShiLab-Bioinformatics/subread), [DESeq2](https://github.com/thelovelab/DESeq2), [edgeR](https://github.com/jianjinxu/edgeR), [limma](https://github.com/cran/limma), [tximport](https://github.com/thelovelab/tximport) |
| 画图工具 | [EnhancedVolcano](https://github.com/kevinblighe/EnhancedVolcano), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler), [enrichplot](https://github.com/YuLab-SMU/enrichplot) |

---

## 11. 转录本组装 / Isoform 分析

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA-seq/long-read RNA → alignment → transcript assembly → isoform quantification → novel transcript annotation → differential transcript usage |
| 核心工具 | [StringTie](https://github.com/gpertea/stringtie), [RSEM](https://github.com/deweylab/RSEM), [Cufflinks](https://github.com/cole-trapnell-lab/cufflinks), [TALON](https://github.com/mortazavilab/TALON), [FLAIR](https://github.com/BrooksLabUCSC/flair), [SQANTI3](https://github.com/ConesaLab/SQANTI3), [IsoQuant](https://github.com/ablab/IsoQuant) |
| 画图工具 | [ggsashimi](https://github.com/guigolab/ggsashimi), [IGV](https://github.com/igvteam/igv), [Gviz](https://github.com/ivanek/Gviz), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) |

---

## 12. 可变剪接 Alternative Splicing

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA-seq → junction extraction → splicing event detection → PSI quantification → differential splicing → sashimi plot → functional interpretation |
| 核心工具 | [rMATS-turbo](https://github.com/Xinglab/rmats-turbo), [MAJIQ](https://github.com/majiq/majiq_academic), [SUPPA2](https://github.com/comprna/SUPPA), [LeafCutter](https://github.com/davidaknowles/leafcutter), [DEXSeq](https://github.com/mikelove/DEXSeq), [IsoformSwitchAnalyzeR](https://github.com/kvittingseerup/IsoformSwitchAnalyzeR) |
| 画图工具 | [rmats2sashimiplot](https://github.com/Xinglab/rmats2sashimiplot), [ggsashimi](https://github.com/guigolab/ggsashimi), [IGV](https://github.com/igvteam/igv), [Gviz](https://github.com/ivanek/Gviz) |

---

## 13. 融合基因 / Chimeric Transcript

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA-seq → chimeric alignment → fusion calling → filtering → annotation → IGV validation → fusion circos / schematic |
| 核心工具 | [STAR-Fusion](https://github.com/STAR-Fusion/STAR-Fusion), [Arriba](https://github.com/suhrig/arriba), [FusionCatcher](https://github.com/ndaniel/fusioncatcher), [pizzly](https://github.com/pmelsted/pizzly), [deFuse](https://github.com/amcpherson/defuse), [JAFFA](https://github.com/Oshlack/JAFFA), [FusionInspector](https://github.com/FusionInspector/FusionInspector) |
| 画图工具 | [Arriba](https://github.com/suhrig/arriba), [IGV](https://github.com/igvteam/igv), [circlize](https://github.com/jokergoo/circlize), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 14. miRNA / small RNA

| 项目 | 内容 |
|---|---|
| 完整研究过程 | small RNA FASTQ → adapter trimming → length distribution → mapping → miRNA quantification → differential miRNA → target/pathway |
| 核心工具 | [miRDeep2](https://github.com/rajewsky-lab/mirdeep2), [sRNAbench](https://github.com/sRNAtoolbox/sRNAbench), [ShortStack](https://github.com/MikeAxtell/ShortStack), [Cutadapt](https://github.com/marcelm/cutadapt), [Bowtie](https://github.com/BenLangmead/bowtie), [DESeq2](https://github.com/thelovelab/DESeq2), [multiMiR](https://github.com/KechrisLab/multiMiR) |
| 画图工具 | [ggplot2](https://github.com/tidyverse/ggplot2), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [EnhancedVolcano](https://github.com/kevinblighe/EnhancedVolcano), [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler) |

---

## 15. lncRNA / circRNA

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA-seq → transcript assembly / back-splice detection → coding潜力过滤 → expression quantification → differential analysis → ceRNA/network |
| 核心工具 | [StringTie](https://github.com/gpertea/stringtie), [CIRI](https://github.com/chrischen1/CIRI), [CIRCexplorer2](https://github.com/YangLab/CIRCexplorer2), [find_circ](https://github.com/marvin-jens/find_circ), [CPAT](https://github.com/liguowang/cpat), [FEELnc](https://github.com/tderrien/FEELnc), [DESeq2](https://github.com/thelovelab/DESeq2) |
| 画图工具 | [circlize](https://github.com/jokergoo/circlize), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [Cytoscape](https://github.com/cytoscape/cytoscape), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 16. 单细胞 RNA-seq 基础分析

| 项目 | 内容 |
|---|---|
| 完整研究过程 | raw matrix/FASTQ → QC → normalization → feature selection → PCA → batch correction → clustering → marker genes → annotation → UMAP |
| 核心工具 | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [AnnData](https://github.com/scverse/anndata), [SingleCellExperiment](https://github.com/Bioconductor/SingleCellExperiment), [scater](https://github.com/alanocallaghan/scater), [scran](https://github.com/MarioniLab/scran), [Harmony](https://github.com/immunogenomics/harmony), [scVI-tools](https://github.com/scverse/scvi-tools) |
| 画图工具 | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [scCustomize](https://github.com/samuel-marsh/scCustomize), [dittoSeq](https://github.com/dtm2451/dittoSeq) |

---

## 17. 单细胞质控 / 去双细胞 / 去环境 RNA

| 项目 | 内容 |
|---|---|
| 完整研究过程 | count matrix → mitochondrial/ribosomal QC → doublet detection → ambient RNA correction → empty droplet removal → QC report |
| 核心工具 | [DoubletFinder](https://github.com/chris-mcginnis-ucsf/DoubletFinder), [Scrublet](https://github.com/swolock/scrublet), [scDblFinder](https://github.com/plger/scDblFinder), [SoupX](https://github.com/constantAmateur/SoupX), [DecontX/celda](https://github.com/campbio/celda), [DropletUtils](https://github.com/MarioniLab/DropletUtils), [CellBender](https://github.com/broadinstitute/CellBender) |
| 画图工具 | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [scater](https://github.com/alanocallaghan/scater), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 18. 单细胞整合 / 批次校正

| 项目 | 内容 |
|---|---|
| 完整研究过程 | 多批次/多队列 scRNA → batch detection → integration → biological signal preservation → clustering → marker validation |
| 核心工具 | [Harmony](https://github.com/immunogenomics/harmony), [scVI-tools](https://github.com/scverse/scvi-tools), [Seurat](https://github.com/satijalab/seurat), [LIGER](https://github.com/welch-lab/liger), [BBKNN](https://github.com/Teichlab/bbknn), [Scanorama](https://github.com/brianhie/scanorama), [MNN Correct](https://github.com/MarioniLab/batchelor) |
| 画图工具 | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [scIB](https://github.com/theislab/scib), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 19. 单细胞细胞类型注释

| 项目 | 内容 |
|---|---|
| 完整研究过程 | clusters → marker detection → reference mapping → automated annotation → manual curation → marker heatmap/dotplot |
| 核心工具 | [SingleR](https://github.com/dviraran/SingleR), [CellTypist](https://github.com/Teichlab/celltypist), [Azimuth](https://github.com/satijalab/azimuth), [scmap](https://github.com/hemberg-lab/scmap), [Garnett](https://github.com/cole-trapnell-lab/garnett), [scPred](https://github.com/powellgenomicslab/scPred), [Seurat](https://github.com/satijalab/seurat) |
| 画图工具 | [Seurat DotPlot](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [dittoSeq](https://github.com/dtm2451/dittoSeq), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 20. 单细胞轨迹 / Pseudotime

| 项目 | 内容 |
|---|---|
| 完整研究过程 | cell embedding → lineage selection → trajectory inference → pseudotime ordering → branch-specific DEG → fate interpretation |
| 核心工具 | [Monocle3](https://github.com/cole-trapnell-lab/monocle3), [Slingshot](https://github.com/kstreet13/slingshot), [PAGA/Scanpy](https://github.com/scverse/scanpy), [Palantir](https://github.com/dpeerlab/Palantir), [dynverse](https://github.com/dynverse/dynverse), [TSCAN](https://github.com/zji90/TSCAN), [tradeSeq](https://github.com/statOmics/tradeSeq) |
| 画图工具 | [Monocle3](https://github.com/cole-trapnell-lab/monocle3), [Scanpy](https://github.com/scverse/scanpy), [tradeSeq](https://github.com/statOmics/tradeSeq), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 21. RNA Velocity / Fate Mapping

| 项目 | 内容 |
|---|---|
| 完整研究过程 | spliced/unspliced matrix → velocity estimation → latent time → transition probability → fate probability → driver gene |
| 核心工具 | [scVelo](https://github.com/theislab/scvelo), [velocyto.py](https://github.com/velocyto-team/velocyto.py), [CellRank](https://github.com/theislab/cellrank), [dynamo](https://github.com/aristoteleo/dynamo-release), [VeloVAE](https://github.com/welch-lab/VeloVAE), [scNT-seq tools](https://github.com/velocyto-team) |
| 画图工具 | [scVelo](https://github.com/theislab/scvelo), [CellRank](https://github.com/theislab/cellrank), [matplotlib](https://github.com/matplotlib/matplotlib), [Scanpy](https://github.com/scverse/scanpy) |

---

## 22. 单细胞通讯 / Cell-cell Communication

| 项目 | 内容 |
|---|---|
| 完整研究过程 | annotated scRNA/spatial → ligand-receptor database → interaction scoring → sender/receiver analysis → pathway-level communication → validation |
| 核心工具 | [CellChat](https://github.com/sqjin/CellChat), [CellPhoneDB](https://github.com/ventolab/CellphoneDB), [NicheNet](https://github.com/saeyslab/nichenetr), [LIANA](https://github.com/saezlab/liana), [COMMOT](https://github.com/zcang/COMMOT), [NATMI](https://github.com/forrest-lab/NATMI), [Connectome](https://github.com/msraredon/Connectome) |
| 画图工具 | [CellChat](https://github.com/sqjin/CellChat), [LIANA](https://github.com/saezlab/liana), [circlize](https://github.com/jokergoo/circlize), [Cytoscape](https://github.com/cytoscape/cytoscape) |

---

## 23. 单细胞调控网络 / GRN / Regulon

| 项目 | 内容 |
|---|---|
| 完整研究过程 | scRNA/scATAC → TF motif/database → co-expression network → regulon inference → TF activity scoring → network visualization |
| 核心工具 | [SCENIC](https://github.com/aertslab/SCENIC), [pySCENIC](https://github.com/aertslab/pySCENIC), [CellOracle](https://github.com/morris-lab/CellOracle), [GENIE3](https://github.com/aertslab/GENIE3), [GRNBoost2](https://github.com/aertslab/arboreto), [DoRothEA](https://github.com/saezlab/dorothea), [decoupleR](https://github.com/saezlab/decoupleR) |
| 画图工具 | [Cytoscape](https://github.com/cytoscape/cytoscape), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [ggraph](https://github.com/thomasp85/ggraph), [igraph](https://github.com/igraph/igraph) |

---

## 24. scATAC-seq

| 项目 | 内容 |
|---|---|
| 完整研究过程 | fragments/BAM → QC/TSS enrichment → peak calling → matrix construction → dimensionality reduction → motif deviation → gene activity → integration |
| 核心工具 | [Signac](https://github.com/stuart-lab/signac), [ArchR](https://github.com/GreenleafLab/ArchR), [SnapATAC2](https://github.com/kaizhang/SnapATAC2), [chromVAR](https://github.com/GreenleafLab/chromVAR), [Cicero](https://github.com/cole-trapnell-lab/cicero-release), [MACS3](https://github.com/macs3-project/MACS), [TOBIAS](https://github.com/loosolab/TOBIAS) |
| 画图工具 | [Signac](https://github.com/stuart-lab/signac), [ArchR](https://github.com/GreenleafLab/ArchR), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [Gviz](https://github.com/ivanek/Gviz) |

---

## 25. 单细胞 Multiome / CITE-seq / 多模态

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA+ATAC/ADT → modality-specific QC → weighted integration → joint embedding → marker/motif/protein analysis → cell state interpretation |
| 核心工具 | [Seurat WNN](https://github.com/satijalab/seurat), [scVI-tools totalVI/MultiVI](https://github.com/scverse/scvi-tools), [muon](https://github.com/scverse/muon), [MOFA2](https://github.com/bioFAM/MOFA2), [LIGER](https://github.com/welch-lab/liger), [Cobolt](https://github.com/epurdom/cobolt), [GLUE](https://github.com/gao-lab/GLUE) |
| 画图工具 | [Seurat](https://github.com/satijalab/seurat), [muon](https://github.com/scverse/muon), [Scanpy](https://github.com/scverse/scanpy), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 26. 空间转录组 Spatial Transcriptomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | spatial count + image → QC → normalization → spatial clustering → spatial variable genes → spatial domain → histology overlay |
| 核心工具 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [Seurat](https://github.com/satijalab/seurat), [stLearn](https://github.com/BiomedicalMachineLearning/stLearn), [BayesSpace](https://github.com/edward130603/BayesSpace), [SpaGCN](https://github.com/jianhuupenn/SpaGCN), [PRECAST](https://github.com/feiyoung/PRECAST) |
| 画图工具 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [Seurat](https://github.com/satijalab/seurat), [napari](https://github.com/napari/napari) |

---

## 27. 空间反卷积 / 细胞定位

| 项目 | 内容 |
|---|---|
| 完整研究过程 | spatial bulk spot + scRNA reference → reference mapping → cell type proportion → spatial abundance → niche interpretation |
| 核心工具 | [cell2location](https://github.com/BayraktarLab/cell2location), [Tangram](https://github.com/broadinstitute/Tangram), [spacexr/RCTD](https://github.com/dmcable/spacexr), [Stereoscope](https://github.com/almaan/stereoscope), [DestVI/scVI-tools](https://github.com/scverse/scvi-tools), [CARD](https://github.com/YMa-lab/CARD), [SPOTlight](https://github.com/MarcElosua/SPOTlight) |
| 画图工具 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [Seurat](https://github.com/satijalab/seurat), [matplotlib](https://github.com/matplotlib/matplotlib) |

---

## 28. 空间细胞邻域 / Spatial Niche / 空间通讯

| 项目 | 内容 |
|---|---|
| 完整研究过程 | spatial coordinates → neighborhood graph → co-localization → ligand-receptor spatial modeling → niche programs → disease-region association |
| 核心工具 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [COMMOT](https://github.com/zcang/COMMOT), [CellChat](https://github.com/sqjin/CellChat), [LIANA](https://github.com/saezlab/liana), [MISTy](https://github.com/saezlab/mistyR), [stLearn](https://github.com/BiomedicalMachineLearning/stLearn) |
| 画图工具 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [CellChat](https://github.com/sqjin/CellChat), [circlize](https://github.com/jokergoo/circlize) |

---

## 29. ChIP-seq

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ → QC → alignment → duplicate removal → peak calling → peak annotation → motif → differential binding → signal profile |
| 核心工具 | [Bowtie2](https://github.com/BenLangmead/bowtie2), [BWA](https://github.com/lh3/bwa), [MACS3](https://github.com/macs3-project/MACS), [deepTools](https://github.com/deeptools/deepTools), [DiffBind](https://github.com/Bioconductor-mirror/DiffBind), [csaw](https://github.com/Bioconductor-mirror/csaw), [ChIPseeker](https://github.com/YuLab-SMU/ChIPseeker), [MEME Suite](https://github.com/cinquin/MEME) |
| 画图工具 | [deepTools](https://github.com/deeptools/deepTools), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [ChIPseeker](https://github.com/YuLab-SMU/ChIPseeker), [IGV](https://github.com/igvteam/igv) |

---

## 30. CUT&Tag / CUT&RUN

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ → trimming → alignment → spike-in normalization → peak calling → signal heatmap → differential enrichment |
| 核心工具 | [Bowtie2](https://github.com/BenLangmead/bowtie2), [MACS3](https://github.com/macs3-project/MACS), [SEACR](https://github.com/FredHutch/SEACR), [deepTools](https://github.com/deeptools/deepTools), [DiffBind](https://github.com/Bioconductor-mirror/DiffBind), [ChIPseeker](https://github.com/YuLab-SMU/ChIPseeker), [samtools](https://github.com/samtools/samtools) |
| 画图工具 | [deepTools](https://github.com/deeptools/deepTools), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [IGV](https://github.com/igvteam/igv) |

---

## 31. ATAC-seq

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ → QC → alignment → Tn5 shifting → peak calling → FRiP/TSS enrichment → motif deviation → differential accessibility |
| 核心工具 | [Genrich](https://github.com/jsh58/Genrich), [HMMRATAC](https://github.com/LiuLabUB/HMMRATAC), [MACS3](https://github.com/macs3-project/MACS), [TOBIAS](https://github.com/loosolab/TOBIAS), [chromVAR](https://github.com/GreenleafLab/chromVAR), [DiffBind](https://github.com/Bioconductor-mirror/DiffBind), [deepTools](https://github.com/deeptools/deepTools) |
| 画图工具 | [deepTools](https://github.com/deeptools/deepTools), [TOBIAS](https://github.com/loosolab/TOBIAS), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [Gviz](https://github.com/ivanek/Gviz) |

---

## 32. DNA 甲基化 / Bisulfite-seq

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ → bisulfite alignment → methylation extraction → CpG filtering → DMR calling → annotation → methylation heatmap/tracks |
| 核心工具 | [Bismark](https://github.com/FelixKrueger/Bismark), [methylKit](https://github.com/al2na/methylKit), [DSS](https://github.com/haowulab/DSS), [bsseq](https://github.com/hansenlab/bsseq), [MethPipe](https://github.com/smithlabcode/methpipe), [bwa-meth](https://github.com/brentp/bwa-meth), [DMRcate](https://github.com/stephenturner/annotables) |
| 画图工具 | [methylKit](https://github.com/al2na/methylKit), [Gviz](https://github.com/ivanek/Gviz), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [circlize](https://github.com/jokergoo/circlize) |

---

## 33. Hi-C / 3D Genome

| 项目 | 内容 |
|---|---|
| 完整研究过程 | Hi-C FASTQ → mapping → contact matrix → normalization → compartments/TADs/loops → differential chromatin architecture → browser visualization |
| 核心工具 | [HiC-Pro](https://github.com/nservant/HiC-Pro), [Juicer](https://github.com/aidenlab/juicer), [cooler](https://github.com/open2c/cooler), [cooltools](https://github.com/open2c/cooltools), [HiCExplorer](https://github.com/deeptools/HiCExplorer), [FitHiC](https://github.com/ay-lab/fithic), [HiGlass](https://github.com/higlass/higlass) |
| 画图工具 | [HiGlass](https://github.com/higlass/higlass), [Juicebox](https://github.com/aidenlab/Juicebox), [cooltools](https://github.com/open2c/cooltools), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) |

---

## 34. Enhancer-Promoter / Regulatory Linking

| 项目 | 内容 |
|---|---|
| 完整研究过程 | ATAC/ChIP/Hi-C/scMultiome → peak-gene linkage → motif/TF analysis → regulatory network → enhancer activity interpretation |
| 核心工具 | [Cicero](https://github.com/cole-trapnell-lab/cicero-release), [Signac](https://github.com/stuart-lab/signac), [ArchR](https://github.com/GreenleafLab/ArchR), [ABC model](https://github.com/broadinstitute/ABC-Enhancer-Gene-Prediction), [TOBIAS](https://github.com/loosolab/TOBIAS), [chromVAR](https://github.com/GreenleafLab/chromVAR), [CellOracle](https://github.com/morris-lab/CellOracle) |
| 画图工具 | [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [Gviz](https://github.com/ivanek/Gviz), [Cytoscape](https://github.com/cytoscape/cytoscape), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 35. 基因组组装 Genome Assembly

| 项目 | 内容 |
|---|---|
| 完整研究过程 | short/long reads → read QC → assembly → polishing → contamination removal → completeness evaluation → graph visualization |
| 核心工具 | [SPAdes](https://github.com/ablab/spades), [MEGAHIT](https://github.com/voutcn/megahit), [Flye](https://github.com/fenderglass/Flye), [Canu](https://github.com/marbl/canu), [hifiasm](https://github.com/chhylp123/hifiasm), [Shasta](https://github.com/chanzuckerberg/shasta), [QUAST](https://github.com/ablab/quast), [BUSCO](https://gitlab.com/ezlab/busco) |
| 画图工具 | [QUAST](https://github.com/ablab/quast), [Bandage](https://github.com/rrwick/Bandage), [gfatools](https://github.com/lh3/gfatools), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 36. 基因组注释 Genome Annotation

| 项目 | 内容 |
|---|---|
| 完整研究过程 | assembly → repeat masking → gene prediction → transcript/protein evidence integration → functional annotation → annotation QC |
| 核心工具 | [Prokka](https://github.com/tseemann/prokka), [Bakta](https://github.com/oschwengers/bakta), [AUGUSTUS](https://github.com/Gaius-Augustus/Augustus), [BRAKER](https://github.com/Gaius-Augustus/BRAKER), [MAKER](https://github.com/Yandell-Lab/maker), [Funannotate](https://github.com/nextgenusfs/funannotate), [eggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper), [InterProScan](https://github.com/ebi-pf-team/interproscan) |
| 画图工具 | [gggenes](https://github.com/wilkox/gggenes), [gggenomes](https://github.com/thackl/gggenomes), [Artemis](https://github.com/sanger-pathogens/Artemis), [JBrowse 2](https://github.com/GMOD/jbrowse-components) |

---

## 37. 比较基因组 / 共线性

| 项目 | 内容 |
|---|---|
| 完整研究过程 | 多基因组 assembly/annotation → ortholog detection → synteny → rearrangement → gene family evolution → comparative visualization |
| 核心工具 | [MUMmer](https://github.com/mummer4/mummer), [SyRI](https://github.com/schneebergerlab/syri), [MCScanX](https://github.com/wyp1125/MCScanX), [jcvi](https://github.com/tanghaibao/jcvi), [OrthoFinder](https://github.com/davidemms/OrthoFinder), [minimap2](https://github.com/lh3/minimap2), [plotsr](https://github.com/schneebergerlab/plotsr) |
| 画图工具 | [plotsr](https://github.com/schneebergerlab/plotsr), [jcvi](https://github.com/tanghaibao/jcvi), [gggenomes](https://github.com/thackl/gggenomes), [circlize](https://github.com/jokergoo/circlize) |

---

## 38. 泛基因组 Pangenome

| 项目 | 内容 |
|---|---|
| 完整研究过程 | 多样本 genome assemblies → annotation → ortholog clustering → core/accessory genes → pangenome graph → phenotype association |
| 核心工具 | [Roary](https://github.com/sanger-pathogens/Roary), [Panaroo](https://github.com/gtonkinhill/panaroo), [PPanGGOLiN](https://github.com/labgem/PPanGGOLiN), [PanTools](https://github.com/bioinfologics/pantools), [PanPhlAn](https://github.com/SegataLab/panphlan), [ggCaller](https://github.com/bacpop/ggCaller), [vg](https://github.com/vgteam/vg) |
| 画图工具 | [Panaroo](https://github.com/gtonkinhill/panaroo), [PPanGGOLiN](https://github.com/labgem/PPanGGOLiN), [UpSetR](https://github.com/hms-dbmi/UpSetR), [ComplexUpset](https://github.com/krassowski/complex-upset) |

---

## 39. 16S / Amplicon 微生物组

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ → primer trimming → denoising/ASV → taxonomy → alpha/beta diversity → differential taxa → ecological interpretation |
| 核心工具 | [QIIME2](https://github.com/qiime2/qiime2), [DADA2](https://github.com/benjjneb/dada2), [mothur](https://github.com/mothur/mothur), [vsearch](https://github.com/torognes/vsearch), [phyloseq](https://github.com/joey711/phyloseq), [vegan](https://github.com/vegandevs/vegan), [DECIPHER](https://github.com/DECIPHER-code/DECIPHER) |
| 画图工具 | [phyloseq](https://github.com/joey711/phyloseq), [microbiomeMarker](https://github.com/yiluheihei/microbiomeMarker), [vegan](https://github.com/vegandevs/vegan), [ggtree](https://github.com/YuLab-SMU/ggtree) |

---

## 40. Shotgun Metagenomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | FASTQ QC → host removal → taxonomic profiling → functional profiling → assembly/binning 可选 → differential microbiome |
| 核心工具 | [Kraken2](https://github.com/DerrickWood/kraken2), [Bracken](https://github.com/jenniferlu717/Bracken), [MetaPhlAn](https://github.com/biobakery/MetaPhlAn), [HUMAnN](https://github.com/biobakery/humann), [Centrifuge](https://github.com/DaehwanKimLab/centrifuge), [MEGAHIT](https://github.com/voutcn/megahit), [anvi'o](https://github.com/merenlab/anvio), [MaAsLin2](https://github.com/biobakery/Maaslin2) |
| 画图工具 | [anvi'o](https://github.com/merenlab/anvio), [phyloseq](https://github.com/joey711/phyloseq), [vegan](https://github.com/vegandevs/vegan), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 41. MAG Binning / 宏基因组组装

| 项目 | 内容 |
|---|---|
| 完整研究过程 | metagenomic reads → assembly → contig binning → MAG refinement → completeness/contamination → taxonomy → metabolic reconstruction |
| 核心工具 | [MEGAHIT](https://github.com/voutcn/megahit), [metaSPAdes](https://github.com/ablab/spades), [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/), [CONCOCT](https://github.com/BinPro/CONCOCT), [VAMB](https://github.com/RasmussenLab/vamb), [CheckM2](https://github.com/chklovski/CheckM2), [GTDB-Tk](https://github.com/Ecogenomics/GTDBTk), [DRAM](https://github.com/WrightonLabCSU/DRAM) |
| 画图工具 | [anvi'o](https://github.com/merenlab/anvio), [Bandage](https://github.com/rrwick/Bandage), [ggtree](https://github.com/YuLab-SMU/ggtree), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 42. 宏转录组 Metatranscriptomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | RNA-seq QC → rRNA removal → host removal → taxonomic/functional profiling → expression normalization → pathway activity |
| 核心工具 | [SortMeRNA](https://github.com/sortmerna/sortmerna), [HUMAnN](https://github.com/biobakery/humann), [MetaPhlAn](https://github.com/biobakery/MetaPhlAn), [Salmon](https://github.com/COMBINE-lab/salmon), [Kraken2](https://github.com/DerrickWood/kraken2), [eggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper), [DESeq2](https://github.com/thelovelab/DESeq2) |
| 画图工具 | [phyloseq](https://github.com/joey711/phyloseq), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [ggplot2](https://github.com/tidyverse/ggplot2), [MaAsLin2](https://github.com/biobakery/Maaslin2) |

---

## 43. Virome / 病毒组

| 项目 | 内容 |
|---|---|
| 完整研究过程 | metagenomic reads → host/bacterial depletion → viral contig identification → taxonomy → abundance → viral-host linkage → functional annotation |
| 核心工具 | [VirSorter2](https://github.com/jiarong/VirSorter2), [VIBRANT](https://github.com/AnantharamanLab/VIBRANT), [CheckV](https://bitbucket.org/berkeleylab/checkv/src/master/), [DeepVirFinder](https://github.com/jessieren/DeepVirFinder), [Kraken2](https://github.com/DerrickWood/kraken2), [MEGAHIT](https://github.com/voutcn/megahit), [DRAM-v](https://github.com/WrightonLabCSU/DRAM) |
| 画图工具 | [ggtree](https://github.com/YuLab-SMU/ggtree), [anvi'o](https://github.com/merenlab/anvio), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [Cytoscape](https://github.com/cytoscape/cytoscape) |

---

## 44. 病原体基因组监测 / Genomic Epidemiology

| 项目 | 内容 |
|---|---|
| 完整研究过程 | pathogen FASTQ/consensus → QC → lineage/clade assignment → mutation profile → phylogeny → transmission/spatiotemporal tracking |
| 核心工具 | [Nextclade](https://github.com/nextstrain/nextclade), [Augur](https://github.com/nextstrain/augur), [Auspice](https://github.com/nextstrain/auspice), [iVar](https://github.com/andersen-lab/ivar), [V-pipe](https://github.com/cbg-ethz/V-pipe), [Snippy](https://github.com/tseemann/snippy), [IQ-TREE2](https://github.com/iqtree/iqtree2) |
| 画图工具 | [Auspice](https://github.com/nextstrain/auspice), [ggtree](https://github.com/YuLab-SMU/ggtree), [ETE Toolkit](https://github.com/etetoolkit/ete), [Microreact](https://github.com/microreact/microreact) |

---

## 45. 系统发育 / Phylogenetics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | sequences → multiple sequence alignment → trimming → model selection → tree inference → bootstrap → tree annotation |
| 核心工具 | [MAFFT](https://github.com/GSLBiotech/mafft), [MUSCLE](https://github.com/rcedgar/muscle), [IQ-TREE2](https://github.com/iqtree/iqtree2), [RAxML-NG](https://github.com/amkozlov/raxml-ng), [FastTree](https://github.com/morgannprice/fasttree), [BEAST2](https://github.com/CompEvol/beast2), [TreeTime](https://github.com/neherlab/treetime), [trimAl](https://github.com/inab/trimal) |
| 画图工具 | [ggtree](https://github.com/YuLab-SMU/ggtree), [ggtreeExtra](https://github.com/YuLab-SMU/ggtreeExtra), [ETE Toolkit](https://github.com/etetoolkit/ete), [Toytree](https://github.com/eaton-lab/toytree) |

---

## 46. 蛋白质组学 Proteomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | raw MS → mzML conversion → peptide identification → protein inference → quantification → differential protein → pathway/network |
| 核心工具 | [OpenMS](https://github.com/OpenMS/OpenMS), [ProteoWizard](https://github.com/ProteoWizard/pwiz), [Crux](https://github.com/crux-toolkit/crux-toolkit), [Comet](https://github.com/UWPR/Comet), [DIA-NN](https://github.com/vdemichev/DiaNN), [MSstats](https://github.com/Vitek-Lab/MSstats), [DEP](https://github.com/arnesmits/DEP), [pyteomics](https://github.com/levitsky/pyteomics) |
| 画图工具 | [DEP](https://github.com/arnesmits/DEP), [MSstats](https://github.com/Vitek-Lab/MSstats), [EnhancedVolcano](https://github.com/kevinblighe/EnhancedVolcano), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |

---

## 47. 代谢组学 Metabolomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | raw MS/NMR → peak picking → alignment → normalization → metabolite annotation → differential metabolites → pathway/network |
| 核心工具 | [XCMS](https://github.com/sneumann/xcms), [MZmine](https://github.com/mzmine/mzmine), [OpenMS](https://github.com/OpenMS/OpenMS), [matchms](https://github.com/matchms/matchms), [SIRIUS](https://github.com/sirius-ms/sirius), [MetaboAnalystR](https://github.com/xia-lab/MetaboAnalystR), [MSnbase](https://github.com/lgatto/MSnbase), [CAMERA](https://github.com/sneumann/xcms) |
| 画图工具 | [MetaboAnalystR](https://github.com/xia-lab/MetaboAnalystR), [ropls](https://github.com/SamGG/ropls), [ggplot2](https://github.com/tidyverse/ggplot2), [Cytoscape](https://github.com/cytoscape/cytoscape) |

---

## 48. 脂质组学 Lipidomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | LC-MS → peak detection → lipid annotation → class-level quantification → differential lipid → lipid pathway/network |
| 核心工具 | [LipidMS](https://github.com/maialab/LipidMS), [MS-DIAL Workbench](https://github.com/systemsomicslab/MsdialWorkbench), [LipidFinder](https://github.com/ODonnell-Lipidomics/LipidFinder), [LipidSigR](https://github.com/YuLab-SMU/LipidSigR), [XCMS](https://github.com/sneumann/xcms), [MZmine](https://github.com/mzmine/mzmine), [matchms](https://github.com/matchms/matchms) |
| 画图工具 | [LipidSigR](https://github.com/YuLab-SMU/LipidSigR), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [ggplot2](https://github.com/tidyverse/ggplot2), [circlize](https://github.com/jokergoo/circlize) |

---

## 49. 糖组学 / Glycomics / Glycoproteomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | MS raw → peptide/glycan search → glycopeptide FDR → site localization → differential glycosylation → pathway/structure visualization |
| 核心工具 | [OpenMS](https://github.com/OpenMS/OpenMS), [pyteomics](https://github.com/levitsky/pyteomics), [GlycoPAT](https://github.com/bschulzlab/glycopat), [GlycoGlyph](https://github.com/akulmehta/GlycoGlyphPublic), [Byonic-related open workflows](https://github.com/OpenMS/OpenMS), [MSFragger FragPipe](https://github.com/Nesvilab/FragPipe) |
| 画图工具 | [GlycoGlyph](https://github.com/akulmehta/GlycoGlyphPublic), [ggplot2](https://github.com/tidyverse/ggplot2), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [Cytoscape](https://github.com/cytoscape/cytoscape) |

---

## 50. 蛋白结构预测

| 项目 | 内容 |
|---|---|
| 完整研究过程 | protein sequence/complex → MSA/template → structure prediction → confidence evaluation → interface/functional site analysis → structural visualization |
| 核心工具 | [AlphaFold](https://github.com/google-deepmind/alphafold), [AlphaFold3](https://github.com/google-deepmind/alphafold3), [ColabFold](https://github.com/sokrypton/ColabFold), [RoseTTAFold](https://github.com/RosettaCommons/RoseTTAFold), [ESM](https://github.com/facebookresearch/esm), [OpenFold](https://github.com/aqlaboratory/openfold), [Boltz](https://github.com/jwohlwend/boltz), [Chai-1](https://github.com/chaidiscovery/chai-lab) |
| 画图工具 | [PyMOL open-source](https://github.com/schrodinger/pymol-open-source), [ChimeraX](https://github.com/RBVI/ChimeraX), [Mol*](https://github.com/molstar/molstar), [NGL Viewer](https://github.com/nglviewer/ngl) |

---

## 51. 蛋白设计 / Protein Design

| 项目 | 内容 |
|---|---|
| 完整研究过程 | target/backbone → generative design → sequence design → structure validation → binding/interface evaluation → wet-lab candidate prioritization |
| 核心工具 | [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion), [ProteinMPNN](https://github.com/dauparas/ProteinMPNN), [ColabDesign](https://github.com/sokrypton/ColabDesign), [Rosetta](https://github.com/RosettaCommons/rosetta), [OpenFold](https://github.com/aqlaboratory/openfold), [ESM](https://github.com/facebookresearch/esm), [PyRosetta notebooks](https://github.com/RosettaCommons) |
| 画图工具 | [PyMOL](https://github.com/schrodinger/pymol-open-source), [ChimeraX](https://github.com/RBVI/ChimeraX), [Mol*](https://github.com/molstar/molstar), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 52. 分子对接 / Virtual Screening

| 项目 | 内容 |
|---|---|
| 完整研究过程 | protein/ligand preparation → binding pocket → docking → rescoring → interaction profiling → hit prioritization → visualization |
| 核心工具 | [AutoDock Vina](https://github.com/ccsb-scripps/AutoDock-Vina), [smina](https://github.com/mwojcikowski/smina), [GNINA](https://github.com/gnina/gnina), [DiffDock](https://github.com/gcorso/DiffDock), [RDKit](https://github.com/rdkit/rdkit), [Open Babel](https://github.com/openbabel/openbabel), [Meeko](https://github.com/forlilab/Meeko), [PLIP](https://github.com/pharmai/plip) |
| 画图工具 | [PyMOL](https://github.com/schrodinger/pymol-open-source), [ChimeraX](https://github.com/RBVI/ChimeraX), [PLIP](https://github.com/pharmai/plip), [ProLIF](https://github.com/chemosim-lab/ProLIF) |

---

## 53. 分子动力学 MD

| 项目 | 内容 |
|---|---|
| 完整研究过程 | system setup → force field → energy minimization → equilibration → production MD → RMSD/RMSF/Rg/H-bond/FEL → visualization |
| 核心工具 | [GROMACS](https://github.com/gromacs/gromacs), [OpenMM](https://github.com/openmm/openmm), [MDAnalysis](https://github.com/MDAnalysis/mdanalysis), [MDTraj](https://github.com/mdtraj/mdtraj), [PLUMED](https://github.com/plumed/plumed2), [ParmEd](https://github.com/ParmEd/ParmEd), [ProLIF](https://github.com/chemosim-lab/ProLIF) |
| 画图工具 | [MDAnalysis](https://github.com/MDAnalysis/mdanalysis), [MDTraj](https://github.com/mdtraj/mdtraj), [VMD Python](https://github.com/Eigenstate/vmd-python), [matplotlib](https://github.com/matplotlib/matplotlib) |

---

## 54. 化学信息学 Cheminformatics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | compound library → standardization → descriptor/fingerprint → similarity search → QSAR/ML → clustering → chemical space visualization |
| 核心工具 | [RDKit](https://github.com/rdkit/rdkit), [Open Babel](https://github.com/openbabel/openbabel), [DeepChem](https://github.com/deepchem/deepchem), [Chemprop](https://github.com/chemprop/chemprop), [TDC](https://github.com/mims-harvard/TDC), [Mordred](https://github.com/mordred-descriptor/mordred), [scikit-learn](https://github.com/scikit-learn/scikit-learn) |
| 画图工具 | [RDKit drawing](https://github.com/rdkit/rdkit), [CDK Depict](https://github.com/cdk/depict), [seaborn](https://github.com/mwaskom/seaborn), [UMAP](https://github.com/lmcinnes/umap) |

---

## 55. 药物基因组学 / Drug Response

| 项目 | 内容 |
|---|---|
| 完整研究过程 | expression/mutation/CNV + drug IC50/AUC → batch correction → feature selection → response modeling → biomarker discovery → validation |
| 核心工具 | [PharmacoGx](https://github.com/bhklab/PharmacoGx), [oncoPredict](https://github.com/maese005/oncoPredict), [pRRophetic](https://github.com/paulgeeleher/pRRophetic), [DeepPurpose](https://github.com/kexinhuang12345/DeepPurpose), [TDC](https://github.com/mims-harvard/TDC), [scikit-learn](https://github.com/scikit-learn/scikit-learn), [xgboost](https://github.com/dmlc/xgboost) |
| 画图工具 | [ggplot2](https://github.com/tidyverse/ggplot2), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [pROC](https://github.com/xrobin/pROC), [SHAP](https://github.com/shap/shap) |

---

## 56. 多组学整合

| 项目 | 内容 |
|---|---|
| 完整研究过程 | transcriptome/proteome/metabolome/epigenome → normalization → batch correction → feature matching → latent factors/network → phenotype association |
| 核心工具 | [MOFA2](https://github.com/bioFAM/MOFA2), [mofapy2](https://github.com/bioFAM/mofapy2), [mixOmics](https://github.com/mixOmicsTeam/mixOmics), [iClusterPlus](https://github.com/cran/iClusterPlus), [DIABLO/mixOmics](https://github.com/mixOmicsTeam/mixOmics), [WGCNA](https://github.com/cran/WGCNA), [scikit-learn](https://github.com/scikit-learn/scikit-learn) |
| 画图工具 | [MOFA2](https://github.com/bioFAM/MOFA2), [mixOmics](https://github.com/mixOmicsTeam/mixOmics), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [ggalluvial](https://github.com/corybrunson/ggalluvial) |

---

## 57. 通路富集 / GSEA / Functional Annotation

| 项目 | 内容 |
|---|---|
| 完整研究过程 | gene/protein/metabolite list → ID conversion → ORA/GSEA/GSVA → redundancy reduction → pathway-level interpretation → enrichment plots |
| 核心工具 | [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler), [enrichplot](https://github.com/YuLab-SMU/enrichplot), [ReactomePA](https://github.com/YuLab-SMU/ReactomePA), [fgsea](https://github.com/alserglab/fgsea), [GSEApy](https://github.com/zqfang/GSEApy), [GSVA](https://github.com/rcastelo/GSVA), [pathview](https://github.com/datapplab/pathview), [msigdbr](https://github.com/igordot/msigdbr) |
| 画图工具 | [enrichplot](https://github.com/YuLab-SMU/enrichplot), [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler), [pathview](https://github.com/datapplab/pathview), [ggplot2](https://github.com/tidyverse/ggplot2) |

---

## 58. 网络生物学 / Biological Networks

| 项目 | 内容 |
|---|---|
| 完整研究过程 | gene/protein/metabolite nodes → edge database/inference → network construction → module detection → hub prioritization → mechanism hypothesis |
| 核心工具 | [Cytoscape](https://github.com/cytoscape/cytoscape), [igraph](https://github.com/igraph/igraph), [networkx](https://github.com/networkx/networkx), [WGCNA](https://github.com/cran/WGCNA), [STRINGdb](https://github.com/Bioconductor-mirror/STRINGdb), [OmniPath](https://github.com/saezlab/omnipath), [ggraph](https://github.com/thomasp85/ggraph) |
| 画图工具 | [Cytoscape](https://github.com/cytoscape/cytoscape), [ggraph](https://github.com/thomasp85/ggraph), [igraph](https://github.com/igraph/igraph), [cytoscape.js](https://github.com/cytoscape/cytoscape.js) |

---

## 59. 网络药理学

| 项目 | 内容 |
|---|---|
| 完整研究过程 | compound → targets → disease genes → intersection/network → PPI/module → enrichment → docking/validation → mechanism figure |
| 核心工具 | [RDKit](https://github.com/rdkit/rdkit), [Open Babel](https://github.com/openbabel/openbabel), [Cytoscape](https://github.com/cytoscape/cytoscape), [OmniPath](https://github.com/saezlab/omnipath), [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler), [AutoDock Vina](https://github.com/ccsb-scripps/AutoDock-Vina), [DeepPurpose](https://github.com/kexinhuang12345/DeepPurpose), [networkx](https://github.com/networkx/networkx) |
| 画图工具 | [Cytoscape](https://github.com/cytoscape/cytoscape), [ggraph](https://github.com/thomasp85/ggraph), [circlize](https://github.com/jokergoo/circlize), [PyMOL](https://github.com/schrodinger/pymol-open-source) |

---

## 60. 生物医学知识图谱 / KG

| 项目 | 内容 |
|---|---|
| 完整研究过程 | entity extraction → relation extraction → ontology mapping → graph database → embedding/link prediction → subgraph evidence → visualization |
| 核心工具 | [Neo4j](https://github.com/neo4j/neo4j), [PyKEEN](https://github.com/pykeen/pykeen), [DGL-KE](https://github.com/awslabs/dgl-ke), [AmpliGraph](https://github.com/Accenture/AmpliGraph), [RDFLib](https://github.com/RDFLib/rdflib), [scispaCy](https://github.com/allenai/scispacy), [BioBERT](https://github.com/dmis-lab/biobert), [networkx](https://github.com/networkx/networkx) |
| 画图工具 | [Neo4j](https://github.com/neo4j/neo4j), [pyvis](https://github.com/WestHealth/pyvis), [Cytoscape](https://github.com/cytoscape/cytoscape), [cytoscape.js](https://github.com/cytoscape/cytoscape.js) |

---

## 61. 癌症基因组学 / Tumor Genomics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | tumor-normal WES/WGS/RNA → mutation/CNV/SV/fusion → MAF → driver/signature → subtype → survival/immune/drug association |
| 核心工具 | [maftools](https://github.com/PoisonAlien/maftools), [GATK](https://github.com/broadinstitute/gatk), [Mutect2](https://github.com/broadinstitute/gatk), [SigProfilerExtractor](https://github.com/AlexandrovLab/SigProfilerExtractor), [MutationalPatterns](https://github.com/UMCUGenetics/MutationalPatterns), [FACETS](https://github.com/mskcc/facets), [CNVkit](https://github.com/etal/cnvkit), [TCGAbiolinks](https://github.com/BioinformaticsFMRP/TCGAbiolinks) |
| 画图工具 | [maftools](https://github.com/PoisonAlien/maftools), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [SigProfilerPlotting](https://github.com/AlexandrovLab/SigProfilerPlotting), [survminer](https://github.com/kassambara/survminer) |

---

## 62. 肿瘤免疫微环境 / Immune Deconvolution

| 项目 | 内容 |
|---|---|
| 完整研究过程 | bulk RNA/scRNA/spatial → immune cell estimation → checkpoint/cytokine score → survival/drug response → validation |
| 核心工具 | [MCPcounter](https://github.com/ebecht/MCPcounter), [xCell](https://github.com/dviraran/xCell), [ESTIMATE](https://github.com/cran/estimate), [immunedeconv](https://github.com/omnideconv/immunedeconv), [CIBERSORTx web](https://cibersortx.stanford.edu/), [GSVA](https://github.com/rcastelo/GSVA), [IOBR](https://github.com/IOBR/IOBR) |
| 画图工具 | [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [ggplot2](https://github.com/tidyverse/ggplot2), [ggpubr](https://github.com/kassambara/ggpubr), [corrplot](https://github.com/taiyun/corrplot) |

---

## 63. 免疫组库 / TCR-BCR / VDJ

| 项目 | 内容 |
|---|---|
| 完整研究过程 | bulk/scVDJ reads → clonotype assembly → V/J usage → clonal expansion → diversity → antigen specificity/network → phenotype association |
| 核心工具 | [MiXCR](https://github.com/milaboratory/mixcr), [Immcantation](https://github.com/immcantation), [Change-O](https://github.com/immcantation/changeo), [scirpy](https://github.com/scverse/scirpy), [scRepertoire](https://github.com/ncborcherding/scRepertoire), [immunarch](https://github.com/immunomind/immunarch), [VDJtools](https://github.com/mikessh/vdjtools) |
| 画图工具 | [scRepertoire](https://github.com/ncborcherding/scRepertoire), [immunarch](https://github.com/immunomind/immunarch), [scirpy](https://github.com/scverse/scirpy), [ggraph](https://github.com/thomasp85/ggraph) |

---

## 64. HLA / 新抗原 / Immunoinformatics

| 项目 | 内容 |
|---|---|
| 完整研究过程 | WES/RNA/TCR → HLA typing → somatic mutation → peptide generation → binding prediction → expression filtering → neoantigen prioritization |
| 核心工具 | [OptiType](https://github.com/FRED-2/OptiType), [arcasHLA](https://github.com/RabadanLab/arcasHLA), [HLA-HD](https://github.com/takumorizo/HLA-HD), [pVACtools](https://github.com/griffithlab/pVACtools), [MHCflurry](https://github.com/openvax/mhcflurry), [netMHCpan wrappers](https://github.com/openvax/mhcflurry), [MixMHCpred-related](https://github.com/GfellerLab) |
| 画图工具 | [pVACtools](https://github.com/griffithlab/pVACtools), [ggplot2](https://github.com/tidyverse/ggplot2), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [maftools](https://github.com/PoisonAlien/maftools) |

---

## 65. 临床生信 / 生存分析 / 预后模型

| 项目 | 内容 |
|---|---|
| 完整研究过程 | clinical + omics → cohort QC → feature selection → survival modeling → risk score → ROC/calibration/DCA → validation cohort |
| 核心工具 | [survival](https://github.com/therneau/survival), [survminer](https://github.com/kassambara/survminer), [lifelines](https://github.com/CamDavidsonPilon/lifelines), [scikit-survival](https://github.com/sebp/scikit-survival), [rms](https://github.com/harrelfe/rms), [pROC](https://github.com/xrobin/pROC), [glmnet](https://github.com/cran/glmnet), [tidymodels](https://github.com/tidymodels/tidymodels) |
| 画图工具 | [survminer](https://github.com/kassambara/survminer), [forestplot](https://github.com/gforge/forestplot), [pROC](https://github.com/xrobin/pROC), [ggDCA](https://github.com/yikeshu0611/ggDCA) |

---

## 66. 因果推断 / Mendelian Randomization

| 项目 | 内容 |
|---|---|
| 完整研究过程 | exposure GWAS + outcome GWAS → instrument selection → harmonization → MR estimation → sensitivity → pleiotropy → causal diagram |
| 核心工具 | [TwoSampleMR](https://github.com/MRCIEU/TwoSampleMR), [MendelianRandomization](https://github.com/cran/MendelianRandomization), [MR-PRESSO](https://github.com/rondolab/MR-PRESSO), [DoWhy](https://github.com/py-why/dowhy), [EconML](https://github.com/py-why/EconML), [MatchIt](https://github.com/kosukeimai/MatchIt), [WeightIt](https://github.com/ngreifer/WeightIt), [dagitty](https://github.com/jtextor/dagitty) |
| 画图工具 | [TwoSampleMR](https://github.com/MRCIEU/TwoSampleMR), [forestplot](https://github.com/gforge/forestplot), [ggplot2](https://github.com/tidyverse/ggplot2), [dagitty](https://github.com/jtextor/dagitty) |

---

## 67. 生物医学机器学习 / Predictive Modeling

| 项目 | 内容 |
|---|---|
| 完整研究过程 | feature matrix → train/test split → preprocessing → model training → tuning → validation → explainability → reproducible report |
| 核心工具 | [scikit-learn](https://github.com/scikit-learn/scikit-learn), [xgboost](https://github.com/dmlc/xgboost), [LightGBM](https://github.com/microsoft/LightGBM), [catboost](https://github.com/catboost/catboost), [PyTorch](https://github.com/pytorch/pytorch), [TensorFlow](https://github.com/tensorflow/tensorflow), [Optuna](https://github.com/optuna/optuna), [SHAP](https://github.com/shap/shap) |
| 画图工具 | [SHAP](https://github.com/shap/shap), [yellowbrick](https://github.com/DistrictDataLabs/yellowbrick), [scikit-plot](https://github.com/reiinakano/scikit-plot), [matplotlib](https://github.com/matplotlib/matplotlib) |

---

## 68. 生物大模型 / Foundation Models for Biology

| 项目 | 内容 |
|---|---|
| 完整研究过程 | sequence/cell/gene/protein data → pretrained model embedding → fine-tuning → prediction/generation → interpretation → downstream biological validation |
| 核心工具 | [ESM](https://github.com/facebookresearch/esm), [scGPT](https://github.com/bowang-lab/scGPT), [Geneformer](https://github.com/jkobject/geneformer), [Nucleotide Transformer](https://github.com/instadeepai/nucleotide-transformer), [DNABERT](https://github.com/jerryji1993/DNABERT), [Evo](https://github.com/evo-design/evo), [BioGPT](https://github.com/microsoft/BioGPT), [Hugging Face Transformers](https://github.com/huggingface/transformers) |
| 画图工具 | [UMAP](https://github.com/lmcinnes/umap), [openTSNE](https://github.com/pavlin-policar/openTSNE), [seaborn](https://github.com/mwaskom/seaborn), [SHAP](https://github.com/shap/shap) |

---

## 69. 生物医学 NLP / 文献挖掘

| 项目 | 内容 |
|---|---|
| 完整研究过程 | PubMed/full text → NER → relation extraction → topic modeling → evidence graph → KG/summary → figure/table |
| 核心工具 | [scispaCy](https://github.com/allenai/scispacy), [BioBERT](https://github.com/dmis-lab/biobert), [PubMedBERT](https://github.com/microsoft/BiomedNLP-PubMedBERT), [BioGPT](https://github.com/microsoft/BioGPT), [BERN2](https://github.com/dmis-lab/BERN2), [metapub](https://github.com/metapub/metapub), [BERTopic](https://github.com/MaartenGr/BERTopic), [spaCy](https://github.com/explosion/spaCy) |
| 画图工具 | [pyvis](https://github.com/WestHealth/pyvis), [networkx](https://github.com/networkx/networkx), [BERTopic](https://github.com/MaartenGr/BERTopic), [pyLDAvis](https://github.com/bmabey/pyLDAvis) |

---

## 70. 数字病理 / 显微图像 / 细胞图像分析

| 项目 | 内容 |
|---|---|
| 完整研究过程 | WSI/microscopy image → preprocessing → segmentation → feature extraction → spatial/statistical modeling → classification/survival → overlay visualization |
| 核心工具 | [QuPath](https://github.com/qupath/qupath), [CellProfiler](https://github.com/CellProfiler/CellProfiler), [Cellpose](https://github.com/MouseLand/cellpose), [StarDist](https://github.com/stardist/stardist), [napari](https://github.com/napari/napari), [scikit-image](https://github.com/scikit-image/scikit-image), [TIAToolbox](https://github.com/TissueImageAnalytics/tiatoolbox), [MONAI](https://github.com/Project-MONAI/MONAI) |
| 画图工具 | [QuPath](https://github.com/qupath/qupath), [napari](https://github.com/napari/napari), [Cellpose](https://github.com/MouseLand/cellpose), [matplotlib](https://github.com/matplotlib/matplotlib) |

---

# 顶刊主图优先可视化工具总表

| 图类型 | 优先工具 |
|---|---|
| QC 汇总 | [MultiQC](https://github.com/MultiQC/MultiQC) |
| 火山图 | [EnhancedVolcano](https://github.com/kevinblighe/EnhancedVolcano), [ggplot2](https://github.com/tidyverse/ggplot2) |
| 热图 | [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap), [pheatmap](https://github.com/raivokolde/pheatmap) |
| PCA / UMAP / tSNE | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [UMAP](https://github.com/lmcinnes/umap) |
| 单细胞 marker 图 | [Seurat](https://github.com/satijalab/seurat), [Scanpy](https://github.com/scverse/scanpy), [scCustomize](https://github.com/samuel-marsh/scCustomize), [dittoSeq](https://github.com/dtm2451/dittoSeq) |
| 轨迹 / velocity | [Monocle3](https://github.com/cole-trapnell-lab/monocle3), [scVelo](https://github.com/theislab/scvelo), [CellRank](https://github.com/theislab/cellrank) |
| 细胞通讯 | [CellChat](https://github.com/sqjin/CellChat), [LIANA](https://github.com/saezlab/liana), [circlize](https://github.com/jokergoo/circlize) |
| 空间组学 | [Squidpy](https://github.com/scverse/squidpy), [Giotto](https://github.com/drieslab/Giotto), [Seurat](https://github.com/satijalab/seurat) |
| 基因组浏览 | [IGV](https://github.com/igvteam/igv), [JBrowse 2](https://github.com/GMOD/jbrowse-components), [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks), [Gviz](https://github.com/ivanek/Gviz) |
| Hi-C | [HiGlass](https://github.com/higlass/higlass), [Juicebox](https://github.com/aidenlab/Juicebox), [cooltools](https://github.com/open2c/cooltools) |
| 瀑布图 / Oncoplot | [maftools](https://github.com/PoisonAlien/maftools), [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) |
| 生存曲线 | [survminer](https://github.com/kassambara/survminer), [lifelines](https://github.com/CamDavidsonPilon/lifelines) |
| ROC / PR | [pROC](https://github.com/xrobin/pROC), [scikit-plot](https://github.com/reiinakano/scikit-plot), [yardstick](https://github.com/tidymodels/yardstick) |
| 森林图 | [forestplot](https://github.com/gforge/forestplot), [metafor](https://github.com/wviechtb/metafor) |
| 网络图 | [Cytoscape](https://github.com/cytoscape/cytoscape), [ggraph](https://github.com/thomasp85/ggraph), [igraph](https://github.com/igraph/igraph), [networkx](https://github.com/networkx/networkx) |
| 富集图 | [clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler), [enrichplot](https://github.com/YuLab-SMU/enrichplot), [pathview](https://github.com/datapplab/pathview) |
| 系统发育树 | [ggtree](https://github.com/YuLab-SMU/ggtree), [ETE Toolkit](https://github.com/etetoolkit/ete), [Toytree](https://github.com/eaton-lab/toytree) |
| 宏基因组组成 | [phyloseq](https://github.com/joey711/phyloseq), [vegan](https://github.com/vegandevs/vegan), [anvi'o](https://github.com/merenlab/anvio) |
| 蛋白结构 | [PyMOL](https://github.com/schrodinger/pymol-open-source), [ChimeraX](https://github.com/RBVI/ChimeraX), [Mol*](https://github.com/molstar/molstar) |
| 分子互作 | [PLIP](https://github.com/pharmai/plip), [ProLIF](https://github.com/chemosim-lab/ProLIF), [PyMOL](https://github.com/schrodinger/pymol-open-source) |
| MD 分析 | [MDAnalysis](https://github.com/MDAnalysis/mdanalysis), [MDTraj](https://github.com/mdtraj/mdtraj) |
| 知识图谱 | [Neo4j](https://github.com/neo4j/neo4j), [pyvis](https://github.com/WestHealth/pyvis), [Cytoscape](https://github.com/cytoscape/cytoscape) |
| 数字病理 | [QuPath](https://github.com/qupath/qupath), [napari](https://github.com/napari/napari), [Cellpose](https://github.com/MouseLand/cellpose) |

---

# 投稿/项目使用建议

如果你是做**顶刊式研究图和方法路线**，我建议每个领域都按这个结构组织：

1. **数据来源图**：cohort / sample / assay / public database。
2. **QC 图**：MultiQC、UMAP QC、测序深度、TSS enrichment、FRiP、mapping rate。
3. **核心发现图**：DEG、marker、mutation、CNV、pathway、trajectory、spatial niche、network module。
4. **机制支持图**：TF、LR、pathway、structure、docking、MD、KG evidence。
5. **验证图**：外部队列、实验验证、临床结局、模型评估。
6. **主图只放强证据结果**，预测性网络、无实验验证的机制图放补图，并明确标注证据等级。
