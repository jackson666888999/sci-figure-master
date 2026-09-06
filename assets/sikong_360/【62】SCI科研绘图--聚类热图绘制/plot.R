library(tidyverse)
library(ggtree)
library(treeio)
library(ape)
library(magrittr)
library(ggtreeExtra)
library(readxl)
library(MetBrewer)

sessionInfo()

gene_exp <- read_excel("Source Data Figure 6.xlsx") %>% 
  column_to_rownames(var="Tissue") %>% scale() %>% 
  as.data.frame() %>% 
  rownames_to_column(var="Tissue") %>% 
  pivot_longer(-Tissue)

tree <- read_excel("Source Data Figure 6.xlsx") %>% 
  column_to_rownames(var="Tissue") %>% 
  t() %>% 
  dist() %>% 
  ape::bionj()


tree2 <- read_excel("Source Data Figure 6.xlsx") %>% 
  column_to_rownames(var="Tissue") %>% 
  dist() %>% 
  ape::bionj()

rc <- ggtree(tree2,branch.length = "none", layout = "circular",
       linetype = 1,size = 0.5, ladderize = T)

gene_exp$Tissue <- factor(gene_exp$Tissue,levels =get_taxa_name(rc))

ggtree(tree,branch.length = "none", layout = "circular",
       linetype = 1,size = 0.5, ladderize = T)+
  layout_fan(angle =90)+
  geom_fruit(data=gene_exp,geom=geom_tile,
             mapping=aes(y=name,x=Tissue,fill=value),pwidth=2,
             axis.params=list(axis="x",text.angle=-90,text.size=2.6,hjust=0))+
  scale_fill_gradientn(colors=rev(met.brewer("Hiroshige")))


