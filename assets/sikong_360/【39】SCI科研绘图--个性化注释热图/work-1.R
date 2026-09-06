library(tidyverse)
library(readxl)
library(magrittr)
library(ggdendro)
library(ggtree)
library(patchwork)
library(grid)

df <- read_excel("F1.xlsx", sheet = "Fig 1c KEGG module") %>% 
  column_to_rownames(var="...1")

hrdata <- hclust(dist(df)) %>% dendro_data(.,type = "rectangle")
hcdata <- hclust(dist(t(df))) %>% dendro_data(.,type = "rectangle")

hc <- hclust(dist(t(df))) %>% ggtree() + layout_dendrogram()+
  theme_void()

df2 <- df %>% rownames_to_column(var="ID") %>% 
  pivot_longer(-1) %>% 
  set_colnames(c("ID","name","value"))

df2$ID <- factor(df2$ID,levels = hrdata$labels %>% select(label) %>% pull())
df2$name <- factor(df2$name,levels = hcdata$labels %>% select(label) %>% pull())

heatmap <- df2 %>% 
  ggplot(aes(name,ID,fill=value))+
  geom_tile()+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  theme(axis.title = element_blank(),
        axis.ticks = element_blank(),
        axis.text = element_blank(),
        legend.title = element_blank(),
        plot.margin = margin(0.5,0,0,0,unit="cm"))+
  guides(fill=guide_colorbar(direction = "vertical",reverse = F,barwidth = unit(.5, "cm"),
                             barheight = unit(10.2,"cm"))) 

(hc/heatmap)+plot_layout(ncol=1,height =c(0.35,1))+ 
  coord_cartesian(clip="off")+
  annotation_custom(grob = grid::textGrob(label = "Shenzhen",hjust=0,
                                          gp=gpar(col="black",cex=1.2)),
                    xmin=30,xmax=40,ymin=55,ymax=60)+
  annotation_custom(grob = grid::textGrob(label = "GunagZhou",hjust=0,
                                          gp=gpar(col="black",cex=1.2)),
                    xmin=70,xmax=75,ymin=55,ymax=60)+
  
  annotation_custom(grob=rectGrob(gp=gpar(col="#BDE7FF",fill="#BDE7FF")),
                    xmin=unit(0.3,"native"),xmax=unit(53,"native"),
                    ymin=unit(44,"native"),ymax=unit(46,"native"))+
  annotation_custom(grob=rectGrob(gp=gpar(col="#FFF2E7",fill="#FFF2E7")),
                    xmin=unit(53.5,"native"),xmax=unit(136,"native"),
                    ymin=unit(44,"native"),ymax=unit(46,"native"))+
  annotation_custom(grob = grid::textGrob(label = "COPD",hjust=0,
                                          gp=gpar(col="black",cex=1)),
                    xmin=20,xmax=30,ymin=44,ymax=46)+
  annotation_custom(grob = grid::textGrob(label = "Healthy",hjust=0,
                                          gp=gpar(col="black",cex=1)),
                    xmin=85,xmax=95,ymin=44,ymax=46)






  

  
  
  