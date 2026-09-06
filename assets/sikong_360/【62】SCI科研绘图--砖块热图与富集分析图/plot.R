library(tidyverse)
library(readxl)
# devtools::install_github("doehm/ggbrick")
library(ggbrick)
library(scales)
library(MetBrewer)
library(patchwork)

sessionInfo()

df <- read_excel("Source Data Figure 3.xlsx",sheet = 3)

dff <- df %>% mutate(Cluster=str_replace_all(Cluster,c("Cluster" = "C")),
                     summit=summit/10000000)

dff$Cluster <- factor(dff$Cluster,levels=rev(c("C1","C2","C3","C4","C5",
                                           "C6","C7","C8","C9","C10","C11","C12")))

plot1 <- dff %>%
  ggplot(aes(Cluster,summit)) +   
  geom_brick(aes(Cluster,summit,fill =Type), colour = NA, size = 0.2)  +
  scale_y_continuous(labels = label_number(),position = "right",expand = c(0,0))+
  scale_x_discrete(expand = c(0,0))+
  labs(y="Number of OCRs",x=NULL,fill =NULL) +
  scale_fill_manual(values=c("#788FCE","#E6956F","#A6BA96"))+
  coord_flip()+
  theme_classic()+
  theme(axis.text.x = element_text(color="black", size=8, face="bold"),
        axis.text.y = element_text(color="black", size=8, face="bold"),
        plot.background = element_rect(fill ="white", colour ="white"),   # 设置图表背景为白色
        plot.margin = margin(b = 5, t = 5, r = 5, l = 5),   # 设置图表的边距
        legend.text = element_text(color="black",size=8, face="bold"),
        legend.background = element_blank(),
        legend.key.height = unit(0.5,"cm"),
        legend.key.width = unit(0.5,"cm"),
        legend.position = c(0.4,0.1))

p2 <- read_excel("Source Data Figure 3.xlsx",sheet = 4)

df <-  p2 %>% mutate("-log10(p.adjust)"=-log10(p.adjust),
                     cluster=str_replace_all(cluster,c("Cluster" = "C"))) %>% 
  select(2,9,10,12)

df$cluster <- factor(df$cluster,levels=(c("C1","C2","C3","C4",
                                               "C6","C7","C9","C10","C11")))

plot2 <- df %>% ggplot(.,aes(cluster,Description,size=Count,fill=`-log10(p.adjust)`))+
  geom_point(shape=21)+
  labs(x = NULL,y = NULL,color=NULL) +
  scale_fill_gradientn(colors=met.brewer("Cassatt1"))+
  theme_bw()+
  theme(axis.text.x=element_text(color="black"),
        axis.text.y=element_text(color="black"),
        panel.background = element_blank(),
        panel.border = element_rect(fill=NA,color="grey80",size=1, linetype="solid"))


plot1+plot2+plot_layout(width=c(1.5,1))

