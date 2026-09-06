library(tidyverse)
library(ggtext)
library(magrittr)
library(ggprism)
library(MetBrewer)

df <- read_csv("IHME-GBD_2019_DATA-34013a2e-1.csv") %>% select(-upper,-lower,-1,-2,-cause) %>% 
  filter(sex !="Both",metric=="Number",age !="All age") %>% 
  mutate(val=val/1000000)

p <- df %>% 
  ggplot(aes(y=age,x = ifelse(sex=="Female",-val,val),fill =rei)) + 
  geom_bar(stat = "identity")+
  scale_fill_manual(values=met.brewer("Hiroshige",9))+
  scale_x_continuous(guide = "prism_minor",expand = c(0,0),limits=c(-2,2),
                     breaks=seq(-2,2,1))+
  geom_vline(xintercept = 0,linetype = 2)+
  labs(x="DALYs (millions)",y=NULL)+
  theme(axis.text.y=element_text(color="black",size=8,margin=margin(r=1)),
        axis.text.x=element_text(color="black",size=9,margin=margin(t=8)),
        axis.title.x = element_text(size=11,margin=margin(t=8),color="black",face="bold"),
        plot.margin=unit(c(0.3,0.3,0.3,0.3),units=,"cm"), 
        panel.background = element_blank(),   # 移除灰色背景框
        prism.ticks.length.y = unit(2, "pt"),
        prism.ticks.length.x = unit(-5, "pt"),
        axis.line = element_line(color="black"),
        axis.ticks.length.x = unit(-.2, "cm"),
        legend.key = element_blank(),
        legend.background = element_blank(),
        legend.title = element_blank(),
        legend.text=element_text(size=8,color="black"),
        legend.spacing.x=unit(0.1,'cm'),
        legend.key.width=unit(0.4,"cm"),
        legend.key.height=unit(0.4,"cm"),
        legend.position = c(0.001,1.02), # 定义图例位置
        legend.justification = c(0,1)
  )+
  annotate(geom="text",y=16,x=0.5,label="Males",size=4,fontface="bold")+
  annotate(geom="text",y=16,x=-0.5,label="Females",size=4,fontface="bold")

p

ggsave(p,file="barplot.pdf",unit="in",width=5.79,height = 3.88,dpi=300)


