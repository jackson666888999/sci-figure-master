library(tidyverse)
library(ggthemes)
library(cowplot)
library(RColorBrewer)
library(patchwork)
library(ggsci)

accidents <- read_tsv("heatmap2.xls") %>% arrange(Year) 

accidents$Year <- as.numeric(accidents$Year)

p1 <- ggplot(accidents, aes(x=Month, y=Year,fill=Deaths)) +
  geom_tile(colour="white") +
  xlim(-20,44) + ylim(2000,2020) +  # 更改刻度范围，根据数据进行设置
  coord_polar(theta = "x", start=20)  + # z转换为极坐标
  scale_fill_gradientn(colours=rev(RColorBrewer::brewer.pal(5,"RdBu")))+
  theme(panel.background=element_rect(fill ="white"),
        axis.title=element_blank(),
        panel.grid=element_blank(),
        axis.text.x = element_blank(),
        axis.ticks=element_blank(),
        axis.text.y=element_blank(),
        legend.position = "non") +
  theme(axis.text=element_blank())

p2 <- accidents %>% 
  group_by(Year) %>% 
  slice_head(n=1) %>% 
  mutate(Year=as.character(Year)) %>% 
  ggplot(aes(Deaths,Year))+
  geom_col(aes(fill="A"),show.legend = F)+
  scale_x_continuous(expand = c(0,0))+
  scale_y_discrete(expand = c(0,0))+
  scale_fill_manual(values="#71D0F5FF")+
  labs(x=NULL,y=NULL)+
  theme_classic()+
  theme(axis.text.y=element_blank(),
        axis.text.x=element_text(color="black"),
        axis.ticks.y=element_blank(),
        axis.line = element_line(color="grey60"),
        panel.background = element_blank(),
        plot.background = element_blank())

p1 %>% ggdraw()+
  draw_plot(p2,scale=0.29,x=0.131,y=-0.25)


