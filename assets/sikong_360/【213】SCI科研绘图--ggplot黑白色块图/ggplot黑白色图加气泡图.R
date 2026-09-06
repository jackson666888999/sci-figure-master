setwd("F:/生物信息学/GO多组气泡图")
A <- read.csv("GO多组气泡图.csv",header=T)
A$p <- ''
A$p[which(A$Padj <1.37e-06)]='<1.37e-06'
A$p[which(A$Padj <8.40e-15)]='<8.40e-15'
A$p[which(A$Padj <3.86e-16)]='<3.86e-16'


library(ggplot2)

ggplot(data=A,aes(x=Group,y=Description))+
  geom_tile(aes(fill=p),
            color="black")+
  geom_point(aes(size=GeneRatio), color="orange")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.title = element_blank(),
        #legend.title = element_blank(),
        axis.text.x = element_text(angle=45,hjust=1))+
  scale_fill_manual(values = c("#b8b8b8",
                               "#4b4b4b","#242424"))+
  labs(fill="FDR")













