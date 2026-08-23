# Computational Biology / Bioinformatics 70 领域工具总表（完整 15 字段版）

> 字段定义（共 15 列）：
> 1. 一级领域
> 2. 二级任务
> 3. 推荐等级：A 顶刊常见 / B 主流可用 / C 补充
> 4. 工具名
> 5. GitHub 链接
> 6. 官方文档
> 7. 代表论文/期刊
> 8. 输入数据
> 9. 输出结果
> 10. 主图画图工具
> 11. 补图画图工具
> 12. 是否适合主图
> 13. 是否适合临床/机制文章
> 14. 是否适合单细胞/多组学/网络药理学/知识图谱
> 15. 注意事项
>
> 说明：本表为**不加精炼的完整版**，覆盖全部 70 个领域。推荐等级 A=顶刊主图常见工具，B=主流可用，C=补充/特定场景。GitHub 链接为仓库主页（多数工具同时有 Bioconda/PyPI/CRAN 安装渠道）。画图工具列给出该领域最适合投稿主图的绘图方案。

---

## 1. 测序数据质控 / NGS QC

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 测序质控 | 原始读长质量评估 | A | FastQC | https://github.com/s-andrews/FastQC | https://www.bioinformatics.babraham.ac.uk/projects/fastqc/ | Andrews S. 2010 (babraham) | FASTQ | HTML 质量报告 | MultiQC | ggplot2 | 否（QC辅助） | 否 | 否 | 仅单样本，多样本需 MultiQC 汇总 |
| 测序质控 | 多样本汇总 | A | MultiQC | https://github.com/MultiQC/multiqc | https://multiqc.info/ | Ewels et al. 2016, Bioinformatics | 各工具日志 | 汇总 HTML | MultiQC | — | 是（QC主图） | 是 | 否 | 支持 1000+ 工具日志，标准 QC 报告首选 |
| 测序质控 | 修剪/过滤 | A | fastp | https://github.com/OpenGene/fastp | https://github.com/OpenGene/fastp | Chen et al. 2018, Bioinformatics | FASTQ | 干净 FASTQ + JSON 报告 | fastp 内置 | MultiQC | 否 | 否 | 否 | 默认去接头/低质，速度快 |
| 测序质控 | 接头/低质修剪 | B | Cutadapt | https://github.com/marcelm/cutadapt | https://cutadapt.readthedocs.io/ | Martin 2011, EMBnet | FASTQ + 接头序列 | 修剪后 FASTQ | — | MultiQC | 否 | 否 | 否 | 需手动指定接头 |
| 测序质控 | 低复杂度/污染过滤 | B | BBTools | https://github.com/BioInfoTools/BBTools | https://jgi.doe.gov/data-and-tools/bbtools/ | Bushnell 2014 | FASTQ | 过滤 FASTQ | — | — | 否 | 否 | 否 | 套件含 bbduk/bbmap 等 |
| 测序质控 | 序列快速处理 | C | seqkit | https://github.com/shenwei356/seqkit | https://bioinf.shenwei356.cc/seqkit/ | Shen et al. 2016, PLoS One | FASTA/FASTQ | 处理文件 | — | — | 否 | 否 | 否 | 命令行快，无图 |
| 测序质控 | 序列采样/转换 | C | seqtk | https://github.com/lh3/seqtk | https://github.com/lh3/seqtk | Li 2012 | FASTQ/FASTA | 子集/格式 | — | — | 否 | 否 | 否 | 用于抽样测试 |

## 2. 短读长基因组比对

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 基因组比对 | 通用比对 | A | BWA-MEM2 | https://github.com/bwa-mem2/bwa-mem2 | https://github.com/bwa-mem2/bwa-mem2 | Li & Durbin 2010, Bioinformatics | FASTQ + 参考基因组 | SAM/BAM | IGV | Qualimap | 否 | 否 | 否 | 短读长金标准 |
| 基因组比对 | 精确短比对 | B | Bowtie2 | https://github.com/BenLangmead/bowtie2 | http://bowtie-bio.sourceforge.net/ | Langmead & Salzberg 2012, Nature Methods | FASTQ + 索引 | SAM/BAM | IGV | — | 否 | 否 | 否 | 适合 >50bp |
| 基因组比对 | 通用序列比对 | A | minimap2 | https://github.com/lh3/minimap2 | https://github.com/lh3/minimap2 | Li 2018, Bioinformatics | FASTQ/FASTA | PAF/SAM | — | — | 否 | 否 | 否 | 长短读长通吃 |
| 基因组比对 | BAM 操作 | A | samtools | https://github.com/samtools/samtools | http://www.htslib.org/ | Li et al. 2009, Bioinformatics | SAM/BAM | 排序/索引 BAM | — | — | 否 | 否 | 否 | 必备基础设施 |
| 基因组比对 | 重复标记/QC | B | Picard | https://github.com/broadinstitute/picard | https://broadinstitute.github.io/picard/ | Broad Institute | BAM | 去重 BAM | — | MultiQC | 否 | 否 | 否 | GATK 流程配套 |
| 基因组比对 | 区间操作 | A | bedtools | https://github.com/arq5x/bedtools2 | https://bedtools.readthedocs.io/ | Quinlan & Hall 2010, Bioinformatics | BED/SAM/VCF | 交集/覆盖 | — | — | 否 | 否 | 否 | 区间运算瑞士军刀 |
| 基因组比对 | 比对质量评估 | B | Qualimap | https://github.com/iereml/qualimap | http://qualimap.bioinfo.cipf.es/ | Okonechnikov et al. 2016, Bioinformatics | BAM + BED | QC 报告 | Qualimap | MultiQC | 否 | 否 | 否 | RNA-seq/ChIP 均可用 |

## 3. 长读长 Nanopore / PacBio

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 长读长 | basecalling | A | Guppy/Dorado | https://github.com/nanoporetech/dorado | https://dorado.nanoporetech.com/ | Oxford Nanopore | POD5/FAST5 | FASTQ | — | — | 否 | 否 | 否 | 官方闭源/开源混合 |
| 长读长 | 质量评估 | A | NanoPlot | https://github.com/wdecoster/NanoPlot | https://github.com/wdecoster/NanoPlot | De Coster et al. 2018, Bioinformatics | FASTQ/BAM | 质量图 | NanoPlot | — | 是 | 否 | 否 | 长读长 QC 标配 |
| 长读长 | 实时 QC | B | pycoQC | https://github.com/tleonardi/pycoQC | https://github.com/tleonardi/pycoQC | Leger & Leonardi 2019 | sequencing_summary | 交互报告 | pycoQC | — | 否 | 否 | 否 | 基于测序 summary |
| 长读长 | 读长过滤 | B | Filtlong | https://github.com/rrwick/Filtlong | https://github.com/rrwick/Filtlong | Wick 2019 | FASTQ | 过滤 FASTQ | — | — | 否 | 否 | 否 | 按长度/质量过滤 |
| 长读长 | 组装 | A | Flye | https://github.com/fenderglass/Flye | https://github.com/fenderglass/Flye | Kolmogorov et al. 2019, Genome Research | 长读长 | 基因组组装 | Bandage | — | 否 | 否 | 否 | 长读长 de novo 首选 |
| 长读长 | 组装 | A | hifiasm | https://github.com/chhylp123/hifiasm | https://github.com/chhylp123/hifiasm | Cheng et al. 2021, Nature Methods | HiFi 读长 | 单倍型组装 | — | — | 否 | 否 | 否 | PacBio HiFi 首选 |
| 长读长 | 可视化 | B | IGV | https://github.com/igvteam/igv | https://software.broadinstitute.org/software/igv/ | Robinson et al. 2011, Nat Biotech | BAM/CRAM | 基因组浏览器 | IGV | pyGenomeTracks | 否 | 否 | 否 | 支持长读长视图 |
| 长读长 | 可视化 | B | pyGenomeTracks | https://github.com/deeptools/pyGenomeTracks | https://pygenometracks.readthedocs.io/ | Lopez-Delisle et al. 2021 | BAM/bigWig | 轨道图 | pyGenomeTracks | — | 是 | 否 | 否 | 多轨道叠加 |

## 4. WGS/WES 变异检测 SNV-Indel

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 变异检测 | 标准流程 | A | GATK | https://github.com/broadinstitute/gatk | https://gatk.broadinstitute.org/ | McKenna et al. 2010, Genome Research | BAM | VCF | IGV | CMplot | 否 | 是（临床级） | 否 | 临床合规 Best Practice |
| 变异检测 | 深度学习 call | A | DeepVariant | https://github.com/google/deepvariant | https://github.com/google/deepvariant | Poplin et al. 2018, Nat Biotech | BAM | VCF | — | — | 否 | 是 | 否 | Google 深度学习 caller |
| 变异检测 | VCF 操作 | A | bcftools | https://github.com/samtools/bcftools | http://www.htslib.org/ | Danecek et al. 2021, GigaScience | VCF | 过滤 VCF | — | — | 否 | 否 | 否 | 必备 |
| 变异检测 | 注释 | A | VEP | https://github.com/Ensembl/ensembl-vep | https://www.ensembl.org/info/docs/tools/vep/ | McLaren et al. 2016, Genome Biology | VCF | 注释 VCF | — | — | 否 | 是 | 否 | Ensembl 注释 |
| 变异检测 | 注释 | B | SnpEff | https://github.com/pcingola/SnpEff | https://pcingola.github.io/SnpEff/ | Cingolani et al. 2012, PLoS One | VCF | 注释 VCF | — | — | 否 | 否 | 否 | 轻量注释 |
| 变异检测 | 区域图 | B | CMplot | https://github.com/YinLiLin/RCMplot | https://github.com/YinLiLin/RCMplot | Yin et al. 2021, Bioinformatics | 位点/表型 | Manhattan 图 | CMplot | — | 是 | 否 | 否 | GWAS Manhattan/QQ |
| 变异检测 | 核型图 | B | karyoploteR | https://github.com/bernatgel/karyoploteR | https://bernatgel.github.io/karyoploteR/ | Gel & Serra 2019, Bioinformatics | 基因组区间 | 核型图 | karyoploteR | — | 是 | 否 | 否 | R/Bioconductor |

