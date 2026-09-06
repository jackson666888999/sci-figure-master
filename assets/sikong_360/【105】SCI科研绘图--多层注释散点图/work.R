library(tidyverse)
library(ggalt)
library(ggnewscale)

df <- read_csv("KY.csv") %>% filter(id=="SH1") %>% 
  mutate(Testdate=str_remove(Testdate,"2022.08.")) %>% 
  select(-date_onset) %>% 
  pivot_longer(-c("id","Ky","Testdate"))

df2 <- df %>% select(Ky,Testdate,value) %>% 
  drop_na() %>% 
  mutate(value=max(value)+2,Ky=as.character(Ky))

df %>% ggplot()+
  geom_xspline(aes(Testdate,value,fill=name,group=name,color=name),
               spline_shape = -0.5,size=1)+
  geom_point(aes(Testdate,value,fill=name,group=name,color=name),
             size=3,pch=21)+
  scale_fill_manual(values=c("#53ae32", "#2e76b5"))+
  scale_color_manual(values=c("#53ae32", "#2e76b5"))+
  new_scale_fill()+
  geom_point(data=df2,aes(Testdate,value,fill=Ky),pch=22,size=4,color="black")+
  scale_fill_manual(values=c("#f2d355", "#d23c28"))+
  labs(x=NULL,y=NULL)+
  theme(axis.text=element_text(color="black",face="bold",size=10),
        axis.line = element_line(color="black"),
        axis.line.x.top  = element_line(color="black"),
        axis.text.x.top = element_blank(),
        axis.ticks.y.right=element_blank(),
        axis.text.y.right = element_blank(),
        axis.ticks.x.top=element_blank(),
        legend.title = element_blank(),
        legend.text=element_text(size=10,color="black",face="bold"),
        legend.box = "horizontal",
        legend.position = "bottom",
        legend.key.width=unit(0.5,"cm"),
        legend.key.height=unit(0.5,"cm"),
        legend.spacing.x = unit(0.1,"cm"))+
  guides(x.sec="axis",y.sec = "axis")



