library(ggpubr)
library(ggplot2)
library(dplyr)
setwd("D:/生物信息学/棒棒糖图")
A <- read.csv("df.csv", header = T)
library(forcats)
A$pathway <- as.factor(A$pathway)
A$pathway <- fct_inorder(A$pathway)

p <- ggplot(A,aes(x=pathway,y=corr)) +
  geom_point(data=A,aes(size=abs(corr),color=Pval)) +
  scale_size(range = c(0,8)) +
  scale_color_viridis_c() +
  geom_segment(aes(x=pathway,xend=pathway,y=0,yend=corr),
               linewidth=1, linetype="solid") +
  labs(x="", y='Correlation(r)', title = 'Gene') +
  coord_flip() +
  theme_bw() +
  theme(axis.text.x=element_text(hjust = 1,vjust=0.5),
        panel.border = element_blank(),
        axis.text = element_text(size = 10, color = "black"),
        axis.ticks = element_blank(),
        plot.title = element_text(hjust=0.5))
  


p1 <- p + geom_point(data=A, aes(size=abs(corr), color=Pval))
  

p2 <- p1+guides(color='none')+
  guides(size=guide_legend(title="Correlation"))
p2

p2 + annotate(geom = "text", x = unique(A$pathway),
             label = A$Pval,
             y =1.1, hjust = 0)
  
  










