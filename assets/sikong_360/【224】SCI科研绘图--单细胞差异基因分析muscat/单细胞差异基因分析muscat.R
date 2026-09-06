################################################################################
#                              差异分析
################################################################################
#加载单细胞数据，我这里用的人的示例数据（无意义，仅仅用于演示）
#这里差异分析我们使用muscat包的pseudobulk分析。众所周知，seurat差异基因分析容易有假阳性。
#我们做单细胞差异基因的目的是为了分析两组间细胞的差异，而不是单个细胞本身的差异。

#pseudobulk分析详细参考：https://www.nature.com/articles/s41467-021-25960-2
#muscat包详细参考：http://www.bioconductor.org/packages/release/bioc/vignettes/muscat/inst/doc/analysis.html
library(Seurat)
library(muscat)
library(SingleCellExperiment)
library(dplyr)
human_data <- readRDS("D:/KS项目/公众号文章/单细胞nichenet/human_data.rds")
human_sce <- subset(human_data, celltype=='Mast', invert=T)#由于本示例数据中Mast cell数量太少，所以直接去除
#很多时候，不论是做monocle、cellchat、cellphonedb或者其他的，有小伙伴就会发现，
#我提取了细胞亚群，UMAP上已经没有其他细胞类型了，但是table查看的时候还有其他细胞，细胞数是0，
#一般情况下不会有影响，但是有些分析会出问题，运行下面的代码，将不需要的细胞彻底去除！
human_sce$celltype = droplevels(human_sce$celltype,
                                exclude = setdiff(levels(human_sce$celltype),
                                                  unique(human_sce$celltype)))

DefaultAssay(human_sce) <- "RNA"
human_sce <- as.SingleCellExperiment(human_sce)#将seurat对象转化为SingleCellExperiment对象

#Prepare SCE for DS analysis
human_sce <- prepSCE(human_sce,#单细胞对象
                     kid = "celltype",#cluster_id,细胞聚类分群，例如seurat——clusters或者celltype
                     gid = "group",#group——id，分组信息
                     sid = "orig.ident",#sample_id, 样本信息
                     drop=T)
human_sce$group_id <- factor(human_sce$group_id, levels=c("BM", "GM"))

nk <- length(kids <- levels(human_sce$cluster_id))
ns <- length(sids <- levels(human_sce$sample_id))
names(kids) <- kids
names(sids) <- sids
t(table(human_sce$cluster_id, human_sce$sample_id))

#将单细胞数据聚合为pseudobulk data
pb <- aggregateData(human_sce,
                    assay = "counts", 
                    fun = "sum",
                    by = c("cluster_id", "sample_id"))
#类似于PCA
(pb_mds <- pbMDS(pb))#在进行任何正式测试之前，我们可以计算聚合信号的多维缩放(MDS)图，以探索总体样本相似性。

#差异分析
pb$group_id <- factor(pb$group_id, levels=c("BM", "GM"))
res <- pbDS(pb, verbose = FALSE)#pseudobulk DS analysis
tmp <- human_sce
counts(tmp) <- as.matrix(counts(tmp))
result_table <- resDS(tmp, res, bind = "row", frq = FALSE, cpm = FALSE)#获得差异结果
rm(tmp)


#将表达某一基因的BM/GM细胞群中的比例添加到result_table，用于后期细胞基因表达比例筛选
human_sce <- subset(human_data, celltype=='Mast', invert=T)
count_mat <- as.matrix(human_sce[["RNA"]]@data) > 0
cluster_list <- unique(result_table$cluster_id)

result_table$BM.frq <- 0
BM_cells <- colnames(human_sce)[human_sce$group == "BM"]
for(i in 1:length(cluster_list)){
  cluster_cells <- colnames(human_sce)[human_sce$celltype == cluster_list[i]]
  test_cells <- intersect(BM_cells, cluster_cells)
  row_ind <- which(result_table$cluster_id == cluster_list[i])
  frq <- rowSums(count_mat[result_table$gene[row_ind],test_cells]) / length(test_cells)
  result_table$BM.frq[row_ind] <- frq
}


GM_cells <- colnames(human_sce)[human_sce$group == "GM"]
result_table$GM.frq <- 0
for(i in 1:length(cluster_list)){
  cluster_cells <- colnames(human_sce)[human_sce$celltype == cluster_list[i]]
  test_cells <- intersect(GM_cells, cluster_cells)
  row_ind <- which(result_table$cluster_id == cluster_list[i])
  frq <- rowSums(count_mat[result_table$gene[row_ind],test_cells]) / length(test_cells)
  result_table$GM.frq[row_ind] <- frq
}


write.csv(result_table, file = "result_table.csv", row.names = F)

#这里对比一下Findmarkers与muscat得到的差异基因结果
####FindMarkers
Mac <- subset(human_data, celltype=="Macrophage")
Mac_DEGs <- FindMarkers(human_data,
                        min.pct = 0,
                        logfc.threshold = 0.25,
                        group.by = 'group',
                        ident.1 ="GM",
                        ident.2="BM")

Mac_DEGs_Findmarker_sig <- Mac_DEGs[Mac_DEGs$p_val < 0.05 &
                                      abs(Mac_DEGs$avg_log2FC) > 0.25, ]


####muscat
Mac_muscat_DEGs <- subset(result_table, cluster_id=='Macrophage')
Mac_muscat_DEGs_sig <- Mac_muscat_DEGs[Mac_muscat_DEGs$p_val < 0.05 &
                                         abs(Mac_muscat_DEGs$logFC) > 0.25&
                                         Mac_muscat_DEGs$BM.frq>0.1&
                                         Mac_muscat_DEGs$GM.frq>0.1, ]
rownames(Mac_muscat_DEGs_sig) <- Mac_muscat_DEGs_sig$gene

library(devtools)
install_github("js229/Vennerable")
library(Vennerable)

Set1 <- as.list(rownames(Mac_DEGs_Findmarker_sig))
Set2 <- as.list(Mac_muscat_DEGs_sig$gene)
example <-list(Set1=Set1,Set2=Set2)


Veenplot <- Venn(example)
Veenplot<-Veenplot[, c("Set1", "Set2")]
plot(Veenplot, doWeights = TRUE)



#差别还是挺大的
same_gene <- Veenplot@IntersectionSets$`11`
data <- cbind(Mac_DEGs_Findmarker_sig[same_gene,][,2],
              Mac_muscat_DEGs_sig[same_gene,][,3])
colnames(data) <- c("Seurat", "Muscat")
data <- as.data.frame(data)

library(ggpubr)
ggscatter(data,x="Seurat",y="Muscat",
          add = "reg.line",
          conf.int = T,
          color = '#0f8096')+
  stat_cor(label.x = 0.2, label.y = 0)