## 5. 结构变异 SV

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 结构变异 | 短读长 SV | A | Manta | https://github.com/Illumina/manta | https://github.com/Illumina/manta | Chen et al. 2016, Bioinformatics | BAM | VCF(SV) | IGV | circlize | 否 | 是 | 否 | Illumina 出品 |
| 结构变异 | 短读长 SV | B | Delly | https://github.com/dellytools/delly | https://github.com/dellytools/delly | Rausch et al. 2012, Nat Gen | BAM | VCF(SV) | — | — | 否 | 否 | 否 | 集成多种 SV |
| 结构变异 | 长读长 SV | A | Sniffles | https://github.com/fritzsedlazeck/Sniffles | https://github.com/fritzsedlazeck/Sniffles | Sedlazeck et al. 2018, Nat Methods | 长读长 BAM | VCF(SV) | svviz2 | IGV | 否 | 否 | 否 | 长读长 SV 首选 |
| 结构变异 | 长读长 SV | B | cuteSV | https://github.com/tjianglab/cuteSV | https://github.com/tjianglab/cuteSV | Jiang et al. 2020, Genome Biology | 长读长 BAM | VCF(SV) | — | — | 否 | 否 | 否 | 速度快 |
| 结构变异 | SV 合并 | B | SURVIVOR | https://github.com/fritzsedlazeck/SURVIVOR | https://github.com/fritzsedlazeck/SURVIVOR | Jeffares et al. 2017, Genome Research | 多 VCF | 合并 VCF | — | — | 否 | 否 | 否 | 合并多 caller |
| 结构变异 | 可视化 | B | svviz2 | https://github.com/nspies/svviz2 | https://github.com/nspies/svviz2 | Spies et al. 2019, Genome Biology | BAM + SV | 支持度图 | svviz2 | — | 是 | 否 | 否 | 断点可视化 |
| 结构变异 | 圈图 | C | circlize | https://github.com/jokergoo/circlize | https://jokergoo.github.io/circlize/ | Gu et al. 2014, Bioinformatics | 区间数据 | 弦图 | circlize | — | 是 | 否 | 是（网络药理学） | R 圈图首选 |

## 6. 拷贝数变异 CNV

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CNV | 芯片/测序 | A | CNVkit | https://github.com/etal/cnvkit | https://cnvkit.readthedocs.io/ | Talevich et al. 2016, PLoS Comp Biol | BAM + 靶点床 | 基因级 CNV | CNVkit 图 | Gviz | 是 | 是 | 否 | 靶向测序 CNV |
| CNV | 肿瘤 WGS | A | ASCAT | https://github.com/Crick-CancerGenomics/ascat | https://github.com/Crick-CancerGenomics/ascat | Van Loo et al. 2010, PNAS | 肿瘤/正常 BAM | 倍性+CNV | ASCAT 图 | — | 是 | 是 | 否 | 需正常对照 |
| CNV | 单细胞 CNV | B | inferCNV | https://github.com/broadinstitute/infercnv | https://github.com/broadinstitute/infercnv | Tickle et al. 2019, Nat Gen | scRNA 矩阵 | CNV 热图 | inferCNV | ComplexHeatmap | 是 | 否 | 是（单细胞） | 肿瘤细胞鉴定 |
| CNV | 可视化 | B | Gviz | https://github.com/ivanek/Gviz | https://bioconductor.org/packages/Gviz/ | Hahne & Ivanek 2016, Bioinformatics | 基因组区间 | 轨道图 | Gviz | — | 是 | 否 | 否 | Bioconductor |

## 7. 基因表达定量 RNA-seq

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 表达定量 | 比对定量 | A | STAR | https://github.com/alexdobin/STAR | https://github.com/alexdobin/STAR | Dobin et al. 2013, Bioinformatics | FASTQ + 转录本 | 比对 BAM | — | — | 否 | 否 | 否 | 哺乳动物首选 aligner |
| 表达定量 | 伪比对定量 | A | Salmon | https://github.com/COMBINE-lab/salmon | https://combine-lab.github.io/salmon/ | Patro et al. 2017, Nat Methods | FASTQ + 索引 | 表达计数 | — | — | 否 | 否 | 否 | 无需比对，速度快 |
| 表达定量 | 转录本定量 | B | kallisto | https://github.com/pachterlab/kallisto | https://pachterlab.github.io/kallisto/ | Bray et al. 2016, Nat Biotech | FASTQ + 索引 | 表达计数 | — | — | 否 | 否 | 否 | 轻量伪比对 |
| 表达定量 | 计数矩阵 | A | featureCounts | https://github.com/Subread/subread | http://subread.sourceforge.net/ | Liao et al. 2014, Bioinformatics | BAM + 注释 | 计数矩阵 | — | — | 否 | 否 | 否 | 生成计数矩阵 |
| 表达定量 | 差异分析 | A | DESeq2 | https://github.com/mikelove/DESeq2 | https://bioconductor.org/packages/DESeq2 | Love et al. 2014, Genome Biology | 计数矩阵 | 差异基因 | EnhancedVolcano | ggplot2/pheatmap | 是 | 是 | 是（多组学） | 负二项模型 |
| 表达定量 | 差异分析 | A | edgeR | https://github.com/edgeRGroup/edgeR | https://bioconductor.org/packages/edgeR | Robinson et al. 2010, Bioinformatics | 计数矩阵 | 差异基因 | — | — | 是 | 是 | 是 | 与 DESeq2 互补 |
| 表达定量 | 火山图 | A | EnhancedVolcano | https://github.com/kevinblighe/EnhancedVolcano | https://github.com/kevinblighe/EnhancedVolcano | Blighe et al. 2019 | DE 结果 | 火山图 | EnhancedVolcano | — | 是 | 是 | 否 | 顶刊火山图首选 |

## 8. 单细胞转录组 scRNA-seq

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 单细胞 | 分析框架 | A | Seurat | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Satija et al. 2015, Nat Biotech | 表达矩阵 | cluster/UMAP | Seurat | ggplot2 | 是 | 是 | 是（单细胞） | R 生态主流 |
| 单细胞 | 分析框架 | A | Scanpy | https://github.com/scverse/scany | https://scanpy.readthedocs.io/ | Wolf et al. 2018, Genome Biology | 表达矩阵 | cluster/UMAP | Scanpy | matplotlib | 是 | 是 | 是 | Python 生态主流 |
| 单细胞 | 降维 | A | UMAP | https://github.com/lmcinnes/umap | https://umap-learn.readthedocs.io/ | McInnes et al. 2018, arXiv | 高维矩阵 | 2D 坐标 | UMAP | — | 是 | 否 | 是 | 替代 tSNE |
| 单细胞 | marker 可视化 | B | scCustomize | https://github.com/samuel-marsh/scCustomize | https://samuel-marsh.github.io/scCustomize/ | Marsh 2023 | Seurat 对象 | 定制图 | scCustomize | — | 是 | 否 | 是 | Seurat 增强 |
| 单细胞 | 可视化套件 | B | dittoSeq | https://github.com/dtmcreynolds/dittoSeq | https://github.com/dtmcreynolds/dittoSeq | Richardson et al. 2021, Bioinformatics | Seurat/SCE | 多类型图 | dittoSeq | — | 是 | 否 | 是 | 用户友好 |
| 单细胞 | 批次校正 | A | Harmony | https://github.com/immunogenomics/harmony | https://github.com/immunogenomics/harmony | Korsunsky et al. 2019, Nat Methods | 嵌入矩阵 | 校正嵌入 | — | — | 否 | 否 | 是 | 整合多批次 |
| 单细胞 | 双细胞检测 | B | Scrublet | https://github.com/scikit-learn-contrib/scrublet | https://github.com/scikit-learn-contrib/scrublet | Wolock et al. 2019, Cell Systems | 表达矩阵 | doublet 分数 | — | — | 否 | 否 | 是 | 必做 QC |

## 9. 单细胞轨迹/分化

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 轨迹 | 拟时序 | A | Monocle3 | https://github.com/cole-trapnell-lab/monocle3 | https://cole-trapnell-lab.github.io/monocle3/ | Cao et al. 2019, Nature | 表达矩阵 | 轨迹/分支 | Monocle3 | ggplot2 | 是 | 否 | 是 | 主流拟时序 |
| 轨迹 | RNA velocity | A | scVelo | https://github.com/scverse/scvelo | https://scvelo.readthedocs.io/ | Bergen et al. 2020, Nat Biotech | 剪接计数 | 速度场 | scVelo | — | 是 | 否 | 是 | 需 loom/spliced |
| 轨迹 | 终点预测 | B | CellRank | https://github.com/theislab/cellrank | https://cellrank.readthedocs.io/ | Lange et al. 2022, Nat Methods | 速度/概率 | 命运图 | CellRank | — | 是 | 否 | 是 | 基于 scVelo |
| 轨迹 | 可视化 | B | PAGA | https://github.com/theislab/scanpy | https://scanpy.readthedocs.io/ | Wolf et al. 2019, Genome Biology | 图抽象 | 抽象图 | PAGA | — | 是 | 否 | 是 | 拓扑抽象 |

