setwd("E:/生物信息学/复现Cell双向柱状图加注释")
A <- read.csv("AA.csv", header = T)
library(ggplot2)
library(tidyverse)

A<-gather(A,key=Sample,value=value,-case_id)#宽数据转化为长数据
A[is.na(A$value), "value"] <- 0  # 将NA值替换为0，或者你可以选择其他合适的处理方式
A[which(A$Sample == 'Myeloid'),'value'] <- 
  A[which(A$Sample == 'Myeloid'), 'value'] * -1   #将Myeloid组变为负值


p1 <- ggplot(A,aes(case_id,value,fill=Sample))+
  geom_col()+
  theme_bw()+
  theme(panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        panel.border = element_blank(),
        legend.title = element_blank(),
        axis.text = element_text(color="black",size=10),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.line.y = element_line(color = "black",, size=0.5))+#添加y坐标
  scale_y_continuous(breaks = seq(-10, 10, 10), 
                     labels = as.character(abs(seq(-10, 10, 10))), 
                     limits = c(-10, 10))+  #修改坐标轴，标签全部变为正值
  labs(x='', y='')+
  geom_hline(yintercept = 0,size=0.5)+
  scale_fill_manual(values = c("#D08E8E","#89B9D8"))



B <- read.csv("BB.csv", header = T)
B1 <- B[,c(1,6)]
B1 <- t(B1)
B1 <- as.data.frame(B1)
colnames(B1) <- B1[1,]
B1 <- B1[-1,]
library(ComplexHeatmap)


B2 <- B[,1:5]
rownames(B2) <- B2[, 1]
B2 <- B2[,-1]
top_anno=HeatmapAnnotation(df=B2,
                           border = T,
                           show_annotation_name = T,
                           col = list(histology_diagnosis=c('PDAC'='#006699',
                                              'Adenosquamous carcinoma'='red')))



# 检查B1的结构，确认数据类型
str(B1)

# 将所有可以转换为数值类型的列转换为数值类型
B1[] <- lapply(B1, function(x) as.numeric(as.character(x)))

# 检查是否有任何列包含NA值，并处理这些NA值
B1 <- na.omit(B1)  # 例如，移除包含NA的行

# 确保B1现在是纯数值矩阵
B1 <- as.matrix(B1)

# 创建热图
p2 <- Heatmap(B1,
              cluster_rows = FALSE,
              cluster_columns = FALSE,
              show_column_names = TRUE,
              show_row_names = TRUE,
              column_title = NULL,
              heatmap_legend_param = list(
                title = 'Disease\nassociation'),
              col = c("#1084A4", "#8D4873"),
              border = 'black',
              row_names_gp = gpar(fontsize = 12),
              column_names_gp = gpar(fontsize = 8),
              top_annotation = top_anno)


p3 <- draw(p2, heatmap_legend_side = "bottom", 
     annotation_legend_side = "bottom",merge_legend = TRUE) #legend排序








