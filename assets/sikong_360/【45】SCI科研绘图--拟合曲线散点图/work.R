library(tidyverse)
library(magrittr)
library(ggsci)
library(ggpubr)
library(cowplot)
library(ggpmisc)


df <- read_tsv("data.txt") %>% 
  select(2:4,"Respiration of plant-derived OC \r\n(Rplant, g C-CO2 \r\nm-2 day-1)",
         "Native SOC decomposition rate \r\n(kSOC, µg C-CO2 \r\ng-1 SOC day-1)",last_col()) %>% 
  set_colnames(c("type","layer","plant","plant_derived","SOC","RPF")) %>% 
  unite(.,col="lintype",layer:type,sep="-",remove = F,na.rm = F)


p1 <- df %>% 
  ggplot(aes(plant_derived,SOC,shape=lintype,color=lintype,linetype=lintype))+
  geom_point()+
  geom_smooth(method = lm, formula = y ~ x,alpha=0.3,se=F)+
  scale_linetype_manual(values = c("dotted","dotted","dotted","solid","solid","solid"))+
  scale_color_manual(values=c("#FD7446FF","#008f39","#56B4E9","#FD7446FF","#008f39","#56B4E9"))+
  scale_shape_manual(values=c(0,2,1,16,17,15))+
  theme_test()+
  theme(legend.title = element_blank(),
        legend.key = element_blank(),
        legend.text = element_text(color="black"))

p2 <- df %>% ggplot(aes(plant_derived,SOC,shape=lintype,color=lintype,linetype=lintype,fill=type))+
  geom_point(size=2.5)+
  geom_smooth(method="lm",formula = y ~ x,alpha=0.3)+
  scale_linetype_manual(values = c("solid","solid","solid","dashed","dashed","dashed"))+
  scale_color_manual(values=c("#FD7446FF","#008f39","#56B4E9","#FD7446FF","#008f39","#56B4E9"))+
  scale_fill_manual(values=c("#FD7446FF","#008f39","#56B4E9"))+
  scale_shape_manual(values=c(0,2,1,16,17,15))+
  labs(x=NULL,y=NULL)+
  geom_hline(yintercept=0,linetype="dashed")+
  geom_vline(xintercept=c(0,10),linetype="dashed")+
  theme(plot.margin=unit(c(0.3,0.3,0.3,0.3),units=,"cm"),
        axis.line = element_line(color = "black",size=0.8),
        panel.grid.minor = element_blank(),
        panel.grid.major = element_line(size = 0.2,color = "#e5e5e5"),
        panel.background = element_blank(),
        axis.text.y = element_text(color="black",size=10,face="bold",angle=90,vjust=0.5,hjust = 0.5),
        axis.text.x = element_text(color="black",size=10,vjust=0.5,hjust = 0.5,face="bold",angle =0),
        axis.line.x.top  = element_line(color="black"), 
        axis.text.x.top = element_blank(),
        axis.ticks.y.right=element_blank(),
        axis.text.y.right = element_blank(),
        axis.ticks.x.top=element_blank(),
        panel.spacing.x = unit(0,"cm"),
        panel.border = element_blank(),
        legend.position = "none",
        panel.spacing = unit(0,"lines"))+guides(x.sec="axis",y.sec = "axis")

df$type <- factor(df$type,levels =rev(c("Cambisol","Vertisol","Andosol")))

p3 <- df %>% select(type,SOC,RPF) %>% 
  ggplot()+
  stat_summary(aes(SOC,type,group=type),
               fun.data = "mean_cl_normal",geom="errorbar",width=0.1,color="black")+
  stat_summary(aes(SOC,type,group=type,fill=type,color=type),pch=20,
               fun.y="mean",geom="point",size=5)+
  scale_fill_manual(values=c("#FD7446FF","#008f39","#56B4E9"))+
  scale_color_manual(values=c("#FD7446FF","#008f39","#56B4E9"))+
  geom_hline(yintercept=2.5,linetype="dashed")+
  labs(x=NULL,y=NULL)+
  theme(plot.margin=unit(c(0.1,0.1,0.1,0.1),units=,"cm"),
        axis.line = element_line(color = "black",size=0.8),
        panel.grid.minor = element_blank(),
        panel.grid.major = element_line(size = 0.2,color = "#e5e5e5"),
        panel.background = element_blank(),
        axis.text.y = element_text(color="black",size=8,face="bold"),
        axis.text.x = element_blank(),
        axis.ticks.x.bottom =element_blank(),
        axis.line.x.top  = element_line(color="black"), 
        axis.text.x.top = element_text(color="black",size=8,vjust=0.5,hjust = 0.5,face="bold",angle =0),
        axis.ticks.y.right=element_blank(),
        axis.text.y.right = element_blank(),
        panel.spacing.x = unit(0,"cm"),
        panel.border = element_blank(),
        legend.position = "none",
        panel.spacing = unit(0,"lines"))+guides(x.sec="axis",y.sec = "axis")
  
p2 %>% ggdraw() + draw_plot(p3,scale=0.3,x=-0.35,y=0.583,height = 0.6,width = 1.2)+
  draw_plot(ggpubr::get_legend(p1) %>% as_ggplot(),scale=0.3,x=0.36,y=0,height = 0.5,width = 1)

ggsave(file="plot.pdf",unit="in",width =6.78,height = 6.21,dpi=300)









