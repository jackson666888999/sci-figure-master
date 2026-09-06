library(tidyverse)
library(readxl)
library(sf)
library(ggspatial)
# install.packages("ggsankey")
library(ggsankey)
library(patchwork)

df <- read_excel("41467_2023_42142_MOESM8_ESM.xlsx") %>% 
  select(1,2,3,4,5,6,7)

p1 <- df %>% select(4,5,6) %>% 
  mutate(Global="Global") %>% 
  make_long(.,Global,Continent,LandCoverType,Habitat) %>%
  ggplot(.,aes(x = x, next_x = next_x,node = node,
               next_node = next_node,
               label = node)) +
  geom_sankey(flow.alpha = .6,node.fill="#87CEEB",
              flow.fill="grey80",width=0.2) +
  geom_sankey_text(size = 3,color="black") +
  scale_fill_manual(values="grey80")+
  theme_sankey(base_size =15) +
  labs(x = NULL) +
  scale_x_discrete(position = "top")+
  theme(legend.position = "none",
        axis.text=element_text(color="black"))

p2 <- map_data("world") %>% ggplot()+
  geom_polygon(aes(x=long,y=lat,group=group),fill="grey")+
  geom_point(data=df,aes(longitude,latitude,fill=Continent,color=Continent),
             show.legend=F,size=1)+
  annotation_north_arrow(location="bl",pad_x=unit(0.03,"in"),pad_y=unit(3.5,"in"),
                         style=north_arrow_nautical(fill=c("grey40","white"),
                                                    line_col="grey20"))+
  annotate("rect", xmin =-128,xmax =-173, ymin=15,ymax=43, alpha = 0.2,fill = "blue")+
  annotate("text",x=-150,y=30,hjust=0.5,size=3,color="black",
           label="North America\n5734 samples\n11 cover types\n10 habitats")+
  theme(plot.background = element_blank(),
        panel.background = element_blank(),
        axis.text=element_blank(),
        axis.ticks = element_blank(),
        axis.title = element_blank())

p1/p2+plot_layout(height = c(1.5,2))

sessionInfo()
