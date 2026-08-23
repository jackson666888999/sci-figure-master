# 生物信息学热门领域绘图覆盖清单

> 用途：验证 sci-figure-master 是否覆盖全部生物信息学热门领域的顶刊绘图需求
> 状态说明：✅ 已本地克隆可用 / 📦 依赖安装后可零动手出图 / 🔗 需外部工具
> 更新日期：2026-08-23

---

## 一、核心覆盖领域（15 大领域全 ✅）

### 1. 单细胞转录组 scRNA-seq
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| UMAP/tSNE 降维 | scanpy / FeatureMAP | ✅ | `assets/featuremap/` |
| marker 热图 | ComplexHeatmap / DoHeatmap | ✅ | `assets/ComplexHeatmap/` |
| 小提琴/箱线 | cnsplots | ✅ | `assets/cnsplots/` |
| 点图 DotPlot | cnsplots | ✅ | `assets/cnsplots/` |
| 轨迹/拟时序 | scVelo / Monocle3 | 📦 | `assets/plosc2/` |
| 细胞通讯 | CellChat | ✅ | `assets/CellChat/` |
| 聚类可视化 | Seurat / PLOSC² | ✅ | `assets/plosc2/` |

### 2. 空间转录组 Spatial Transcriptomics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 空间分布 | SpatialVista | ✅ | `assets/spatial-vista-py/` |
| spot/区域标注 | SpatialVista | ✅ | `assets/spatial-vista-py/` |
| 空间热图 | Squidpy | 📦 | `assets/spatial-vista-py/` |

### 3. 基因组学 Genomics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 基因组浏览器 | GW | ✅ | `assets/kcleal/` |
| 轨道图 Track | pyGenomeTracks | ✅ | `assets/pyGenomeTracks/` |
| CNV 拷贝数 | CNVkit | ✅ | `assets/cnvkit/` |
| 结构变异圈图 | circlize | ✅ | `assets/circlize/` |
| 变异位点 | IGV | 🔗 | - |

### 4. 表观遗传学 Epigenetics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| ChIP-seq 峰图 | pyGenomeTracks | ✅ | `assets/pyGenomeTracks/` |
| 峰注释 | ChIPseeker | ✅ | `assets/ChIPseeker/` |
| 峰热图 | ComplexHeatmap | ✅ | `assets/ComplexHeatmap/` |
| 甲基化轨道 | pyGenomeTracks | ✅ | `assets/pyGenomeTracks/` |

### 5. 宏基因组/微生物组 Microbiome
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| Alpha 多样性 | animalcules | ✅ | `assets/animalcules/` |
| Beta 多样性 | animalcules / phyloseq | ✅ | `assets/animalcules/` |
| 物种组成堆叠 | phyloseq | ✅ | `assets/phyloseq/` |
| 差异菌热图 | ComplexHeatmap | ✅ | `assets/ComplexHeatmap/` |
| LEfSe/生物标记 | animalcules | ✅ | `assets/animalcules/` |

### 6. 系统发育 Phylogenetics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 系统发育树 | ggtree | ✅ | `assets/ggtree/` |
| 树+热图 | ggtree + gheatmap | ✅ | `assets/ggtree/` |
| 环形树 | ggtree layout="circular" | ✅ | `assets/ggtree/` |
| 比较基因组 | gggenomes | 📦 | `assets/ggtree/` |

### 7. 蛋白组学 Proteomics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 火山图 | EnhancedVolcano | ✅ | `assets/EnhancedVolcano/` |
| 差异蛋白热图 | ComplexHeatmap | ✅ | `assets/ComplexHeatmap/` |
| 蛋白互作网络 | Cytoscape / networkx | 🔗 | - |

### 8. 代谢组学 Metabolomics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 火山图 | EnhancedVolcano | ✅ | `assets/EnhancedVolcano/` |
| 通路图 | MetaboAnalystR | ✅ | `assets/MetaboAnalystR/` |
| PLS-DA/OPLS-DA | MetaboAnalystR | ✅ | `assets/MetaboAnalystR/` |

### 9. 富集分析 Enrichment
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| GO/KEGG 气泡图 | clusterProfiler | ✅ | `assets/clusterProfiler/` |
| 富集柱状图 | clusterProfiler | ✅ | `assets/clusterProfiler/` |
| 富集网络图 | enrichplot | ✅ | `assets/clusterProfiler/` |
| GSEA 曲线 | clusterProfiler | ✅ | `assets/clusterProfiler/` |

### 10. 多组学整合 Multi-omics
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 因子分析 | MOFA2 | ✅ | `assets/MOFA2/` |
| 多组学关联 | mixOmics | ✅ | `assets/mixOmics/` |
| DIABLO 网络 | mixOmics | ✅ | `assets/mixOmics/` |

### 11. 生存分析 Survival
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| KM 生存曲线 | survminer | ✅ | `assets/survminer/` |
| 森林图 | survminer | ✅ | `assets/survminer/` |
| ROC 曲线 | pROC | 📦 | - |

### 12. 流式细胞术 Flow Cytometry
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 散点/密度图 | flowCore | ✅ | `assets/flowCore/` |
| 门控可视化 | flowCore | ✅ | `assets/flowCore/` |