## 10. 细胞通讯

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 通讯 | 配体-受体 | A | CellChat | https://github.com/sqjin/CellChat | https://github.com/sqjin/CellChat | Jin et al. 2021, Nat Comm | 表达矩阵+分组 | 通讯网络 | CellChat | circlize | 是 | 是 | 是 | 顶刊通讯首选 |
| 通讯 | 多方法整合 | A | LIANA | https://github.com/saezlab/liana | https://liana-py.readthedocs.io/ | Dimitrov et al. 2022, Nat Cell Biol | 表达矩阵 | 集合评分 | LIANA | — | 是 | 否 | 是 | 整合 16+ 方法 |
| 通讯 | 可视化 | B | circlize | https://github.com/jokergoo/circlize | https://jokergoo.github.io/circlize/ | Gu et al. 2014, Bioinformatics | 网络数据 | 弦图 | circlize | — | 是 | 否 | 是 | 通讯弦图 |

## 11. 空间转录组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 空间组学 | 分析框架 | A | Squidpy | https://github.com/scverse/squidpy | https://squidpy.readthedocs.io/ | Palla et al. 2022, Nat Biotech | 空间计数 | 空间图/邻域 | Squidpy | Scanpy | 是 | 是 | 是 | 10x Visium 主流 |
| 空间组学 | 分析框架 | A | Giotto | https://github.com/RubD/Giotto | https://rubd.github.io/Giotto_site/ | Dries et al. 2021, Nat Comm | 空间计数 | 空间分析 | Giotto | — | 是 | 是 | 是 | 多平台支持 |
| 空间组学 | 整合 | B | Seurat | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Stuart et al. 2021, Cell | 空间+单细胞 | 映射图 | Seurat | — | 是 | 是 | 是 | 空间×单细胞映射 |
| 空间组学 | 图像配准 | B | napari | https://github.com/napari/napari | https://napari.org/ | Ahlers et al. 2023, Nat Methods | 图像+层 | 多维视图 | napari | — | 是 | 否 | 否 | Python 图像查看器 |

## 12. 蛋白质组学

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 蛋白质组 | 谱图搜索 | A | MaxQuant | https://github.com/MaxLimProteomics/MaxQuant | https://www.maxquant.org/ | Cox & Mann 2008, Nat Biotech | raw 质谱 | 蛋白定量 | — | — | 否 | 是 | 否 | 需 Andromeda |
| 蛋白质组 | 谱图搜索 | A | FragPipe | https://github.com/Nesvilab/FragPipe | https://fragpipe.nesvilab.org/ | Kong et al. 2021, Nat Comm | raw 质谱 | 蛋白定量 | — | — | 否 | 是 | 否 | MSFragger 引擎 |
| 蛋白质组 | 差异分析 | A | limma | https://github.com/Bioconductor/limma | https://bioconductor.org/packages/limma | Ritchie et al. 2015, Nucleic Acids | 表达/强度 | 差异蛋白 | ggplot2 | pheatmap | 是 | 是 | 是 | 通用线性模型 |
| 蛋白质组 | 富集 | B | clusterProfiler | https://github.com/YuLab-SMU/clusterProfiler | https://yulab-smu.top/ | Wu et al. 2021, The Innovation | 基因列表 | 富集结果 | enrichplot | — | 是 | 是 | 是 | 蛋白→基因富集 |
| 蛋白质组 | 可视化 | B | pheatmap | https://github.com/raivokolde/pheatmap | https://github.com/raivokolde/pheatmap | Kolde 2019 | 数值矩阵 | 热图 | pheatmap | — | 是 | 否 | 否 | 简单热图 |

## 13. 代谢组学

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 代谢组 | 峰对齐 | A | XCMS | https://github.com/sneumann/xcms | https://rdrr.io/github/sneumann/xcms/ | Smith et al. 2006, Anal Chem | mzML | 峰表 | — | — | 否 | 是 | 否 | LC-MS 主流 |
| 代谢组 | 注释 | A | MetaboAnalyst | https://github.com/xia-lab/MetaboAnalystR | https://www.metaboanalyst.ca/ | Pang et al. 2021, Nat Proto | 峰表 | 统计/通路 | MetaboAnalyst | — | 是 | 是 | 否 | 网页+ R 包 |
| 代谢组 | 通路 | B | pathview | https://github.com/datapplab/pathview | https://bioconductor.org/packages/pathview | Luo & Brouwer 2013, Bioinformatics | 基因/化合物 | 通路图 | pathview | — | 是 | 是 | 是（网络药理） | KEGG 通路映射 |
| 代谢组 | 多组学整合 | B | mixOmics | https://github.com/mixOmicsTeam/mixOmics | https://mixomics.org/ | Rohart et al. 2017, PLoS Comp Biol | 多组学矩阵 | 整合模型 | mixOmics | — | 是 | 否 | 是 | DIABLO/sPLS |

## 14. 微生物组 16S / 宏基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 微生物组 | 分析框架 | A | phyloseq | https://github.com/joey711/phyloseq | https://joey711.github.io/phyloseq/ | McMurdie & Holmes 2013, PLoS One | OTU/ASV 表 | 群落图 | phyloseq | ggplot2 | 是 | 是 | 否 | R 生态主流 |
| 微生物组 | 多样性 | B | vegan | https://github.com/vegandevs/vegan | https://github.com/vegandevs/vegan | Oksanen et al. 2022 | 群落表 | 多样性/排序 | vegan | ggplot2 | 是 | 否 | 否 | 生态统计 |
| 微生物组 | 分析框架 | A | QIIME2 | https://github.com/qiime2/qiime2 | https://qiime2.org/ | Bolyen et al. 2019, Nat Biotech | 测序数据 | 群落特征 | QIIME2 | — | 否 | 否 | 否 | 完整流程 |
| 微生物组 | 差异丰度 | B | ANCOM-BC | https://github.com/FrederickHuangLab/ANCOM-BC | https://github.com/FrederickHuangLab/ANCOM-BC | Lin & Peddada 2020, Nat Comm | 计数表 | 差异属 | ComplexHeatmap | phyloseq | 是 | 是 | 否 | 组成型数据偏倚校正 |
| 微生物组 | 可视化 | B | anvi'o | https://github.com/merenlab/anvio | https://anvio.org/ | Eren et al. 2015, PeerJ | 宏基因组 | 交互视图 | anvi'o | — | 是 | 否 | 否 | 可交互 |
| 微生物组 | 系统发育 | B | ggtree | https://github.com/YuLab-SMU/ggtree | https://yulab-smu.top/ | Yu et al. 2017, Methods Ecol Evol | 树+注释 | 树图 | ggtree | — | 是 | 否 | 否 | 进化树注释 |

## 15. 系统发育 / 进化

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 系统发育 | 建树 | A | IQ-TREE | https://github.com/iqtree/iqtree2 | http://www.iqtree.org/ | Minh et al. 2020, Mol Biol Evol | 比对序列 | 最大似然树 | — | — | 否 | 否 | 否 | 模型选择自动 |
| 系统发育 | 树可视化 | A | ggtree | https://github.com/YuLab-SMU/ggtree | https://yulab-smu.top/ | Yu et al. 2017, Methods Ecol Evol | 树+注释 | 注释树 | ggtree | — | 是 | 否 | 否 | 顶刊树图首选 |
| 系统发育 | 工具包 | B | ETE Toolkit | https://github.com/etetoolkit/ete | http://etetoolkit.org/ | Huerta-Cepas et al. 2016, Mol Biol Evol | 树 | 树+可视化 | ETE | — | 是 | 否 | 否 | Python |
| 系统发育 | 树可视化 | C | iTOL | https://github.com/iTOL-net/iTOL | https://itol.embl.de/ | Letunic & Bork 2021, NAR | 树+注释 | 在线树 | iTOL | — | 是 | 否 | 否 | 在线交互 |

## 16. 蛋白结构

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 蛋白结构 | 分子查看 | A | PyMOL | https://github.com/schrodinger/pymol-open-source | https://pymol.org/ | Schrödinger LLC | PDB | 分子图 | PyMOL | — | 是 | 是 | 否 | 机制图必备 |
| 蛋白结构 | 分子查看 | A | ChimeraX | https://github.com/RBVI/ChimeraX | https://www.rbvi.ucsf.edu/chimerax/ | Pettersen et al. 2021, Protein Sci | PDB | 分子图 | ChimeraX | — | 是 | 是 | 否 | 新一代查看器 |
| 蛋白结构 | 浏览器查看 | B | Mol* | https://github.com/molstar/molstar | https://molstar.org/ | Sehnal et al. 2021, Nucleic Acids | PDB/mmCIF | Web 分子图 | Mol* | — | 是 | 否 | 否 | PDBe/RCSB 在用 |
| 蛋白结构 | 预测 | A | AlphaFold | https://github.com/google-deepmind/alphafold | https://github.com/google-deepmind/alphafold | Jumper et al. 2021, Nature | 序列 | 结构模型 | PyMOL | ChimeraX | 是 | 是 | 否 | 结构预测金标准 |
| 蛋白结构 | 预测 | A | ColabFold | https://github.com/sokrypton/ColabFold | https://github.com/sokrypton/ColabFold | Mirdita et al. 2022, Nat Methods | 序列 | 结构模型 | PyMOL | — | 是 | 是 | 否 | AlphaFold 轻量版 |
| 蛋白结构 | 互作图 | B | PLIP | https://github.com/pharmai/plip | https://plip.biotec.tu-dresden.de/ | Salentin et al. 2015, Nucleic Acids | PDB | 互作图 | PLIP | PyMOL | 是 | 是 | 否 | 配体-蛋白互作 |

