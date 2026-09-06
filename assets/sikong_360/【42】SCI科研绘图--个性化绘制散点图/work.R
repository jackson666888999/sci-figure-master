library(tidyverse)
library(readxl)
library(ggtext)
library(ggsci)

df1 <- read_excel("41588_2022_1184_MOESM5_ESM.xlsx",sheet = 4)

df1$taxon <- factor(df1$taxon,levels=c("nicaraguensis","luxurians","diploperennis",
                                       "perennis","huehuetenangensis","mexicana",
                                       "parviglumis","TST","TEM"))

p_value1 <- tibble(
  x = c("nicaraguensis","nicaraguensis","parviglumis","parviglumis"),
  y= c(7.8,7.8,7.8,7.8))

p_value2 <- tibble(
  x = c("perennis","perennis","TEM","TEM"),
  y=c(7.8,8.2,8.2,0.8))

p_value3 <- tibble(
  x = c("TST","TST","TEM","TEM"),
  y=c(0.7,0.7,0.7,0.7))

df1 %>% mutate(SNP=SNP/100000) %>% 
  ggplot(aes(taxon,SNP))+
  geom_jitter(width = 0.1,color="grey")+
#  stat_boxplot(geom = "errorbar", aes(ymin = ..ymax..),width=0.1) +
#  stat_boxplot(geom = "errorbar", aes(ymax = ..ymin..),width=0.1)+
  stat_boxplot(outlier.shape = NA,width=0,aes(color=taxon,fill=taxon),
               show.legend = F) +
  stat_summary(aes(taxon,SNP,color=taxon,fill=taxon),pch=22,
               fun.y="mean",geom="point",size=4,
               show.legend = F)+
  geom_line(data = p_value1,aes(x = x, y = y,group=1))+
  geom_line(data = p_value2,aes(x = x, y = y,group=1))+
  geom_line(data = p_value3,aes(x = x, y = y,group=1))+
  labs(x=NULL,y="Number of taxon-specific SNPs (x10<sup>5</sup>)")+
  scale_y_continuous(limits = c(0,8.5),breaks = seq(0,8.5,2.5))+
  scale_fill_npg()+
  scale_color_npg()+
  theme_classic()+
  theme(axis.text.x=element_text(angle = 90,vjust = 0.5,hjust=1,size=10,
                                 color="black",face="bold"),
        axis.text.y=element_text(size=10,color="black"),
        axis.title.y= element_markdown(color="black",size=11,face="bold",
                                       margin = margin(r=10)))+
  annotate("text",x =7,y =8.3,label="**",size = 6,color = "#22292F")
  

