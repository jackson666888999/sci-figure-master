setwd('F:/生物信息学/离散型热图')
A <- read.csv("gene_dis.csv", header = T)


#######################ggplot2##########################
library(tidyr)
dft <-gather(A, disease, value, 2:9)
dft

library(forcats)
dft$gene <- as.factor(dft$gene)
dft$gene <- fct_inorder(dft$gene)
library(ggplot2)
ggplot(data=dft,aes(x=disease,y=gene))+
  geom_tile(aes(fill=value),color="grey")+
  theme_minimal()+
  theme(panel.border = element_rect(fill=NA,color="black", size=1, linetype="solid"),
        panel.grid = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title = element_blank(),
        axis.text.x = element_text(angle=45,hjust=1, colour = 'black', size = 12),
        axis.text.y = element_text(colour = 'black', size = 12),
        plot.margin=unit(c(0.4,0.4,0.4,0.4),units=,"cm"))+
  scale_fill_manual(values = c('white','black'))+
  labs(fill="Disease\nassociation")



###################ComplexHeatmap##########################
library(ComplexHeatmap)
B <- read.csv("gene_dis.csv", header = T, row.names = 1)


Heatmap(B,
        cluster_rows = F,
        cluster_columns = F,
        show_column_names = T,
        show_row_names = T,
        row_names_side =  'left',
        column_title = NULL,
        heatmap_legend_param = list(
          title='Disease\nassociation'),
        col = c('white','black'),
        border = 'black',
        rect_gp = gpar(col = "grey", lwd = 1),
        row_names_gp = gpar(fontsize = 10),
        column_names_gp = gpar(fontsize = 10))

####
disease <- c("disease1","disease2","disease3","disease4","disease5","disease6","disease7","disease8")
group <- c("Male_spc","Male_spc","Male_spc","Female_spc","Female_spc","Female_spc","MF","MF")
Group <- data.frame(disease, group)#创建数据框

top_anno=HeatmapAnnotation(df=Group,
                           border = T,
                           show_annotation_name = F,
                           col = list(group=c('Male_spc'='#006699',
                                              'Female_spc'='#993333',
                                              'MF'='#33CCCC')))

Heatmap(B,
        cluster_rows = F,
        cluster_columns = F,
        show_column_names = F,
        show_row_names = T,
        row_names_side =  'left',
        column_title = NULL,
        heatmap_legend_param = list(
          title='Disease\nassociation'),
        col = c('white','black'),
        border = 'black',
        rect_gp = gpar(col = "grey", lwd = 1),
        row_names_gp = gpar(fontsize = 10),
        column_names_gp = gpar(fontsize = 10),
        top_annotation = top_anno)