## 17. 分子动力学 MD

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MD | 轨迹分析 | A | MDAnalysis | https://github.com/MDAnalysis/mdanalysis | https://www.mdanalysis.org/ | Michaud-Agrawal et al. 2011, J Comp Chem | 轨迹文件 | 分析数据 | matplotlib | seaborn | 是 | 是 | 否 | Python |
| MD | 轨迹分析 | A | MDTraj | https://github.com/mdtraj/mdtraj | https://mdtraj.org/ | McGibbon et al. 2015, Biophys J | 轨迹文件 | RMSD等 | matplotlib | — | 是 | 否 | 否 | 快 |
| MD | 模拟引擎 | A | GROMACS | https://github.com/gromacs/gromacs | https://www.gromacs.org/ | Abraham et al. 2015, SoftwareX | 拓扑+坐标 | 轨迹 | — | — | 否 | 否 | 否 | 主流引擎 |
| MD | 模拟引擎 | B | OpenMM | https://github.com/openmm/openmm | https://openmm.org/ | Eastman et al. 2017, PLoS Comp Biol | 系统描述 | 轨迹 | — | — | 否 | 否 | 否 | Python 友好 |

## 18. 通路/富集分析

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 富集 | 超几何/ORA | A | clusterProfiler | https://github.com/YuLab-SMU/clusterProfiler | https://yulab-smu.top/ | Wu et al. 2021, The Innovation | 基因列表 | 富集表 | enrichplot | — | 是 | 是 | 是 | 顶刊富集首选 |
| 富集 | 富集可视化 | A | enrichplot | https://github.com/YuLab-SMU/enrichplot | https://yulab-smu.top/ | Yu 2022 | 富集结果 | 点/山/网络图 | enrichplot | — | 是 | 是 | 是 | clusterProfiler 配套 |
| 富集 | 通路映射 | B | pathview | https://github.com/datapplab/pathview | https://bioconductor.org/packages/pathview | Luo & Brouwer 2013, Bioinformatics | 基因/化合物 | KEGG 图 | pathview | — | 是 | 是 | 是 | 网络药理常用 |
| 富集 | 网络富集 | B | ReactomePA | https://github.com/YuLab-SMU/ReactomePA | https://yulab-smu.top/ | Yu & He 2016, Oncotarget | 基因列表 | Reactome 图 | ReactomePA | — | 是 | 是 | 是 | Reactome 通路 |
| 富集 | GSEA | B | fgsea | https://github.com/ctlab/fgsea | https://github.com/ctlab/fgsea | Korotkevich et al. 2021 | 排序基因 | GSEA 结果 | fgsea | — | 是 | 是 | 否 | 快速 GSEA |

## 19. 网络分析 / 网络药理学

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 网络药理 | 网络构建 | A | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | Shannon et al. 2003, Genome Research | 节点/边表 | 网络图 | Cytoscape | — | 是 | 是 | 是 | 网络药理学必备 |
| 网络药理 | 网络可视化 | A | ggraph | https://github.com/thomasp85/ggraph | https://ggraph.data-imaginist.com/ | Pedersen 2022 | 网络数据 | 网络图 | ggraph | — | 是 | 否 | 是 | R/tidygraph |
| 网络药理 | 图算法 | A | igraph | https://github.com/igraph/igraph | https://igraph.org/ | Csardi & Nepusz 2006, InterJournal | 图对象 | 拓扑指标 | — | ggraph | 否 | 否 | 是 | R/Python |
| 网络药理 | 网络可视化 | B | networkx | https://github.com/networkx/networkx | https://networkx.org/ | Hagberg et al. 2008 | 图对象 | 图分析 | matplotlib | — | 否 | 否 | 是 | Python |
| 网络药理 | PPI | B | STRING | https://github.com/string-db/stringdb | https://string-db.org/ | Szklarczyk et al. 2023, NAR | 蛋白列表 | PPI 网络 | STRING | Cytoscape | 是 | 是 | 是 | 数据库+API |
| 网络药理 | 成分-靶标 | C | SwissTargetPrediction | https://www.swisstargetprediction.ch/ | http://www.swisstargetprediction.ch/ | Gfeller et al. 2014, Nucleic Acids | 化合物 | 预测靶标 | — | Cytoscape | 否 | 是 | 是 | 网络药理上游 |

## 20. 知识图谱

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 知识图谱 | 图数据库 | A | Neo4j | https://github.com/neo4j/neo4j | https://neo4j.com/docs/ | Neo4j | 三元组 | 图数据库 | Neo4j Browser | — | 否 | 是 | 是 | 药食同源图谱可用 |
| 知识图谱 | 可视化 | B | pyvis | https://github.com/WestHealth/pyvis | https://pyvis.readthedocs.io/ | WestHealth | 网络数据 | 交互网络 | pyvis | Cytoscape | 是 | 是 | 是 | Python 交互 |
| 知识图谱 | 可视化 | B | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | Shannon et al. 2003 | 节点/边 | 网络图 | Cytoscape | — | 是 | 是 | 是 | 静态出版图 |
| 知识图谱 | 嵌入 | C | DGL-KE | https://github.com/awslabs/dgl-ke | https://github.com/awslabs/dgl-ke | Zheng et al. 2020, KDD | 三元组 | 实体嵌入 | — | — | 否 | 否 | 是 | 知识图谱嵌入 |

## 21. 生存分析 / 预后

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 生存分析 | 生存曲线 | A | survminer | https://github.com/kassambara/survminer | https://rpkgs.datanovia.com/survminer/ | Kassambara et al. 2021 | 生存数据 | KM 曲线 | survminer | — | 是 | 是 | 否 | 顶刊生存图 |
| 生存分析 | 模型 | A | survival | https://github.com/therneau/survival | https://github.com/therneau/survival | Therneau 2023 | 生存数据 | Cox 模型 | — | survminer | 否 | 是 | 否 | R 基础包 |
| 生存分析 | ROC | A | pROC | https://github.com/xrobin/pROC | https://xrobin.github.io/pROC/ | Robin et al. 2011, BMC Bioinf | 预测+标签 | ROC 曲线 | pROC | — | 是 | 是 | 否 | AUC 计算 |
| 生存分析 | Python | B | lifelines | https://github.com/CamDavidsonPilon/lifelines | https://lifelines.readthedocs.io/ | Davidson-Pilon 2019 | 生存数据 | 生存模型 | lifelines | — | 是 | 是 | 否 | Python |

## 22. 机器学习 / 深度学习

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ML | 通用框架 | A | scikit-learn | https://github.com/scikit-learn/scikit-learn | https://scikit-learn.org/ | Pedregosa et al. 2011, JMLR | 特征矩阵 | 模型/预测 | matplotlib | SHAP | 否 | 是 | 是 | 经典 ML |
| ML | 可解释 | A | SHAP | https://github.com/shap/shap | https://shap.readthedocs.io/ | Lundberg & Lee 2017, Nat Neur | 模型+数据 | 贡献图 | SHAP | — | 是 | 是 | 是 | 顶刊可解释性 |
| ML | 深度学习 | A | PyTorch | https://github.com/pytorch/pytorch | https://pytorch.org/ | Paszke et al. 2019, NeurIPS | 张量 | 模型 | matplotlib | — | 否 | 否 | 是 | 主流 DL |
| ML | 深度学习 | A | TensorFlow | https://github.com/tensorflow/tensorflow | https://www.tensorflow.org/ | Abadi et al. 2016, OSDI | 张量 | 模型 | — | — | 否 | 否 | 是 | Google |
| ML | 生物专用 | B | PyTorch Geometric | https://github.com/pyg-team/pytorch_geometric | https://pytorch-geometric.readthedocs.io/ | Fey & Lenssen 2019, ICLR | 图数据 | GNN 模型 | — | — | 否 | 否 | 是 | 图神经网络 |
| ML | 自动 ML | C | auto-sklearn | https://github.com/automl/auto-sklearn | https://automl.github.io/auto-sklearn/ | Feurer et al. 2022, JMLR | 特征矩阵 | 最优模型 | — | — | 否 | 否 | 否 | 自动化 |

## 23. 表观基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 表观 | 峰调用 | A | MACS2 | https://github.com/taoliu/MACS | https://github.com/taoliu/MACS | Zhang et al. 2008, Genome Biology | BAM | 峰 BED | — | pyGenomeTracks | 否 | 是 | 否 | ChIP-seq 主流 |
| 表观 | 可视化 | A | deepTools | https://github.com/deeptools/deeptools | https://deeptools.readthedocs.io/ | Ramirez et al. 2016, Nucleic Acids | BAM/bigWig | 热图/PRO | deepTools | — | 是 | 是 | 否 | 信号轨迹热图 |
| 表观 | 甲基化 | A | Bismark | https://github.com/FelixKrueger/Bismark | https://github.com/FelixKrueger/Bismark | Krueger & Andrews 2011, Bioinformatics | BAM | 甲基化表 | — | methylKit | 否 | 是 | 否 | Bisulfite |
| 表观 | 甲基化分析 | B | methylKit | https://github.com/al2na/methylKit | https://github.com/al2na/methylKit | Akalin et al. 2012, Genome Biology | 甲基化表 | 差异甲基化 | methylKit | — | 是 | 是 | 否 | R |
| 表观 | 单细胞表观 | B | Signac | https://github.com/stuart-lab/signac | https://stuartlab.org/signac/ | Stuart et al. 2021, Cell | 表观计数 | 嵌入/峰 | Signac | Seurat | 是 | 是 | 是 | scATAC |

## 24. 基因调控网络

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 调控网络 | 推断 | A | SCENIC | https://github.com/aertslab/SCENIC | https://github.com/aertslab/SCENIC | Aibar et al. 2017, Nat Methods | 表达矩阵 | 调控网络 | SCENIC | Cytoscape | 是 | 否 | 是 | 单细胞 TF 网络 |
| 调控网络 | 推断 | B | GENIE3 | https://github.com/aertslab/GENIE3 | https://github.com/aertslab/GENIE3 | Huynh-Thu et al. 2010, PLoS One | 表达矩阵 | 网络 | — | ggraph | 否 | 否 | 是 | 随机森林 |
| 调控网络 | 推断 | B | ARACNE | https://github.com/califano-lab/ARACNE | https://github.com/califano-lab/ARACNE | Margolin et al. 2006, BMC Bioinf | 表达矩阵 | 网络 | — | Cytoscape | 否 | 否 | 是 | 互信息 |

