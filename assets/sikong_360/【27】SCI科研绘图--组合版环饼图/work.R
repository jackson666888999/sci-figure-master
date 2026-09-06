library(tidyverse)
library(readxl)
library(camcorder)
library(ggtext)
library(ggsci)
library(cowplot)

df <- read_excel("41591_2022_2116_MOESM5_ESM.xlsx") %>% 
  select(1,2,3,group_2) %>% 
  rownames_to_column(var="ID") %>% 
  mutate_at(vars(c(S1)),~str_split(.," ",simplify=T)[,1]) %>%
  mutate(group_3 = rep(LETTERS[1:4], times=c(5,12,10,11))) %>% 
  mutate(S1=as.numeric(S1),ID=as.numeric(ID)) %>% 
  group_by(group_2) %>% 
  mutate(per=S1/sum(S1)*10) %>% 
  arrange(desc(per)) %>% 
  ungroup()

p <- df %>% 
  ggplot(aes(x="",y=per,fill=group_3))+
  geom_col()+ coord_polar("y")+
  scale_fill_npg()+
  theme_void()+
  theme(legend.position = "non")

p2 <- ggplot(df) +
  annotate("segment", x = -Inf, xend = Inf, y = seq(0,10,1), yend = seq(0,10,1),
           size = rep(c(0.25, 0.1),length.out =11), alpha = 0.5)+
  annotate("label", x = 0, y = seq(0,10,1), label = seq(0,10,1),color="black",
           size = 3, fill = "#FEF8FA",label.padding = unit(0.1,"lines"),
           label.size = 0)+
  geom_col(aes(x = ID, y =per, fill = group_2),position = "dodge", width=0.6)+
  scale_y_continuous(limits = c(-4,10)) +
  scale_x_continuous(limits = c(-0.5,38.5), breaks = 1:38.5) +
  scale_fill_manual(values=c("#709AE1FF","#8A9197FF","#D2AF81FF","#FD7446FF",
                    "#D5E4A2FF","#197EC0FF","#F05C3BFF","#46732EFF",
                    "#71D0F5FF","#075149FF","#C80813FF","#91331FFF"))+
  coord_polar()+
  theme_minimal() +
  theme(
    legend.position = "none",
    plot.background =element_blank(),
    panel.background = element_blank(),
    panel.grid = element_blank(),
    axis.text.y = element_blank(),
    axis.title = element_blank(),
    axis.text.x = element_blank())

ggdraw(p2)+
  draw_plot(p,scale=0.23,x=0,y=0)

