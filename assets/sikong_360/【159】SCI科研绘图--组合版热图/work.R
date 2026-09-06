library(tidyverse)
library(ggh4x)
library(patchwork)
library(ggsci)

theme_niwot <- function(){
  theme_test()+
    theme(
          axis.text.y=element_text(color="black",size =8.5),
          axis.ticks= element_blank(),
          strip.background = element_blank(),
          strip.text = element_blank(),
          panel.spacing.y = unit(0,"cm"),
          plot.background = element_blank(),
          panel.border = element_rect(fill=NA,color="white",size=1),
          plot.margin = margin(0,0.2,0,0.2,"cm")
    )
}

data <- read_tsv("data.xls")

df <- data %>% pivot_longer(-sample) %>% 
  left_join(.,read_tsv("group.xls"),by="name") %>% 
  arrange(sample) %>% 
  mutate(sample=as.character(sample))

df$sample <- factor(df$sample,levels = df$sample %>% unique())

p1 <- df %>%
  ggplot(.,aes(sample,name))+
  geom_tile(color="grey60",fill="white",size=0.2)+
  geom_text(aes(label=value),size=3,color="black",hjust=0.5,vjust=0.5)+
  labs(x = NULL,y = NULL,color=NULL,fill=NULL)+
  theme_niwot()

p2 <- df %>% filter(group=="A") %>% 
  ggplot(aes(sample,name,fill=value,color=value))+
  geom_tile(color="grey60",fill="white",size=0.2)+
  geom_point(aes(size=value),shape=22)+
  facet_grid2(group~.,scale="free_y",switch = "y")+
  labs(x = NULL,y = NULL,color=NULL,fill=NULL)+
  scale_color_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  theme_niwot()+
  theme(legend.position = "bottom")+
  scale_size(guide=NULL)+
  guides(color=guide_colorbar(direction="horizontal",reverse = F,
                              barwidth = unit(17, "cm"),
                              barheight = unit(.5,"cm"))) 

p3 <- df %>% filter(group=="B") %>% 
  ggplot(aes(sample,name,fill=value,color=value))+
  geom_tile(color="grey60",fill="white",size=0.2)+
  geom_text(aes(label=value),size=2.8,color="black",hjust=0.5,vjust=0.5)+
  facet_grid2(group~.,scale="free_y",switch = "y")+
  labs(x = NULL,y = NULL,color=NULL,fill=NULL)+
  scale_color_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  theme_niwot()+
  theme(axis.text.x=element_blank())+
  scale_size(guide=NULL)

p3/p2+plot_layout(heights=c(2,1.2))

p1
