devtools::install_github("XiaoLuo-boy/ggheatmap")
library(ggheatmap)
setwd("F:/生物信息学/ggheatmap热图")
A <- read.csv("A1.csv",header = T,row.names = 1)
A <- log2(A)
#660033 #FFFFFF(white) #003366
#99CC99 #336699 #FF9999  44 36 11
col_ann <- data.frame(group= c(rep("CTRL",44),rep("LIVER",36), rep("BB",11)))
rownames(col_ann) <- colnames(A)

groupcol <- c("#99CC99","#336699","#FF9999")
names(groupcol) <- c("CTRL","LIVER","BB")
col <- list(group=groupcol)

text_columns <- sample(colnames(A),0)

p <- ggheatmap(A,color=colorRampPalette(c("#003366","#FFFFFF","#660033"))(60),
          cluster_rows = T,cluster_cols = F,scale = "none",
          annotation_cols = col_ann,
          annotation_color = col,
          legendName="Relative value",
          text_show_cols = text_columns)

ggheatmap_plotlist(p)

library(dplyr)
p1 <- p%>%ggheatmap_theme(1,theme =list(geom_vline(xintercept=c(11.5,55.5),size=.8)))
p2 <- p1%>%ggheatmap_theme(2,theme =list(theme(panel.border = element_rect(fill=NA,color="black", size=1, linetype="solid"))))
p3 <- p2%>%ggheatmap_theme(1,theme =list(theme(panel.border = element_rect(fill=NA,color="black", size=1, linetype="solid"))))                     
p4 <- p3%>%ggheatmap_theme(1,theme =list(geom_hline(yintercept=12.5,size=.8)))        
p4












                   
                           