## 25. 多组学整合

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 多组学 | 整合 | A | MOFA+ | https://github.com/bioFAM/MOFA2 | https://github.com/bioFAM/MOFA2 | Argelaguet et al. 2020, Nat Biotech | 多组学矩阵 | 隐因子 | MOFA+ | — | 是 | 是 | 是 | 因子分析 |
| 多组学 | 整合 | A | mixOmics | https://github.com/mixOmicsTeam/mixOmics | https://mixomics.org/ | Rohart et al. 2017, PLoS Comp Biol | 多组学矩阵 | 整合模型 | mixOmics | — | 是 | 否 | 是 | sPLS/DIABLO |
| 多组学 | 整合 | B | LIGER | https://github.com/MacoskoLab/liger | https://github.com/MacoskoLab/liger | Welch et al. 2019, Cell | 多组学矩阵 | 共享因子 | LIGER | — | 是 | 否 | 是 | iNMF |
| 多组学 | 整合 | B | Seurat WNN | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Hao et al. 2021, Cell | 多模态 | 加权图 | Seurat | — | 是 | 是 | 是 | 加权最近邻 |

## 26. 数字病理 / 图像分析

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 数字病理 | 切片分析 | A | QuPath | https://github.com/qupath/qupath | https://qupath.github.io/ | Bankhead et al. 2017, Scientific Reports | 全切片图像 | 定量/标注 | QuPath | — | 是 | 是 | 否 | 病理首选 |
| 数字病理 | 分割 | A | Cellpose | https://github.com/MouseLand/cellpose | https://www.cellpose.org/ | Stringer et al. 2021, Nat Methods | 显微镜图像 | 细胞掩码 | Cellpose | napari | 是 | 是 | 否 | 通用分割 |
| 数字病理 | 多维查看 | B | napari | https://github.com/napari/napari | https://napari.org/ | Ahlers et al. 2023, Nat Methods | 图像+层 | 多维视图 | napari | — | 是 | 否 | 否 | Python |
| 数字病理 | 深度学习 | B | StarDist | https://github.com/stardist/stardist | https://github.com/stardist/stardist | Schmidt et al. 2018, Nat Methods | 图像 | 实例分割 | StarDist | — | 是 | 是 | 否 | 核分割 |

## 27. 基因组浏览器 / 可视化

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 浏览器 | 桌面 | A | IGV | https://github.com/igvteam/igv | https://software.broadinstitute.org/software/igv/ | Robinson et al. 2011, Nat Biotech | BAM/CRAM/VCF | 浏览器视图 | IGV | — | 否 | 否 | 否 | 标准浏览器 |
| 浏览器 | 网页 | A | JBrowse2 | https://github.com/GMOD/jbrowse-components | https://jbrowse.org/jb2/ | Diesh et al. 2023, PLoS Comp Biol | 轨道数据 | 网页浏览器 | JBrowse2 | — | 否 | 否 | 否 | 可共享 |
| 浏览器 | 轨道图 | A | pyGenomeTracks | https://github.com/deeptools/pyGenomeTracks | https://pygenometracks.readthedocs.io/ | Lopez-Delisle et al. 2021 | BAM/bigWig | 轨道图 | pyGenomeTracks | — | 是 | 是 | 否 | 出版级轨道 |
| 浏览器 | 圈图 | B | circlize | https://github.com/jokergoo/circlize | https://jokergoo.github.io/circlize/ | Gu et al. 2014 | 区间数据 | 圈图 | circlize | — | 是 | 否 | 是 | 基因组概览 |

## 28. Hi-C / 3D 基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3D基因组 | 可视化 | A | HiGlass | https://github.com/higlass/higlass | https://higlass.io/ | Kerpedjiev et al. 2018, Nat Gen | 矩阵 | 交互矩阵 | HiGlass | — | 是 | 否 | 否 | 网页交互 |
| 3D基因组 | 可视化 | B | Juicebox | https://github.com/aidenlab/Juicebox | https://aidenlab.org/juicebox/ | Durand et al. 2016, Cell Systems | hic 矩阵 | 矩阵视图 | Juicebox | — | 否 | 否 | 否 | Java |
| 3D基因组 | 处理 | B | cooltools | https://github.com/open2c/cooltools | https://cooltools.readthedocs.io/ | Open2C et al. 2022, Nat Comm | cool 文件 | 平衡矩阵 | cooltools | HiGlass | 否 | 否 | 否 | Python |

## 29. 癌症基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 癌症 | MAF 可视化 | A | maftools | https://github.com/PoisonAlien/maftools | https://github.com/PoisonAlien/maftools | Mayakonda et al. 2018, Genome Biology | MAF | Oncoplot | maftools | ComplexHeatmap | 是 | 是 | 否 | 肿瘤突变全景 |
| 癌症 | 拷贝数 | A | GISTIC2 | https://github.com/broadinstitute/gistic2 | https://software.broadinstitute.org/software/copy-number/ | Mermel et al. 2011, Genome Biology | 分段数据 | 显著区域 | — | Gviz | 否 | 是 | 否 | Broad 出品 |
| 癌症 | 肿瘤纯度 | B | ESTIMATE | https://github.com/singha53/estimate | https://bioinformatics.mdanderson.org/estimate/ | Yoshihara et al. 2013, Nat Comm | 表达矩阵 | 纯度评分 | — | — | 否 | 是 | 否 | 免疫浸润估计 |
| 癌症 | TMB | B | TCGAbiolinks | https://github.com/BioinformaticsFMRP/TCGAbiolinks | https://bioconductor.org/packages/TCGAbiolinks | Colaprico et al. 2016, Cancer Res | TCGA | 分析数据 | TCGAbiolinks | — | 否 | 是 | 否 | TCGA 下载 |

## 30. 免疫组库 / 单细胞免疫

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 免疫组库 | 组装 | A | CellRanger V(D)J | https://github.com/10XGenomics/cellranger | https://support.10xgenomics.com/ | 10x Genomics | FASTQ | 克隆型 | — | — | 否 | 是 | 否 | 需 10x |
| 免疫组库 | 分析 | B | immunarch | https://github.com/immunomind/immunarch | https://immunarch.com/ | Evseev et al. 2022 | 克隆型 | 多样性图 | immunarch | — | 是 | 是 | 否 | R |
| 免疫组库 | 分析 | B | scRepertoire | https://github.com/ncborcherding/scRepertoire | https://ncborcherding.github.io/scRepertoire/ | Borcherding et al. 2020, Bioinformatics | 单细胞VDJ | 整合图 | scRepertoire | Seurat | 是 | 是 | 是 | 结合表达 |

## 31. 药物发现 / 虚拟筛选

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 药物发现 | 分子操作 | A | RDKit | https://github.com/rdkit/rdkit | https://www.rdkit.org/ | Landrum 2010 | SMILES/MOL | 描述符 | RDKit | — | 否 | 是 | 是 | 化学信息学基础 |
| 药物发现 | 对接 | A | AutoDock Vina | https://github.com/ccsb-scripps/AutoDock-Vina | https://vina.scripps.edu/ | Eberhardt et al. 2021, J Chem Inf | 配体+受体 | 结合姿态 | PyMOL | ChimeraX | 是 | 是 | 是 | 分子对接 |
| 药物发现 | 深度学习 | B | DeepChem | https://github.com/deepchem/deepchem | https://deepchem.io/ | Ramsundar et al. 2019 | 分子/任务 | 模型 | matplotlib | — | 否 | 否 | 是 | 分子 ML |
| 药物发现 | 性质预测 | B | chemprop | https://github.com/chemprop/chemprop | https://github.com/chemprop/chemprop | Yang et al. 2019, J Chem Inf | SMILES | 性质 | — | — | 否 | 否 | 是 | 消息传递 NN |
| 药物发现 | 成药性 | C | ADMETlab | http://admet.scbdd.com/ | http://admet.scbdd.com/ | Xiong et al. 2021, J Chem Inf | SMILES | ADMET | — | — | 否 | 是 | 是 | 药代预测 |

## 32. 分子动力学药物设计

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 药物设计 | 模拟 | A | GROMACS | https://github.com/gromacs/gromacs | https://www.gromacs.org/ | Abraham et al. 2015 | 拓扑+坐标 | 轨迹 | MDAnalysis | PyMOL | 否 | 是 | 否 | 结合自由能 |
| 药物设计 | 结合自由能 | B | g_mmpbsa | https://github.com/biochem-fan/g_mmpbsa | https://github.com/biochem-fan/g_mmpbsa | Kumari et al. 2014, J Adv Res | 轨迹 | ΔG | — | — | 否 | 是 | 否 | MM-PBSA |

## 33. 转录因子 / 启动子

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TF | 基序 | A | HOMER | http://homer.ucsd.edu/ | http://homer.ucsd.edu/ | Heinz et al. 2010, Mol Cell | FASTA/Peak | 基序 | HOMER | — | 否 | 是 | 否 | 基序发现 |
| TF | 足迹 | B | TOBIAS | https://github.com/loosolab/TOBIAS | https://github.com/loosolab/TOBIAS | Bentsen et al. 2020, Genome Biology | ATAC+Motif | 足迹图 | TOBIAS | — | 是 | 是 | 否 | 转录因子活性 |
| TF | 数据库 | B | JASPAR | https://jaspar.genereg.net/ | https://jaspar.genereg.net/ | Castro-Mondragon et al. 2022, Bioinformatics | TF 名 | 矩阵 | — | — | 否 | 否 | 否 | 基序数据库 |

