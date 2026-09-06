setwd('C:/Users/34790/Desktop/单细胞seurat替换UMAP坐标')
#===============================================================================
#读入数据
library(ggplot2)
library(Seurat)
meta <- read.table('GSE133345_Annotations.txt', header = T, row.names = 1)

folders=list.files('./GSE133345_RAW/',pattern='^[GSM]')#文件夹目录
folders

Exp_matrix = lapply(folders,function(x){ 
  read.table(paste0('./GSE133345_RAW/',x),header = T, row.names = 1)
})#批量读入

names(Exp_matrix) <- substr(folders, 1, 10)#取向量每个元素的前10个字符，这里就是样本GSM号，给上面的表达矩阵list命名

scelist <- list()
for (i in 1:length(Exp_matrix)) {
  sce <- CreateSeuratObject(counts = Exp_matrix[[i]])
  sce$sample <- names(Exp_matrix)[i]
  scelist[[i]] <- sce
  
}

#merge data
sce = merge(scelist[[1]], 
            y = c(scelist[[2]],scelist[[3]],
                  scelist[[4]],scelist[[5]],
                  scelist[[6]],scelist[[7]],
                  scelist[[8]],scelist[[9]])) 
#这里可以看出，最终的细胞数和原始矩阵细胞数不一样，应该是过滤了
#为了保证一致，我们后续不再过滤细胞，这里直接挑选meta里面的细胞即可
dim(sce)
# [1] 26318  1268
dim(meta)
# [1] 1231    7

sce1 <- sce[,rownames(meta)]
dim(sce1)
#===============================================================================
#接下来就是标准流程了，至于其中的参数，差不多就行了，我们的目的主要是为了跑UMAP降维
sce1 <- NormalizeData(sce1)
sce1 <- FindVariableFeatures(sce1, nfeatures = 4000)
sce1 <- ScaleData(sce1,verbose = T)
sce1 <- RunPCA(sce1,npcs = 50, verbose = FALSE)
sce1 <- RunUMAP(sce1,  dims = 1:20)
sce1 <- FindNeighbors(sce1, dims = 1:20) 
sce1  <- FindClusters(object = sce1 , resolution = 1, verbose = FALSE) 
DimPlot(sce1, reduction = 'umap', label = T)+
  theme_bw()+
  theme(panel.background = element_blank(),
        panel.grid = element_blank())


#===============================================================================
#保证meta和seurat obj两者的barcode一致
sce1$cellid <- rownames(sce1@meta.data)
meta = meta[sce1$cellid,]#让meta的barcode排序和seurat一样

#替换坐标
umap1 <- meta$UMAP1
names(umap1) <- rownames(meta)
sce1@reductions[["umap"]]@cell.embeddings[,1] <- umap1

umap2 <- meta$UMAP2
names(umap2) <- rownames(meta)
sce1@reductions[["umap"]]@cell.embeddings[,2] <- umap2

#将meta添加到seurat
sce1@meta.data <- cbind(sce1@meta.data, meta)
#设定原文作者命名好的celltype cluster为active ident
Idents(sce1)='cluster'

DimPlot(sce1, reduction = 'umap', label = F, repel = T)+
  theme_bw()+
  theme(panel.background = element_blank(),
        panel.grid = element_blank())

#这样你的seurat对象就和原文一模一样了，有了分组什么的数据。就可以进行其他分析了




