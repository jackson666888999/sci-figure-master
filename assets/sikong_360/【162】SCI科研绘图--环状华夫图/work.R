library(tidyverse)
library(ggtext)

df <- read_tsv("data.xls") %>% mutate(count =as.factor(EDA_count))

labels <- tibble(x = 0,y = 1:5,
  text = c("A", "B","C","D","E"))

ggplot() +
  geom_segment(data =df, aes(x = x + .5, xend = x + (.5+.9), y = plot_seg, yend = plot_seg, color = count),
               size = 3)+
  geom_segment(aes(x = 0 + .5, xend = 2 + (.5+.9), y = 1 - .4, yend = 1 - .4),
               size = 0.5, color = "black",
               arrow = arrow(length = unit(0.005, "npc"))) +
  geom_text(data = labels, aes(x = x, y = y, label = text),
            colour="black",family="Times",fontface = "bold") +
  annotate(geom = "richtext",x = 0,y = -6,label = "**count**",
    color = "black", family = "Times",
    fill = NA, label.color = NA, size = 5) +
  scale_color_brewer(palette="Paired")+
  ylim(-8, 6) +
  xlim(0, 20) +
  coord_polar() +
  guides(color = guide_legend(keywidth =2, keyheight = 1,title.position = "top",
                              title.hjust = .5)) +
  theme(
    panel.grid = element_blank(),
    axis.ticks = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank(),
    legend.position = c(0.5,0.5),
    legend.key = element_blank(),
    legend.key.height = unit(5,"mm"),
    legend.key.width = unit(5, "mm"),
    legend.text = element_text(family = "Times", hjust = 0.5, size = 10, colour = "black", face = "bold"),
    legend.title = element_blank(),
    legend.background =element_blank(),
    panel.background = element_rect(fill ="white", colour = "white"),
    plot.background = element_rect(fill = "white", colour = "white", size = 3))