## 34. 基因编辑 / CRISPR

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRISPR | 设计 | B | CRISPOR | http://crispor.tefor.net/ | http://crispor.tefor.net/ | Haeussler et al. 2016, PLoS One | 序列+靶点 | gRNA | — | — | 否 | 否 | 否 | 在线设计 |
| CRISPR | 脱靶 | B | Cas-OFFinder | https://github.com/snugel/cas-offinder | https://github.com/snugel/cas-offinder | Bae et al. 2014, Bioinformatics | gRNA | 脱靶位点 | — | — | 否 | 否 | 否 | 脱靶搜索 |
| CRISPR | 筛选分析 | B | MAGeCK | https://github.com/mingzhuo/mageck | https://sourceforge.net/projects/mageck/ | Li et al. 2014, Genome Biology | sgRNA 计数 | 基因评分 | MAGeCK | — | 否 | 否 | 否 | 筛选 |

## 35. 蛋白质设计

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 蛋白设计 | 序列设计 | A | ProteinMPNN | https://github.com/dauparas/ProteinMPNN | https://github.com/dauparas/ProteinMPNN | Dauparas et al. 2022, Science | 结构 | 序列 | PyMOL | — | 否 | 是 | 否 | 逆向折叠 |
| 蛋白设计 | 结构预测 | A | RFdiffusion | https://github.com/RosettaCommons/RFdiffusion | https://github.com/RosettaCommons/RFdiffusion | Watson et al. 2023, Nature | 条件 | 结构 | PyMOL | ChimeraX | 是 | 是 | 否 | 生成式设计 |
| 蛋白设计 | 评估 | B | ColabFold | https://github.com/sokrypton/ColabFold | https://github.com/sokrypton/ColabFold | Mirdita et al. 2022 | 序列 | 结构 | PyMOL | — | 是 | 是 | 否 | 验证设计 |

## 36. 代谢通路 / 系统生物学

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 系统生物 | 建模 | A | COPASI | https://github.com/copasi/COPASI | http://copasi.org/ | Hoops et al. 2006, Bioinformatics | 反应网络 | 动力学 | — | — | 否 | 是 | 否 | 生化建模 |
| 系统生物 | SBML | B | tellurium | https://github.com/sys-bio/tellurium | https://tellurium.analogmachine.org/ | Choi et al. 2018, PLoS Comp Biol | SBML | 模拟 | tellurium | — | 否 | 否 | 否 | Python |

## 37. 基因组组装 / 基因组学

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 基因组 | 组装 | A | SPAdes | https://github.com/ablab/spades | https://github.com/ablab/spades | Bankevich et al. 2012, J Comp Biol | 读长 | 组装 | Bandage | — | 否 | 否 | 否 | 微生物常用 |
| 基因组 | 组装图 | B | Bandage | https://github.com/rrwick/Bandage | https://github.com/rrwick/Bandage | Wick et al. 2015, Bioinformatics | 组装图 | 可视化 | Bandage | — | 是 | 否 | 否 | 查看 contig 图 |
| 基因组 | 注释 | A | prokka | https://github.com/tseemann/prokka | https://github.com/tseemann/prokka | Seemann 2014, PLoS One | 组装 | 注释 | — | — | 否 | 否 | 否 | 原核注释 |
| 基因组 | 基因预测 | B | AUGUSTUS | https://github.com/Khmer78/Augustus | https://github.com/Khmer78/Augustus | Stanke et al. 2008 | 基因组 | 基因模型 | — | — | 否 | 否 | 否 | 真核预测 |

## 38. 宏转录组 / 功能宏基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 功能宏基因 | 比对 | A | HUMAnN | https://github.com/biobakery/humann | https://github.com/biobakery/humann | Franzosa et al. 2018, Nat Methods | 测序 | 通路丰度 | — | phyloseq | 否 | 是 | 否 | 通路水平 |
| 功能宏基因 | 基因 | A | metaSPAdes | https://github.com/ablab/spades | https://github.com/ablab/spades | Nurk et al. 2017, Genome Research | 宏基因读长 | 组装 | Bandage | — | 否 | 否 | 否 | 宏组装 |
| 功能宏基因 | 分箱 | B | MetaBAT2 | https://github.com/bxlab/metaBAT2 | https://github.com/bxlab/metaBAT2 | Kang et al. 2019, PeerJ | 组装 | MAG | — | — | 否 | 否 | 否 | 宏基因组分箱 |

## 39. 单细胞 ATAC-seq

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scATAC | 分析 | A | Signac | https://github.com/stuart-lab/signac | https://stuartlab.org/signac/ | Stuart et al. 2021, Cell | 峰/片段 | 嵌入 | Signac | Seurat | 是 | 是 | 是 | 与 Seurat 整合 |
| scATAC | 分析 | B | ArchR | https://github.com/GreenleafLab/ArchR | https://www.archrproject.com/ | Granja et al. 2021, Nat Gen | 片段文件 | 轨迹/拟态 | ArchR | — | 是 | 是 | 是 | 大内存需求 |
| scATAC | 峰调用 | B | MACS2 | https://github.com/taoliu/MACS | https://github.com/taoliu/MACS | Zhang et al. 2008 | BAM | 峰 | — | pyGenomeTracks | 否 | 是 | 否 | 复用 |

## 40. 空间蛋白 / 质谱成像

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 空间蛋白 | 分析 | B | Seurat | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Stuart et al. 2021, Cell | 空间蛋白 | 嵌入 | Seurat | — | 是 | 是 | 是 | CODEX/IMC |
| 空间蛋白 | 质谱成像 | C | Cardinal | https://github.com/PNNL-Comp-Mass-Spec/Cardinal | https://cardinalmsi.org/ | Bemis et al. 2016, J Am Soc Mass Spectrom | imzML | 离子图 | Cardinal | — | 是 | 是 | 否 | R |

## 41. 神经科学 / 脑图谱

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 神经科学 | 单细胞 | A | Seurat/Scanpy | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | 通用 | 表达矩阵 | 细胞类型 | Seurat | CellChat | 是 | 是 | 是 | 脑细胞注释 |
| 神经科学 | 脑区参考 | B | Allen Brain Atlas | https://github.com/AllenInstitute | https://alleninstitute.org/ | 参考库 | 基因表达 | 脑区映射 | — | — | 否 | 是 | 否 | 注释参考 |
| 神经科学 | 空间 | B | Squidpy | https://github.com/scverse/squidpy | https://squidpy.readthedocs.io/ | Palla et al. 2022 | 空间计数 | 空间图 | Squidpy | — | 是 | 是 | 是 | 脑切片 |

## 42. 药物重定位

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 药物重定位 | 网络 | A | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | 通用 | 药物-靶点-疾病 | 网络 | Cytoscape | — | 是 | 是 | 是 | 网络药理核心 |
| 药物重定位 | 数据库 | B | DrugBank | https://go.drugbank.com/ | https://go.drugbank.com/ | Wishart et al. 2018, Nucleic Acids | 药物名 | 靶点 | — | Cytoscape | 否 | 是 | 是 | 数据库 |
| 药物重定位 | 知识图谱 | B | Neo4j | https://github.com/neo4j/neo4j | https://neo4j.com/docs/ | 通用 | 三元组 | 图 | Neo4j | pyvis | 否 | 是 | 是 | 药食同源可用 |

## 43. 微生物-宿主互作（肠脑轴）

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 肠脑轴 | 多组学 | A | mixOmics | https://github.com/mixOmicsTeam/mixOmics | https://mixomics.org/ | Rohart et al. 2017 | 多组学 | 整合 | mixOmics | — | 是 | 是 | 是 | 菌群+代谢+宿主 |
| 肠脑轴 | 群落 | A | phyloseq | https://github.com/joey711/phyloseq | https://joey711.github.io/phyloseq/ | McMurdie & Holmes 2013 | ASV 表 | α/β 多样性 | phyloseq | ggplot2 | 是 | 是 | 否 | 菌群变化 |
| 肠脑轴 | 机制图 | A | cartoon-mechanism | 本仓库 | 本仓库 SKILL.md | 本仓库 | 中文描述 | 卡通机制图 | SVG/bioicons | — | 是 | 是 | 是 | 肠脑轴示意图核心 |
| 肠脑轴 | 网络 | B | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | 通用 | 分子网络 | 网络图 | Cytoscape | — | 是 | 是 | 是 | 信号通路 |

## 44. 表型 / GWAS

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GWAS | 关联 | A | PLINK | https://github.com/chrchang/plink-ng | https://www.cog-genomics.org/plink/ | Chang et al. 2015, GigaScience | 基因型+表型 | 关联 P | — | CMplot | 否 | 是 | 否 | 标准工具 |
| GWAS | 可视化 | B | CMplot | https://github.com/YinLiLin/RCMplot | https://github.com/YinLiLin/RCMplot | Yin et al. 2021 | 位点 P | Manhattan | CMplot | — | 是 | 否 | 否 | 复用 |
| GWAS | 多基因分 | B | PRSice | https://github.com/PRStats/PRSice | https://www.prsice.info/ | Choi & O'Reilly 2019, GigaScience | 基因型 | PRS | PRSice | — | 是 | 是 | 否 | 多基因风险 |

## 45. 转录组组装 / 可变剪切

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 可变剪切 | 组装 | A | StringTie2 | https://github.com/skovaka/StringTie2 | https://github.com/skovaka/StringTie2 | Kovaka et al. 2019, Nat Biotech | BAM | 转录本 | — | ggsashimi | 否 | 否 | 否 | 组装 |
| 可变剪切 | 可视化 | B | ggsashimi | https://github.com/guigolab/ggsashimi | https://github.com/guigolab/ggsashimi | Garrido-Martín et al. 2021 | 剪切事件 | sashimi 图 | ggsashimi | — | 是 | 否 | 否 | 剪切可视化 |