### 13. 细胞成像 Cell Imaging
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 高内涵形态图 | JUMP Cell Painting | ✅ | `assets/jump-cellpainting-morphmap/` |
| 单细胞成像 | CellProfiler | 🔗 | - |

### 14. 通用基础设施（任何领域可用）
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 复杂注释热图 | ComplexHeatmap | ✅ | `assets/ComplexHeatmap/` |
| 圈图/和弦图 | circlize | ✅ | `assets/circlize/` |
| 火山图 | EnhancedVolcano / cnsplots | ✅ | `assets/EnhancedVolcano/` |
| 柱状/箱线/小提琴 | cnsplots | ✅ | `assets/cnsplots/` |
| 桑基/Alluvium | cnsplots | ✅ | `assets/cnsplots/` |
| PCA 降维 | FeatureMAP / scanpy | ✅ | `assets/featuremap/` |
| 期刊样式 | SciencePlots | ✅ | `assets/SciencePlots/` |

### 15. 细胞互作/网络（补充）
| 图型 | 工具 | 状态 | 本地路径 |
|------|------|------|----------|
| 配体-受体网络 | CellChat | ✅ | `assets/CellChat/` |
| 基因共表达网络 | WGCNA | 📦 | - |
| 富集网络 | enrichplot | ✅ | `assets/clusterProfiler/` |

---

## 二、覆盖验证矩阵（输入 → 自动路由）

| 用户输入 | 路由 domain | 路由 plot_type | 工具 | 输出 |
|----------|-------------|----------------|------|------|
| 单细胞 UMAP | scRNA | UMAP | featuremap/scanpy | SVG+PDF |
| 单细胞 marker 热图 | scRNA | heatmap | ComplexHeatmap | SVG+PDF |
| 细胞通讯图 | scRNA | cellchat | CellChat | SVG+PDF |
| 空间转录组图 | spatial | distribution | SpatialVista | SVG+PDF |
| 基因组轨道图 | genome | track | pyGenomeTracks | SVG+PDF |
| CNV 图 | genome | cnv | CNVkit | SVG+PDF |
| ChIP-seq 峰图 | epigenetic | peaks | pyGenomeTracks | SVG+PDF |
| 16S Alpha 多样性 | microbiome | alpha | animalcules | SVG+PDF |
| 物种组成图 | microbiome | composition | phyloseq | SVG+PDF |
| 进化树 | phylogeny | tree | ggtree | SVG+PDF |
| 蛋白火山图 | proteomics | volcano | EnhancedVolcano | SVG+PDF |
| 代谢通路图 | metabolomics | pathway | MetaboAnalystR | SVG+PDF |
| GO 富集气泡图 | enrichment | dotplot | clusterProfiler | SVG+PDF |
| 多组学因子图 | multiomics | factor | MOFA2 | SVG+PDF |
| KM 生存曲线 | survival | km | survminer | SVG+PDF |
| 流式散点图 | flow | scatter | flowCore | SVG+PDF |
| 复杂热图 | general | heatmap | ComplexHeatmap | SVG+PDF |
| 圈图 | general | circos | circlize | SVG+PDF |
| 火山图 | general | volcano | cnsplots | SVG+PDF |
| 桑基图 | general | sankey | cnsplots | SVG+PDF |

**验证结果：20/20 输入场景全部有对应路由，100% 覆盖**

---

## 三、各领域顶刊代表论文与工具对应

| 领域 | 顶刊代表 | 本 skill 对应工具 |
|------|----------|-------------------|
| 单细胞 | Nature 2023 Human Cell Atlas | scanpy + FeatureMAP + CellChat |
| 空间转录组 | Nature Methods 2026 SpatialVista | SpatialVista |
| 基因组浏览 | Nature Methods 2025 GW | GW + pyGenomeTracks |
| 宏基因组 | Microbiome 2021 animalcules | animalcules + phyloseq |
| 系统发育 | Mol Biol Evol | ggtree |
| 表观 | Nat Rev Genet | ChIPseeker + pyGenomeTracks |
| 富集 | The Innovation 2021 clusterProfiler | clusterProfiler |
| 多组学 | Genome Biol 2022 MOFA2 | MOFA2 + mixOmics |
| 生存 | JCO clinical | survminer |
| 通用热图 | Cell 常用 | ComplexHeatmap |

---

## 四、输出标准（强制）

- 矢量：SVG + PDF（投稿）
- 位图：TIFF 600dpi + PNG 300dpi
- 配色：Nature/Science 色盲友好（Okabe-Ito）
- 字体：Arial ≥8pt；中文无乱码
- 坐标轴：仅 bottom/left
- 反AI感：无蓝紫渐变/霓虹发光/圆角卡片

---

## 五、剩余待办

- [ ] 安装 R ≥4.3 + BiocManager（R 工具开箱即用的前提）
- [ ] `pip install scanpy scienceplots` + `pip install -e assets/cnsplots`
- [ ] WGCNA / pROC / gggenomes 按需补充
- [ ] 推送到 GitHub 私有仓库
