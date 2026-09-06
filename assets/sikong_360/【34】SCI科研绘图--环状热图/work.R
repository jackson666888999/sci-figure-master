package.list=c("tidyverse","ggtreeExtra","ggtree","treeio","ggnewscale","patchwork","ComplexHeatmap")

for (package in package.list) {
  if (!require(package,character.only=T, quietly=T)) {
    install.packages(package)
    library(package, character.only=T)
  }
}

df <- read_tsv("data.xls") %>% pivot_longer(-gene) %>% 
  mutate(group=case_when(value == 0 ~ "not regulated",
                         name=="CNA" & value== 1 ~ "CNA (direct)",
                         name=="mir" & value== 1 ~ "miRNA (inverse)",
                         name=="methylationpromoter" & value==1 ~ "methylation (direct)",
                         name=="methylationgenebody" & value==1 ~ "methylation (direct)",
                         name=="methylationanywhere" & value==1 ~ "methylation (direct)",
                         name=="methylationpromoter" | name=="methylationgenebody" | name=="methylationanywhere" | 
                         value == -1 ~ "methylation (inverse)"))

df$group <- factor(df$group,levels = c("CNA (direct)","miRNA (inverse)","methylation (inverse)",
                                       "methylation (direct)","not regulated"))

df$name <- factor(df$name,levels = rev(c("methylationgenebody","methylationanywhere","methylationpromoter",
                                     "mir","CNA")))


g1 <- hclust(dist(read_tsv("data.xls") %>% column_to_rownames(var="gene"))) %>% ggtree(layout="fan", open.angle=0, size=0.3) %>% 
  rotate_tree(.,angle=0)+
  geom_tiplab(size=3,family="Times",color="black",offset=0.53)+
  new_scale_fill()+
  geom_fruit(data=df, geom=geom_tile,
             mapping=aes(y=gene,x=name,fill=group),
             color = "grey50",offset = 0.04,size = 0.02)+
  scale_fill_manual(values=c("#5686C3","#973CB6","#F5A300","#75C500","#D9D9D9"))+
  theme(legend.position="non")


p2 <- read_tsv("data2.xls") %>% pivot_longer(-gene) %>%
  mutate(group=case_when(value == 0 ~ "not regulated",
                         name=="CNA" & value== 1 ~ "CNA (direct)",
                         name=="mir" & value== 1 ~ "miRNA (inverse)",
                         name=="methprom" & value==1 ~ "methylation (direct)",
                         name=="methbody" & value==1 ~ "methylation (direct)",
                         name=="methanywhere" & value==1 ~ "methylation (direct)",
                         name=="methprom" | name=="methbody" | name=="methanywhere" | 
                           value == -1 ~ "methylation (inverse)"))

p2$group <- factor(p2$group,levels = c("CNA (direct)","miRNA (inverse)","methylation (inverse)",
                                       "methylation (direct)","not regulated"))

p2$name <- factor(p2$name,levels = rev(c("methbody","methanywhere","methprom","mir","CNA")))


g2 <- hclust(dist(read_tsv("data2.xls") %>% column_to_rownames(var="gene"))) %>% ggtree(layout="fan", open.angle=0, size=0.3) %>% 
  rotate_tree(.,angle=0)+
  geom_tiplab(size=3,family="Times",color="black",offset=0.6)+
  new_scale_fill()+
  geom_fruit(data=p2, geom=geom_tile,
             mapping=aes(y=gene,x=name,fill=group),
             color = "grey50",offset = 0.04,size = 0.02)+
  scale_fill_manual(values=c("#5686C3","#973CB6","#F5A300","#75C500","#D9D9D9"))+
  theme(legend.position="non")

g1+g2

lgd = Legend(labels =c("CNA (direct)","miRNA (inverse)","methylation (inverse)",
                       "methylation (direct)","not regulated"),
             legend_gp = gpar(fill=c("#5686C3","#973CB6","#F5A300","#75C500","#D9D9D9")),
             labels_gp = gpar(col = "black", fontsize = 10),
             grid_width = unit(7,"mm"),grid_height=unit(3,"mm"))

draw(lgd,x = unit(0.55,"npc"),y = unit(0.85,"npc"),just = c("right","top"))







