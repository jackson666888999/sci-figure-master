rm(list=ls())
options(stringsAsFactors = F)
library(vegan)
library(ggplot2)
library(ggrepel)
library(dplyr)

genus<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
genus<-as.data.frame(t(genus))
otu.dist <- vegdist(genus,method="bray")
#Pcoa
otu_pcoa<- cmdscale(otu.dist,eig=TRUE)
pc12 <- as.data.frame(otu_pcoa$points[,1:2])

#pc12 <- as.data.frame(otu_pca$x[,1:2])
pc12$samples<-rownames(pc12)

groups<-read.delim('group2.txt',header = T)
colnames(groups)[1]<-'samples'

pc<-round(otu_pcoa$eig/sum(otu_pcoa$eig)*100,digits = 2)

pc12<-merge(pc12,groups,by='samples')
colnames(pc12)[2:3]<-c('PC1','PC2')
#

pc12$group1<-factor(pc12$group1,levels = unique(groups$group1))
pc12$group2<-factor(pc12$group2,levels = unique(groups$group2))

temp<-as.matrix(otu.dist)
table(colnames(temp)==groups$samples)

ADONIS<-adonis(otu.dist~groups$group1)
Fvalue<-round(ADONIS$aov.tab$F.Model[1],digits = 3)

TEST_adonis<-ADONIS$aov.tab$`Pr(>F)`[1]
R2adonis<-round(ADONIS$aov.tab$R2[1],digits = 3)
sink('adonis.txt')
print(ADONIS)
sink()
mycol<- c("#E41A1C" ,"#377EB8")
myshape<-21:22

ggplot(data = pc12,aes(PC1,PC2,group=group1,
                       # color=group1,
                       fill=group1,
                       shape=group2)) +
  geom_point(color='black',size=3)+
  scale_fill_manual(values=mycol)+
  scale_color_manual(values =mycol)+
  scale_shape_manual(values=myshape)+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("PCoA1(",round(pc[1],2),"%",")"),y=paste0("PCoA2(",round(pc[2],2),"%)"))+
  stat_ellipse(data=pc12,aes(x = PC1, y =PC2, fill =group1), linetype = 1,
               geom='polygon',alpha=0.3,
               level = 0.95,show.legend = F,inherit.aes = F) +
  guides(fill = guide_legend(title = 'group1',order = 1,
                             override.aes = list(size=4,fill=mycol,shape=21)),
         shape=guide_legend(title='group2',override.aes = list(size=3)))+
  ggtitle(label = paste(  'PERMANOVA:F=', Fvalue,', p=',TEST_adonis,sep = ''))+
  theme_bw()+theme(#panel.grid=element_blank(),
                   title=element_text(size=10))

ggsave('step12.pcoa_1.pdf',width = 7,height = 5)


