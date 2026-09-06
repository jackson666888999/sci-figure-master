library(tidyverse)
library(magrittr)
library(ggtree)
library(psych)
library(reshape)
library(ggtreeExtra)
library(ggnewscale)

asv <- read_csv('ASV_ba_rep.csv') %>% select(1:3000) %>% 
  column_to_rownames(var="...1") %>% t() %>% as.data.frame() %>% 
  rownames_to_column(var="asv")

tax <- read_csv("ASVname_ba.csv") %>% dplyr::rename(asv="...1") 

genus <- left_join(asv,tax,by="asv")  %>% select(Genus,where(is.numeric)) %>% 
  drop_na() %>% 
  group_by(Genus) %>%
  summarise(across(where(is.numeric), ~ sum(.x, na.rm=TRUE)))

env <- read_csv("env_rep.txt") %>% dplyr::rename(sampleID="...1") %>% 
  select(1:10)

df <- genus %>% column_to_rownames(var="Genus")

hc <- hclust(dist(df))

tree_hc <- ggtree(hc,layout = 'circular', branch.length='none')

spearman <- corr.test(env %>% column_to_rownames(var="sampleID"),
                      genus %>% 
                        column_to_rownames(var="Genus") %>% t() %>% as.data.frame(),
                      method = 'spearman', adjust = 'none')


envdata <- melt(spearman$r) %>% mutate(pvalue=melt(spearman$p.adj)[,3],
                            p_signif=symnum(pvalue, corr = FALSE, na = FALSE,  
                                            cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1), 
                                            symbols = c("***", "**", "*", "", " "))) %>% 
  filter(pvalue < 0.05) %>% 
  set_colnames(c("env","spe","r","p","p_signif"))  

# 上面部分在很多文档中都做过介绍，在这里不在过多解释

# new_scale_fill()，new_scale_color() 如果对树添加了颜色后则对后续图形添加颜色需要用到该函数


# 这里重点解释geom_fruit图层，pwidth 函数表示热图与聚类树之间的大小比例，
# text="x“表示将热图文本添加到X

tree_hc +
  layout_fan(angle = 60)+theme_void()+
  new_scale_fill()+
  new_scale_color()+
  geom_fruit(data=envdata,geom=geom_tile,
             mapping=aes(y=spe, x=env,fill=r),
             offset = 0.02,size = 0.02,pwidth=0.4,position_identityx(),
             axis.params = list(axis = "x",hjust=0,vjust=0.5,text.angle=-90,
                                text.size=2,color="black",text ="x"))+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  theme(legend.position = c(0.7,0.4),
        legend.title = element_blank())+
  guides(fill=guide_colorbar(direction = "horizontal",
         barwidth=unit(5.5,"cm"),
         barheight=unit(.5,"cm")))




