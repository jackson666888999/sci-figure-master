rm(list=ls())
options(stringsAsFactors = F)
#install.packages("vegan")
library(vegan)
#library(maptools)
library(ggplot2)
library(ggrepel)
library(dplyr)
library(RColorBrewer)
mydata<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
mydata<-as.data.frame(t(mydata))
mydata=decostand(mydata,method = "hellinger")
otu_pca<- prcomp(mydata,scal=F)
pc12 <- as.data.frame(otu_pca$x[,1:2])*100
pc12$samples<-rownames(pc12)

groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'
groups$group<-factor(groups$group,levels = groups$group[!duplicated(groups$group)])

pc <-summary(otu_pca)$importance[2,]*100
pc12<-merge(pc12,groups,by='samples')
colnames(pc12)[2:3]<-c('PC1','PC2')
paste(brewer.pal(n=4,'Set1'),collapse = "','")
mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')

ggplot(data = pc12,aes(x=PC1,y=PC2,color=group,shape=group)) +
  geom_point(size=3)+
  geom_hline(yintercept=0,linetype=2,color='gray') + 
  geom_vline(xintercept=0,linetype=2,color='gray')+
  labs(x=paste0("PC1(",round(pc[1],2),"%",")"),y=paste0("PC2(",round(pc[2],2),"%)"))+
  theme_bw()+
  theme(panel.grid = element_blank())+
  stat_ellipse(aes(x = PC1, y =PC2, color = group,fill=group),alpha=0.1, 
               linetype = 1, level = 0.95,geom='polygon') +
  scale_color_manual(values = mycol)

ggsave('step8.pca.pdf',width = 6,height = 4)

#

ggplot(data = pc12,aes(PC1,PC2,color=group,shape=group,label=samples)) +
  geom_point(size=3)+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  geom_text_repel()+
  labs(x=paste0("PC1(",round(pc[1],2),"%",")"),y=paste0("PC2(",round(pc[2],2),"%)"))+
  theme_bw()+
  theme(panel.grid = element_blank())+
 # stat_ellipse(aes(x = PC1, y =PC2, color = group,fill=group),alpha=0.1,   linetype = 1, level = 0.95,geom='polygon') +
  scale_color_manual(values = mycol)

ggsave('step8.pca_withname.pdf',width = 6,height = 4)



