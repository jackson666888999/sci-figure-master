
setwd("D:/tq/生物信息学/热图标注特定基因")
A <- read.csv("热图标注特定基因.csv", header = T,row.names = 1)
library(ComplexHeatmap)

A <- as.matrix(A)
samples <- rep(c('Control', 'Treat'), c(3, 3)) #定义样本分组信息  
for (i in 1:nrow(A)) A[i, ] <- scale(log(unlist(A[i, ] + 1), 2))

Group = factor(rep(c("control","treat"),times = c(3,3)))
Group = factor(Group,levels = c("control","treat"))


B <- Heatmap(A,#表达矩阵
        col = colorRampPalette(c("navy","white","firebrick3"))(100),#颜色定义
        show_row_names = F,#不展示行名
        top_annotation = top_annotation,#顶部分组信息
        column_split = Group,#用group信息将热土分开，以group聚类
        column_title = NULL,#不显示列标题
        show_column_names = F,
        name = "")#不显示列名
       

genes <- c("S100A10",
           "S100A11",
           "S100A9",
           "S100A8",
           "ILF2",
           "RPS27",
           "HAX1",
           "SNRPE",
           "SLFN5",
           "CCL5",
           "SYNRG",
           "MLLT6",
           "RPL23",
           "NCOA4",
           "BUD31",
           "TNIP1",
           "KDM6B",
           "SMG1")
genes <- as.data.frame(genes)


B + rowAnnotation(link = anno_mark(at = which(rownames(A) %in% genes$genes), 
                                      labels = genes$genes, labels_gp = gpar(fontsize = 10)))


top_annotation = HeatmapAnnotation(cluster = anno_block(gp = gpar(fill = c("#009933", "#FF3333")),
                       labels = c("Control","Treat"),
                       labels_gp = gpar(col = "black", fontsize = 12)))




#热图分裂

library(ComplexHeatmap)
library(circlize)
col_fun = colorRamp2(c(-2, 0, 2), c("#2fa1dd", "white", "#f87669"))

top_annotation = HeatmapAnnotation(
  cluster = anno_block(gp = gpar(fill = c("#2fa1dd", "#f87669")),
                       labels = c("control","treat"),
                       labels_gp = gpar(col = "white", fontsize = 12)))

m = Heatmap(t(scale(t(exp[g,]))),name = " ",
            col = col_fun,
            top_annotation = top_annotation,
            column_split = Group,
            show_heatmap_legend = T,
            border = F,
            show_column_names = F,
            show_row_names = F,
            column_title = NULL)
m





