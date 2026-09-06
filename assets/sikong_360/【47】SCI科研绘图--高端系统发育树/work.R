library(tidyverse)
library(ggtree)
library(ggtreeExtra)
library(ggnewscale)
library(ggsci)
library(cowplot)

df <- read_csv("data.csv") %>% dplyr::rename(tax=`...1`) %>% 
  column_to_rownames(var="tax")

#  由于我们需要给分类线条添加颜色，通过上图可以看到分为6类因此在此使用cutree(hc,6)

hc <- hclust(dist(df))
clus <- cutree(hc,6)
g <- split(names(clus),clus)
p <- ggtree(hc,branch.length = "none",layout = "circular",linetype=1,size=0.5,ladderize = T)+
  layout_fan(angle = 90)+theme_void()

clades <- sapply(g, function(n) MRCA(p, n))

# 构建注释信息表

deseq <- read_tsv("DEseq.xls") %>% mutate(name=as.factor(name))

data2 <- df %>% rownames_to_column(var="ID") %>%
  select(ID,starts_with("n")) %>% 
  pivot_longer(-ID)

data3 <- data2 %>% filter(name %in% c("nap","nif"))

# 绘制进化树
tree <- groupClade(p,clades, group_name='subtree') + aes(color=subtree)+
  scale_color_brewer(palette='Paired', breaks=1:6)+  #绘制主图
  new_scale_fill()+
  # 绘制第一圈注释
  geom_fruit(data=deseq,geom=geom_bar,
             mapping=aes(y=sample, x=name,fill=name),
             orientation="y",pwidth=0,stat="identity")+
  scale_fill_manual(values=c("#3C5488FF","#00A087FF"))+
  new_scale_fill()+
  # 绘制第二圈注释
  geom_fruit(data=data2, geom=geom_tile,
             mapping=aes(y=ID, x=name,alpha=value,fill=name),
             color = "grey50",offset = 0.03,size = 0.02)+
  scale_fill_manual(values=c("#FFC125","#87CEFA","#7B68EE","#808080","#800080"))+
  new_scale_fill()+
  # 最外圈注释
  geom_fruit(data=data3,geom=geom_bar,
             mapping=aes(y=ID, x=value,fill=name),
             offset = 0.05,
             orientation="y", 
             stat="identity")+
  scale_fill_manual(values=c("#D15FEE", "#9ACD32"))+
  theme(legend.position = "non")
  

# 绘制条形图
bar <- data2 %>% left_join(.,deseq,by=c("ID"="sample")) %>% 
  ggplot(aes(name.x,value,fill=name.y))+
  geom_col(width = 0.5)+
  scale_fill_manual(values=c("#3C5488FF","#00A087FF"))+
  labs(x = NULL,y = NULL,fill = NULL) +
  scale_y_continuous(expand=c(0,0)) +
  theme_classic()+
  theme(
    panel.background = element_blank(),
    axis.line = element_line(color = "black"),
    axis.text = element_text(size=10,color = "black"),
    axis.text.x = element_text(margin=margin(t =5)),
    axis.text.y = element_text(size=10),
    legend.position = "non")

# 拼图
tree %>% ggdraw()+
  draw_plot(bar,scale=0.32,x=0.17,y=-0.23)

  