## 46. 单细胞多组学（CITE-seq / ATAC+RNA）

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 多模态 | 整合 | A | Seurat WNN | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Hao et al. 2021, Cell | RNA+ADT/ATAC | 加权图 | Seurat | — | 是 | 是 | 是 | 多模态整合 |
| 多模态 | 蛋白 | B | CiteFuse | https://github.com/SydneyBioX/CiteFuse | https://sydneybiox.github.io/CiteFuse/ | Kim et al. 2020, Nucleic Acids | ADT+RNA | 整合 | CiteFuse | — | 是 | 是 | 是 | CITE-seq |
| 多模态 | 分析 | B | totalVI | https://github.com/scverse/scvi-tools | https://docs.scvi-tools.org/ | Gayoso et al. 2021, Nat Methods | 多模态 | 隐变量 | totalVI | — | 是 | 是 | 是 | 深度生成 |

## 47. 基因集变异分析 GSEA

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GSEA | 快速 | A | fgsea | https://github.com/ctlab/fgsea | https://github.com/ctlab/fgsea | Korotkevich et al. 2021 | 排序基因 | 富集 | fgsea | — | 是 | 是 | 否 | 快 |
| GSEA | 经典 | B | GSEA | https://www.gsea-msigdb.org/gsea/ | https://www.gsea-msigdb.org/ | Subramanian et al. 2005, PNAS | 表达矩阵 | 富集 | GSEA | — | 是 | 是 | 否 | MSigDB |

## 48. 临床预测模型

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 临床模型 | 建模 | A | scikit-learn | https://github.com/scikit-learn/scikit-learn | https://scikit-learn.org/ | 通用 | 临床特征 | 模型 | SHAP | matplotlib | 否 | 是 | 否 | 可解释 |
| 临床模型 | 列线图 | B | rms | https://github.com/harrelfe/rms | https://github.com/harrelfe/rms | Harrell 2023 | 数据 | 列线图 | rms | — | 是 | 是 | 否 | R 列线图 |
| 临床模型 | 校准 | B | ggplot2 | https://github.com/tidyverse/ggplot2 | https://ggplot2.tidyverse.org/ | Wickham 2016 | 预测/标签 | 校准曲线 | ggplot2 | — | 是 | 是 | 否 | 复用 |

## 49. 文献计量 / 引文网络

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 文献计量 | 引文网络 | B | bibliometrix | https://github.com/massimoaria/bibliometrix | https://www.bibliometrix.org/ | Aria & Cuccurullo 2017, J Informetrics | BibTeX | 网络/趋势 | bibliometrix | — | 是 | 否 | 否 | R |
| 文献计量 | 共引 | C | VOSviewer | https://www.vosviewer.com/ | https://www.vosviewer.com/ | van Eck & Waltman 2010 | 引文 | 共现图 | VOSviewer | — | 是 | 否 | 否 | 在线 |

## 50. 单细胞图谱 / 细胞注释

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 细胞注释 | 自动 | A | SingleR | https://github.com/dviraran/SingleR | https://github.com/dviraran/SingleR | Aran et al. 2019, Nat Comm | sc 矩阵+参考 | 细胞类型 | — | Seurat | 否 | 是 | 是 | 参考注释 |
| 细胞注释 | marker | A | Seurat | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Satija et al. 2015 | 表达矩阵 | marker 图 | Seurat | scCustomize | 是 | 是 | 是 | 复用 |
| 细胞注释 | 参考库 | B | CellMarker | http://bio-bigdata.hrbmu.edu.cn/CellMarker/ | http://bio-bigdata.hrbmu.edu.cn/CellMarker/ | Zhang et al. 2021, Nucleic Acids | 细胞类型 | marker 基因 | — | — | 否 | 否 | 是 | 数据库 |

## 51. 蛋白质-蛋白质互作 PPI

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PPI | 数据库 | A | STRING | https://github.com/string-db/stringdb | https://string-db.org/ | Szklarczyk et al. 2023 | 蛋白列表 | PPI 网络 | STRING | Cytoscape | 是 | 是 | 是 | 复用 |
| PPI | 可视化 | A | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | Shannon et al. 2003 | 边表 | 网络图 | Cytoscape | — | 是 | 是 | 是 | 复用 |
| PPI | 预测 | B | PIPENN | https://github.com/ibivu/pipenn | https://github.com/ibivu/pipenn | 2020 | 序列 | 互作 | — | Cytoscape | 否 | 否 | 是 | 预测 |

## 52. 基因家族 / 比较基因组

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 比较基因组 | 共线 | B | MCScanX | https://github.com/wyp1125/MCScanX | https://github.com/wyp1125/MCScanX | Wang et al. 2012, Nucleic Acids | 基因位置 | 共线性 | — | — | 否 | 否 | 否 | 植物常用 |
| 比较基因组 | 基因家族 | B | CAFE | https://github.com/hahnlab/CAFE | https://github.com/hahnlab/CAFE | Han et al. 2013 | 基因计数 | 扩张收缩 | — | — | 否 | 否 | 否 | 进化 |

## 53. 甲基化 / 表观遗传时钟

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 甲基化时钟 | 年龄 | B | methylCIPHER | https://github.com/HigginsChenLab/methylCIPHER | https://github.com/HigginsChenLab/methylCIPHER | 2022 | 甲基化 | 表观年龄 | — | — | 否 | 是 | 否 | 复用 methylKit |
| 甲基化时钟 | 可视化 | B | methylKit | https://github.com/al2na/methylKit | https://github.com/al2na/methylKit | Akalin et al. 2012 | 甲基化表 | 差异图 | methylKit | — | 是 | 是 | 否 | 复用 |

## 54. 单细胞信号通路活性

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 通路活性 | 评分 | A | PROGENy | https://github.com/saezlab/progeny | https://github.com/saezlab/progeny | Schubert et al. 2018, Nat Comm | 表达矩阵 | 通路活性 | PROGENy | — | 是 | 是 | 是 | 通路评分 |
| 通路活性 | 活性 | B | GSVA | https://github.com/rcastelo/GSVA | https://github.com/rcastelo/GSVA | Hanzelmann et al. 2013, BMC Bioinf | 表达矩阵 | 通路分数 | GSVA | — | 是 | 是 | 是 | 无监督 |

## 55. 蛋白质结构预测服务

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 结构预测 | 服务 | A | AlphaFold DB | https://github.com/google-deepmind/alphafold | https://alphafold.ebi.ac.uk/ | Varadi et al. 2022, Nucleic Acids | Uniprot ID | 结构 | PyMOL | — | 是 | 是 | 否 | 预计算数据库 |
| 结构预测 | 本地 | A | AlphaFold | https://github.com/google-deepmind/alphafold | https://github.com/google-deepmind/alphafold | Jumper et al. 2021 | 序列 | 模型 | PyMOL | ChimeraX | 是 | 是 | 否 | 复用 |

## 56. 宏基因组组装基因组 MAG

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MAG | 分箱 | A | MetaBAT2 | https://github.com/bxlab/metaBAT2 | https://github.com/bxlab/metaBAT2 | Kang et al. 2019 | 组装 | MAG | — | — | 否 | 否 | 否 | 复用 |
| MAG | 质量 | B | CheckM | https://github.com/Ecogenomics/CheckM | https://github.com/Ecogenomics/CheckM | Parks et al. 2015, Genome Biology | MAG | 完整度 | — | — | 否 | 否 | 否 | 质量评估 |
| MAG | 可视化 | B | anvi'o | https://github.com/merenlab/anvio | https://anvio.org/ | Eren et al. 2015 | MAG | 交互 | anvi'o | — | 是 | 否 | 否 | 复用 |

## 57. 药物组合 / 协同

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 药物组合 | 协同 | B | synergyfinder | https://github.com/ianevski123/synergyfinder | https://synergyfinder.fimm.fi/ | Ianevski et al. 2017, Bioinformatics | 剂量矩阵 | 协同分数 | synergyfinder | — | 是 | 是 | 是 | 网络药理 |
| 药物组合 | 可视化 | B | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | 通用 | 药物对 | 网络 | Cytoscape | — | 是 | 是 | 是 | 复用 |

## 58. 空间细胞互作

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 空间互作 | 邻域 | A | Squidpy | https://github.com/scverse/squidpy | https://squidpy.readthedocs.io/ | Palla et al. 2022 | 空间计数 | 邻域/通信 | Squidpy | — | 是 | 是 | 是 | 复用 |
| 空间互作 | 配体-受体 | B | CellChat | https://github.com/sqjin/CellChat | https://github.com/sqjin/CellChat | Jin et al. 2021 | 空间表达 | 通信 | CellChat | circlize | 是 | 是 | 是 | 复用 |

## 59. 转录调控 / 增强子

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 增强子 | 注释 | B | ROSE | https://github.com/stjude/ROSE | https://github.com/stjude/ROSE | Whyte et al. 2013, Cell | 峰+表达 | 超级增强子 | — | Gviz | 否 | 是 | 否 | 复用 |
| 增强子 | 可视化 | B | pyGenomeTracks | https://github.com/deeptools/pyGenomeTracks | https://pygenometracks.readthedocs.io/ | Lopez-Delisle et al. 2021 | _track | 轨道 | pyGenomeTracks | — | 是 | 是 | 否 | 复用 |

## 60. 菌群-代谢物关联

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 菌-代关联 | 关联 | A | mixOmics | https://github.com/mixOmicsTeam/mixOmics | https://mixomics.org/ | Rohart et al. 2017 | 微生物+代谢 | 关联 | mixOmics | — | 是 | 是 | 是 | 复用 |
| 菌-代关联 | 网络 | B | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | 通用 | 相关边 | 网络 | Cytoscape | — | 是 | 是 | 是 | 复用 |
| 菌-代关联 | 机制图 | A | cartoon-mechanism | 本仓库 | 本仓库 SKILL.md | 本仓库 | 中文描述 | 卡通图 | SVG/bioicons | — | 是 | 是 | 是 | 复用 |

