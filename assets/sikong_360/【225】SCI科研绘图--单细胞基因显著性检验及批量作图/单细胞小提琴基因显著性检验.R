library(Seurat)
library(ggplot2)
library(ggpubr)
library(dplyr)

VlnPlot(mouse_data, features = 'S100a8', group.by = 'orig.ident')+
  theme_classic() + 
  theme(axis.text.x = element_text(size = 10,color="black"),
        axis.text.y = element_text(size = 10,color="black"),
        axis.title.y= element_text(size=12,color="black"),
        axis.title.x = element_blank(),
        legend.position='none')


#===================================================函数
singlecell_gene_test <- function(SerautObj, 
                                 genes.use, 
                                 group.by=NULL, 
                                 assay = "RNA", 
                                 comp = NULL, 
                                 alpha_start = .05, 
                                 Bonferroni = T,
                                 only_postive =F) {
  p_val.out <- c()
  stat.out <- c()
  condition.out <- c()
  gene.out <- c()
  if (only_postive == F){
    for (gene in genes.use){
      group1_cellname = rownames(SerautObj@meta.data[SerautObj@meta.data[[group.by]] == comp[1],])
      group1_exp = SerautObj@assays[[assay]]@data[gene, group1_cellname] #提取group1的表达量
      
      group2_cellname = rownames(SerautObj@meta.data[SerautObj@meta.data[[group.by]] == comp[2],])
      group2_exp = SerautObj@assays[[assay]]@data[gene, group2_cellname]#提取group2的表达量
      
      #T检验
      t_out = t.test(group1_exp, group2_exp)
      #condition标记
      cond = paste(comp[1], comp[2], sep = "_")
      #t检验结果
      condition.out <- c(condition.out, cond)
      stat.out <- c(stat.out, t_out[["statistic"]])
      p_val.out <- c(p_val.out, t_out[["p.value"]])
      gene.out <- c(gene.out, gene)
    }
  }
  else{
    for (gene in genes.use){
      group1_cellname = rownames(SerautObj@meta.data[SerautObj@meta.data[[group.by]] == comp[1],])
      group1_exp = SerautObj@assays[[assay]]@data[gene, group1_cellname]
      group1_exp <- group1_exp[which(group1_exp>0)] 
      
      
      group2_cellname = rownames(SerautObj@meta.data[SerautObj@meta.data[[group.by]] == comp[2],])
      group2_exp = SerautObj@assays[[assay]]@data[gene, group2_cellname]
      group2_exp <- group2_exp[which(group2_exp>0)] 
      
      t_out = t.test(group1_exp, group2_exp)
      cond = paste(comp[1], comp[2], sep = "_")
      condition.out <- c(condition.out, cond)
      stat.out <- c(stat.out, t_out[["statistic"]])
      p_val.out <- c(p_val.out, t_out[["p.value"]])
      gene.out <- c(gene.out, gene)
    }
    
  }
  
  #BH矫正
  if (Bonferroni == T){
    new_alpha = alpha_start/(2*length(genes.use))
    cat(paste("\n", "P-value for significance: p <", new_alpha, "\n"))
    sig_out = p_val.out < new_alpha
    dfOUT<- data.frame(gene=gene.out, condition = condition.out, p_val = p_val.out, statistic = stat.out, significant = sig_out)
    
    dfOUT$sig = ifelse(dfOUT$p_val > 0.05, "ns",
                       ifelse(dfOUT$p_val > 0.01, '*',
                              ifelse(dfOUT$p_val > 0.001, "**", "****")))
    
  }
  
  else{
    dfOUT<- data.frame(gene=gene.out, condition = condition.out, p_val = p_val.out, statistic = stat.out)
    dfOUT$sig = ifelse(dfOUT$p_val > 0.05, "ns",
                       ifelse(dfOUT$p_val > 0.01, '*',
                              ifelse(dfOUT$p_val > 0.001, "**", "****")))
  }
  
  return(dfOUT)
}



#显著性检验，只能进行两组比较
A <- singlecell_gene_test(mouse_data, #seurat对象
                          genes.use = c('S100a8','Ltf','Ncf1','Ly6g','Anxa1','Il1b'),#需要检验的基因
                          group.by = 'orig.ident', #metadat中的分组列名
                          comp = c("10X_ntph_F", "10X_ntph_M"))#分组

A1 <- singlecell_gene_test(mouse_data,
                           genes.use = c('S100a8','Ltf','Ncf1','Ly6g','Anxa1','Il1b'),
                           group.by = 'orig.ident', 
                           comp = c("10X_ntph_F", "10X_ntph_M"),
                           only_postive = T)#这里选择T，代表我们只比较表达这个基因的细胞

#注释label
anno_pvalue <- format(A$p_val, scientific = T,digits = 3) 
anno_sig <- A$sig

plots_violins <- VlnPlot(mouse_data, 
                         cols = c("limegreen", "navy"),
                         pt.size = 0,
                         group.by = "orig.ident",
                         features = c('S100a8','Ltf','Ncf1','Ly6g','Anxa1','Il1b'), 
                         ncol = 3, 
                         log = FALSE,
                         combine = FALSE)

for(i in 1:length(plots_violins)) {
  data <- plots_violins[[i]]$data
  colnames(data)[1] <- 'gene'
  plots_violins[[i]] <- plots_violins[[i]] + 
    theme_classic() + 
    theme(axis.text.x = element_text(size = 10,color="black"),
          axis.text.y = element_text(size = 10,color="black"),
          axis.title.y= element_text(size=12,color="black"),
          axis.title.x = element_blank(),
          legend.position='none')+
    scale_y_continuous(expand = expansion(mult = c(0.05, 0.1)))+
    scale_x_discrete(labels = c("Female","Male"))+
    geom_signif(annotations = anno_sig[i],
                y_position = max(data$gene)+0.5,
                xmin = 1,
                xmax = 2,
                tip_length = 0)
}

CombinePlots(plots_violins)

