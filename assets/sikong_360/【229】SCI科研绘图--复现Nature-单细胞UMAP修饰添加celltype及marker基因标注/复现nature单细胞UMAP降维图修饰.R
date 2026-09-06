setwd('G:/生信课程/R代码/2024年11月新增/复现Nature-单细胞UMAP修饰添加celltype及marker基因标注')
library(Seurat)
library(ggplot2)
library(ggrastr)
library(tidydr)
library(dplyr)
library(ggrepel)

load("adj_scRNA.RData")
adj_scRNA <- subset(adj_scRNA, celltype=="Other", invert=T)
DimPlot(adj_scRNA, label = T)


#提取UMAP坐标信息
df <- adj_scRNA@reductions$umap@cell.embeddings%>% 
  as.data.frame() %>%
  cbind(cell_type = adj_scRNA@meta.data$celltype)
# colnames(df)
# [1] "UMAP_1"    "UMAP_2"    "cell_type"


#取每种细胞在坐标轴的中心位置，用于添加扇形
label <- df %>%group_by(cell_type) %>%
  summarise(UMAP_1 = median(UMAP_1),
            UMAP_2 = median(UMAP_2))%>%
  as.data.frame()
rownames(label) <- label$cell_type

label$number <- seq(1:9)





cols= c('#7F3C8D' ,'#11A579', '#3969AC',
        '#E73F74', '#80BA5A', '#E68310',
        '#008695', '#CF1C90', '#f97b72')

#ggplot作图
p = ggplot()+
  geom_point_rast(data=df, aes(x= UMAP_1 , y = UMAP_2 ,color = cell_type),size = 1,shape=16) +
  scale_color_manual(values = alpha(cols,0.3))+ #设置下透明度
  theme_classic()+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.ticks = element_blank(),
        axis.line = element_blank(),
        axis.title = element_blank(),
        axis.text = element_blank(),
        legend.position = 'none')+
  geom_point(data = label, aes(x= UMAP_1 , y = UMAP_2), size=6, color='white', alpha=0.9)+
  geom_point(data = label, aes(x= UMAP_1 , y = UMAP_2), size=6, color='black', shape=21)+
  geom_text(data = label,
            mapping = aes(x= UMAP_1 , y = UMAP_2, label = number),
            color='black')


#============================================================================
#label celltype

marker_gene <- FindAllMarkers(adj_scRNA, only.pos = T,
                              logfc.threshold = 0.8, min.pct = 0.8)

#每种celltype挑选5个展示
marker_genes <- marker_gene %>% 
  group_by(cluster) %>% 
  top_n(n = 5, wt = avg_log2FC) 

write.csv(marker_genes, file = 'marker_genes.csv')

#添加需要标记的基因
label$gene <- ''
for (i in 1:9) {
  
  dat <- subset(marker_genes, cluster==as.character(label$cell_type)[i])
  dat <- dat$gene
  datstr <- paste(dat, collapse = "\n")
  label$gene[i] <- datstr
  
}


label$labels <- paste(label$cell_type,":\n", label$gene)


#按照UMAP坐标四个象限，添加文字标注，这样会让标注清晰可见
#这里比较麻烦的就是位置需要自己慢慢调整
  
p + geom_label_repel(  
  data=label[which(label$UMAP_1>0 &label$UMAP_2>0),],   
  aes(x= UMAP_1, y = UMAP_2,label=labels),   
  size=3,  
  nudge_x = 4,  
  box.padding = 0.5,  
  nudge_y = 8,  
  segment.curvature = -0.1,  
  segment.ncp = 3,  
  segment.angle = 20,  
  direction = "y", hjust = "left")+  
  geom_label_repel(    
    data=label[which(label$UMAP_1>0 &label$UMAP_2<0),],     
    aes(x= UMAP_1, y = UMAP_2,label=labels),     
    size=3,    
    nudge_x = 4,    
    box.padding = 0.5,    
    nudge_y = -8,    
    segment.curvature = -0.1,    
    segment.ncp = 3,    
    segment.angle = 20,    
    direction = "y", hjust = "left")+  
  geom_label_repel(    
    data=label[which(label$UMAP_1<0 &label$UMAP_2>3),],     
    aes(x= UMAP_1, y = UMAP_2,label=labels),     
    size=3,    
    nudge_x = -6,    
    box.padding = 0.5,    
    nudge_y = 15,    
    segment.curvature = -0.1,    
    segment.ncp = 3,    
    segment.angle = 20,    
    direction = "y", hjust = "left")+  
  geom_label_repel(    
    data=label[which(label$UMAP_1<0 &label$UMAP_2<3),],     
    aes(x= UMAP_1, y = UMAP_2,label=labels),     
    size=3,    
    nudge_x = -3,    
    box.padding = 0.5,    
    nudge_y = -12,    
    segment.curvature = -0.1,    
    segment.ncp = 3,    
    segment.angle = 20,    
    direction = "y", hjust = "left")




  

  
  
  
  

  