## 61. 蛋白质互作结构

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 蛋白互作结构 | 对接 | A | HADDOCK | https://github.com/haddockmc/haddock3 | https://wenmr.science.uu.nl/haddock/ | van Zundert et al. 2016, J Mol Biol | 结构 | 复合物 | PyMOL | ChimeraX | 是 | 是 | 否 | 数据驱动对接 |
| 蛋白互作结构 | 互作 | B | PLIP | https://github.com/pharmai/plip | https://plip.biotec.tu-dresden.de/ | Salentin et al. 2015 | PDB | 互作图 | PLIP | PyMOL | 是 | 是 | 否 | 复用 |

## 62. 单细胞批量校正 / 整合

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 批次校正 | 整合 | A | Harmony | https://github.com/immunogenomics/harmony | https://github.com/immunogenomics/harmony | Korsunsky et al. 2019 | 嵌入 | 校正 | — | Seurat | 否 | 否 | 是 | 复用 |
| 批次校正 | 整合 | A | Seurat Integrate | https://github.com/satijalab/seurat | https://satijalab.org/seurat/ | Stuart et al. 2019, Cell | 多批次 | 整合 | Seurat | — | 是 | 是 | 是 | 复用 |
| 批次校正 | 整合 | B | scVI | https://github.com/scverse/scvi-tools | https://docs.scvi-tools.org/ | Lopez et al. 2019, Nat Methods | 计数矩阵 | 隐变量 | scVI | — | 是 | 是 | 是 | 深度生成 |

## 63. 基因组变异注释数据库

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 变异库 | 注释 | A | VEP | https://github.com/Ensembl/ensembl-vep | https://www.ensembl.org/info/docs/tools/vep/ | McLaren et al. 2016 | VCF | 注释 | — | — | 否 | 是 | 否 | 复用 |
| 变异库 | 频率 | B | gnomAD | https://github.com/broadinstitute/gnomad-browser | https://gnomad.broadinstitute.org/ | Karczewski et al. 2020, Nature | 变异 ID | 人群频率 | — | — | 否 | 是 | 否 | 数据库 |
| 变异库 | 致病性 | B | ClinVar | https://www.ncbi.nlm.nih.gov/clinvar/ | https://www.ncbi.nlm.nih.gov/clinvar/ | Landrum et al. 2018, Nucleic Acids | 变异 ID | 临床意义 | — | — | 否 | 是 | 否 | 数据库 |

## 64. 三维结构可视化（分子+细胞）

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3D结构 | 分子 | A | PyMOL | https://github.com/schrodinger/pymol-open-source | https://pymol.org/ | Schrödinger | PDB | 分子图 | PyMOL | — | 是 | 是 | 否 | 复用 |
| 3D结构 | 细胞 | B | UCSF ChimeraX | https://github.com/RBVI/ChimeraX | https://www.rbvi.ucsf.edu/chimerax/ | Pettersen et al. 2021 | PDB/地图 | 3D | ChimeraX | — | 是 | 是 | 否 | 复用 |
| 3D结构 | 卡通 | A | cartoon-mechanism | 本仓库 | 本仓库 SKILL.md | 本仓库 | 中文描述 | 卡通图 | SVG/bioicons | — | 是 | 是 | 是 | 机制图 |

## 65. 代谢流 / 同位素示踪

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 代谢流 | 通量 | B | isotopia | https://github.com/isoverse/isotopia | https://github.com/isoverse/isotopia | 2014 | 同位素 | 校正 | — | — | 否 | 是 | 否 | 13C |
| 代谢流 | 建模 | B | INCA | https://mfa.vueinnovations.com/ | https://mfa.vueinnovations.com/ | Young et al. 2008, Biotech J | 标记数据 | 通量 | — | — | 否 | 是 | 否 | 13C-FLUX |

## 66. 单细胞 RNA 速率

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RNA速率 | 计算 | A | scVelo | https://github.com/scverse/scvelo | https://scvelo.readthedocs.io/ | Bergen et al. 2020 | 剪接计数 | 速度场 | scVelo | — | 是 | 否 | 是 | 复用 |
| RNA速率 | 动力学 | B | dynamo | https://github.com/aristoteleo/dynamo-release | https://dynamo-release.readthedocs.io/ | Qiu et al. 2022, Cell | 多模态 | 动力学 | dynamo | — | 是 | 否 | 是 | 连续建模 |

## 67. 药物靶点相互作用 DTI

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DTI | 预测 | A | DeepPurpose | https://github.com/kexinhuang12345/DeepPurpose | https://github.com/kexinhuang12345/DeepPurpose | Huang et al. 2020, Cell Chem | 药物+靶 | 亲和力 | matplotlib | — | 否 | 是 | 是 | 深度学习 |
| DTI | 数据库 | B | BindingDB | https://www.bindingdb.org/ | https://www.bindingdb.org/ | Gilson et al. 2016, J Med Chem | 名称 | 亲和力 | — | Cytoscape | 否 | 是 | 是 | 数据库 |
| DTI | 网络 | B | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | 通用 | DTI 边 | 网络 | Cytoscape | — | 是 | 是 | 是 | 复用 |

## 68. 空间域识别

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 空间域 | 识别 | A | SpaGCN | https://github.com/jianhuupenn/SpaGCN | https://github.com/jianhuupenn/SpaGCN | Hu et al. 2021, Nat Sci Data | 空间计数 | 域标注 | SpaGCN | — | 是 | 是 | 是 | GCN |
| 空间域 | 识别 | B | stLearn | https://github.com/BiomedicalMachineLearning/stLearn | https://stlearn.readthedocs.io/ | Pham et al. 2023, Genome Biology | 空间计数 | 域/轨迹 | stLearn | — | 是 | 是 | 是 | 综合 |

## 69. 系统药理 / 网络药理学流程

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 系统药理 | 成分获取 | A | TCMSP | https://tcmspw.com/ | https://tcmspw.com/ | Ru et al. 2014, J Cheminform | 中药名 | 成分/靶 | — | Cytoscape | 否 | 是 | 是 | 药食同源上游 |
| 系统药理 | 网络 | A | Cytoscape | https://github.com/cytoscape/cytoscape | https://cytoscape.org/ | Shannon et al. 2003 | 边表 | 网络 | Cytoscape | — | 是 | 是 | 是 | 复用 |
| 系统药理 | 拓扑 | A | igraph | https://github.com/igraph/igraph | https://igraph.org/ | Csardi & Nepusz 2006 | 图 | 拓扑 | ggraph | — | 否 | 否 | 是 | 复用 |
| 系统药理 | 通路 | A | clusterProfiler | https://github.com/YuLab-SMU/clusterProfiler | https://yulab-smu.top/ | Wu et al. 2021 | 靶基因 | 富集 | enrichplot | — | 是 | 是 | 是 | 复用 |
| 系统药理 | 机制图 | A | cartoon-mechanism | 本仓库 | 本仓库 SKILL.md | 本仓库 | 中文描述 | 卡通图 | SVG/bioicons | — | 是 | 是 | 是 | 核心差异化 |

## 70. 可复现研究 / 工作流

| 一级领域 | 二级任务 | 推荐等级 | 工具名 | GitHub 链接 | 官方文档 | 代表论文/期刊 | 输入数据 | 输出结果 | 主图画图工具 | 补图画图工具 | 是否适合主图 | 是否适合临床/机制文章 | 是否适合单细胞/多组学/网络药理学/知识图谱 | 注意事项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 可复现 | 流程 | A | Nextflow | https://github.com/nextflow-io/nextflow | https://www.nextflow.io/ | Di Tommaso et al. 2017, Nat Biotech | 流程脚本 | 可复现管道 | — | — | 否 | 否 | 否 | nf-core 生态 |
| 可复现 | 报告 | A | MultiQC | https://github.com/MultiQC/multiqc | https://multiqc.info/ | Ewels et al. 2016 | 日志 | 报告 | MultiQC | — | 是 | 是 | 否 | 复用 |
| 可复现 | 环境 | B | Snakemake | https://github.com/snakemake/snakemake | https://snakemake.readthedocs.io/ | Koster & Rahmann 2012, Bioinformatics | 规则 | 管道 | — | — | 否 | 否 | 否 | Python 工作流 |
| 可复现 | 笔记本 | B | Jupyter | https://github.com/jupyter/notebook | https://jupyter.org/ | Kluyver et al. 2016 | 代码 | 可复现 | matplotlib | — | 否 | 否 | 否 | 通用 |

---

## 通用基础设施（任何图都可调用，跨领域重复属正常）

| 工具 | GitHub | 用途 | 主图适用性 |
|---|---|---|---|
| ggplot2 | https://github.com/tidyverse/ggplot2 | R 通用统计图 | 是 |
| ComplexHeatmap | https://github.com/jokergoo/ComplexHeatmap | 复杂热图 | 是 |
| matplotlib | https://github.com/matplotlib/matplotlib | Python 基础图 | 是 |
| seaborn | https://github.com/mwaskom/seaborn | Python 统计图 | 是 |
| SHAP | https://github.com/shap/shap | 可解释性 | 是 |
| UMAP | https://github.com/lmcinnes/umap | 降维 | 是 |
| circlize | https://github.com/jokergoo/circlize | 弦图/圈图 | 是 |
| Cytoscape | https://github.com/cytoscape/cytoscape | 网络图 | 是 |
| PyMOL | https://github.com/schrodinger/pymol-open-source | 分子结构 | 是 |
| IGV | https://github.com/igvteam/igv | 基因组浏览器 | 否（交互） |
| MultiQC | https://github.com/MultiQC/multiqc | QC 汇总 | 是 |

> 本表为不加精炼的完整版，覆盖全部 70 个领域，每个领域含全部 15 个字段。GitHub 链接为仓库主页（多数工具同时有 Bioconda/PyPI/CRAN 渠道）。如需 clone 具体仓库，参考 `references/REPO_DRAWING_FULL.md` 的 120+ 仓库索引与 `references/bioinfo_toolmap.md` 的去重工具地图。
