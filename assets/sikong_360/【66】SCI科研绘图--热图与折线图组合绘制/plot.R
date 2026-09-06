library(tidyverse)
library(cowplot)

df <- read_tsv("group.xls")

heatmap <- df %>% pivot_longer(-cluster) %>% 
  separate(`name`,into="name",sep="-") %>% 
  ggplot(aes(name,cluster,fill=value))+
  geom_tile()+
  scale_y_discrete(position = "right")+
  scale_x_discrete(limits=c("Epipelagic","Mesopelagic","Deep"))+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  theme(panel.background = element_blank(),
        plot.background = element_blank(),
        legend.background = element_blank(),
        plot.margin = margin(20,200,20,20),
        axis.title = element_blank(),
        axis.ticks=element_blank(),
        axis.text.x = element_text(angle = 45,color="black",vjust=1,hjust=1),
        legend.position = c(4,0.8),
        legend.title = element_blank())

line <- read_tsv("type.xls") %>% 
  ggplot(aes(x=type,y=len,group=cluster,color=group))+geom_line()+
  geom_point(size=2)+
  geom_text(aes(label=text),nudge_x=0.08)+
  scale_x_discrete(limits=c("tVCs","Hodts"))+
  scale_color_brewer(palette = "Paired")+
  theme(plot.margin = margin(2,2,2,0),
        plot.background = element_blank(),
        panel.background = element_blank(),
        legend.position = "non",
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.y=element_blank(),
        axis.text.x=element_text(color="black",face="bold"),
        axis.title= element_blank(),
        axis.ticks = element_blank())

plot <- heatmap %>% ggdraw()+
  draw_plot(line,scale=0.88,x=0.07,y=0.03)

ggsave(plot,file="heatmap.pdf",width=4.27,height=5.76,dpi=300)
