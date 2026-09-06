library(Seurat)
mouse_data <- readRDS("D:/KS科研分享与服务公众号/mouse_data.rds")
DimPlot(mouse_data, label = T)
PMN0 <- subset(mouse_data, celltype=='PMN(0)')
#差异基因，为了显示所有点，Fc和min都设置为0
DEGs_PMN0 <- FindMarkers(PMN0,
                         ident.1 = '10X_ntph_F',
                         ident.2 = '10X_ntph_M',
                         group.by = "orig.ident",
                         logfc.threshold = 0,
                         min.pct = 0)
#添加差异基因的列
DEGs_PMN0$difference <- DEGs_PMN0$pct.1 - DEGs_PMN0$pct.2
DEGs_PMN0_sig <- DEGs_PMN0[which(DEGs_PMN0$p_val_adj<0.05 & abs(DEGs_PMN0$avg_log2FC) >0.25),]
DEGs_PMN0_sig$label <- rownames(DEGs_PMN0_sig)

library(ggplot2)
library(ggrepel)
#作图
ggplot(DEGs_PMN0, aes(x=difference, y=avg_log2FC)) + 
  geom_point(size=2, color="grey60") + 
  geom_text_repel(data=DEGs_PMN0_sig, aes(label=label),
                  color="black",fontface="italic")+
  geom_point(data=DEGs_PMN0[which(DEGs_PMN0$p_val_adj<0.05 & DEGs_PMN0$avg_log2FC>0.1),],
             aes(x=difference, y=avg_log2FC),
             size=2, color="red")+
  geom_point(data=DEGs_PMN0[which(DEGs_PMN0$p_val_adj<0.05 & DEGs_PMN0$avg_log2FC< -0.1),],
             aes(x=difference, y=avg_log2FC),
             size=2, color="blue")+
  theme_classic()+
  theme(axis.text.x = element_text(colour = 'black',size = 12),
        axis.text.y = element_text(colour = 'black',size = 12),
        axis.title = element_text(colour = 'black',size = 15),
        axis.line = element_line(color = 'black', size = 1))+
  geom_hline(yintercept = 0,lty=2,lwd = 1)+
  geom_vline(xintercept = 0,lty=2,lwd = 1)+
  ylab("Log-fold Change")+
  xlab("Delta Percent")
  
  
  
