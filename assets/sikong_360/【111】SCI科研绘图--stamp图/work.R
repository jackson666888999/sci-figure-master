library(tidyverse)
library(magrittr)
library(GGally)
library(ggprism)
library(patchwork)
library(cowplot)
library(ComplexHeatmap)


df <- read_tsv("meta.txt") %>% column_to_rownames(var="ID") %>% 
  t() %>%  as.data.frame() %>% rownames_to_column(var="sample") %>% 
  left_join(.,read_tsv("group_1.txt",col_names = F) %>% set_colnames(c("sample","group")),by="sample") %>% 
  pivot_longer(-c(sample,group)) %>% 
  mutate(group=as.factor(group))

p1 <- df %>% group_by(name,group) %>% 
  summarise(mean = mean(value),sd = sd(value)) %>% 
  ggplot(aes(name,mean,fill=group))+
  geom_errorbar(aes(ymax=mean+sd,ymin=mean-sd),position=position_dodge(width=0.8),width=0.2,size=0.5,color="black")+
  geom_bar(stat="identity",position=position_dodge(width=0.8),width = 0.8)+
  geom_stripped_cols()+
  scale_fill_manual(values=c("#E69F00","#56B4E9"))+
  scale_color_manual(values=c("#E69F00","#56B4E9"))+
  theme_prism()+
  scale_y_continuous(expand=c(0,0),limits = c(0,0.4),guide="prism_offset_minor")+
  labs(y="Proportions(%)",x=NULL)+
  theme(axis.ticks.y=element_blank(),
        axis.line.y = element_blank(),
        axis.line.x=element_line(size=0.5),
        axis.ticks.x = element_line(size=0.5),
        panel.grid.major.y =element_blank(),
        panel.grid.major.x = element_blank(),
        axis.text = element_text(size = 10, color = "black"),
        axis.text.y = element_text(margin = margin(r=0)),
        axis.text.x = element_text(size = 10,color = "black",margin=margin(b=6)),
        axis.title.x =  element_text(size=11,color = "black",hjust = 0.5),
        legend.position = "non")+
  coord_flip()


df2 <- df %>% group_by(name) %>% 
  rstatix::wilcox_test(value ~group,detailed = TRUE) %>% arrange(name)
#  mutate(p=p.adjust(p,"bonferroni")) 
#  filter(p < 0.05)

df3 <- df2 %>% select(name,estimate,conf.low,conf.high,p) %>% 
  mutate(group=ifelse(df2$estimate >0,levels(df$group)[1],
                      levels(df$group)[2])) %>% 
  mutate(p_signif=symnum(p,corr = FALSE, na = FALSE,  
                         cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1), 
                         symbols = c("***", "**", "*", " ", ""))) %>% 
  unite(.,col="p_value",p_signif,p,sep=" ",remove = T,na.rm = F)

p2 <- df3 %>% 
  ggplot(aes(name,estimate,fill = group))+
  geom_errorbar(aes(ymin = conf.low, ymax = conf.high),
                position = position_dodge(0.62), width = 0.2,size = 0.5) +
  geom_point(aes(color=group),shape = 21,size=3) +
  geom_hline(aes(yintercept = 0),linetype='dashed',color = 'black')+
  geom_stripped_cols()+
  labs(y="Difference between proportions(%)",x=NULL,title="95% confidence intervals")+
  theme_prism()+
  scale_y_continuous(expand=c(0,0),guide="prism_offset_minor") + 
  scale_fill_manual(values=c("#E69F00","#56B4E9"))+
  scale_color_manual(values=c("#E69F00","#56B4E9"))+
  theme(axis.ticks.y=element_blank(),
        axis.line.y = element_blank(),
        axis.line.x=element_line(size=0.5),
        axis.ticks.x = element_line(size=0.5),
        panel.grid.major.y =element_blank(),
        panel.grid.major.x = element_blank(),
        panel.background = element_blank(),
        axis.text.y=element_blank(),
        plot.margin = unit(c(0,0.5,0,0),"cm"),
        axis.text.x = element_text(size = 10,color = "black",margin=margin(b=6)),
        axis.title.x =  element_text(size=10,color = "black",hjust = 0.5),
        legend.position = "non",
        plot.title = element_text(size = 11,colour = "black",hjust = 0.5)) +
  coord_flip()


p3 <- df3 %>% mutate(group2="a") %>% 
  ggplot(aes(group2,p_value))+
  geom_text(aes(group2,p_value,label=p_value),size=3.5,color="black") +
  labs(y="P_value")+
  scale_y_discrete(position = "right")+
  theme_prism()+
  theme(axis.ticks=element_blank(),
        axis.line = element_blank(),
        panel.grid.major.y =element_blank(),
        panel.grid.major.x = element_blank(),
        panel.background = element_blank(),
        axis.text=element_blank(),
        plot.margin = unit(c(0,0.2,0,0),"cm"),
        axis.title.y =  element_text(size=11,color = "black",hjust = 0.5),
        axis.title.x=element_blank(),
        legend.position = "non") 

title <- ggdraw() +
  draw_label("Wilcoxon rank-sun test bar plot on Geneus level",colour="black",hjust = .5,vjust = .5,size =16) 


title/(p1+p2+p3+plot_layout(ncol = 3,width = c(1,2.5,0.25)))+
  plot_layout(ncol = 1,heights = c(0.5,5))

lgd = Legend(labels = c("AML","Con"),
             legend_gp = gpar(fill=c("#E69F00","#56B4E9")),
             labels_gp = gpar(col = "black", fontsize = 11),
             grid_width = unit(7,"mm"),grid_height=unit(3,"mm"))

draw(lgd,x = unit(0.96,"npc"),y = unit(0.96,"npc"),just = c("right","top"))

ggsave(file="barplot.pdf",unit="in",width =7.8,height = 5.9,dpi=300)





  