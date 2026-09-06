#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 

rm(list=ls())
list.files()
library(vegan)
#library(maptools)
library(ggplot2)
library(ggrepel)
library(dplyr)

mydata<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
mydata<-as.data.frame(t(mydata))
mydata=decostand(mydata,method = "hellinger")
env <- read.delim('env.txt',row.names = 1,header = T)
otu_pca<- prcomp(mydata,scal=F)

pc12 <- as.data.frame(otu_pca$x[,1:2])
env<-env[rownames(pc12),]
fit<-envfit(otu_pca,env,permutations = 999,na.rm = TRUE)

fit

sink('step19.envfit1.txt',append=FALSE)
fit
sink(file=NULL)
fit1<-as.data.frame(fit$vectors$arrows)
pc12$samples<-rownames(pc12)

groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'

groups$group<-factor(groups$group,levels = groups$group[!duplicated(groups$group)])
pc <-summary(otu_pca)$importance[2,]*100

pc12<-merge(pc12,groups,by='samples')

fit2<-fit1
mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,22,21,22)

ggplot() +
  #geom_text_repel(data = st,aes(RDA1,RDA2,label=row.names(st)),size=4)+#Show a Square
  geom_point(data = pc12,aes(PC1,PC2,shape=group,fill=group),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values =myshape)+
  #scale_color_manual(values=rep())+
  geom_segment(data = fit2,aes(x = 0, y = 0, xend = PC1, yend = PC2), 
               arrow = arrow(angle=12.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "red")+
  geom_text_repel(data = fit1,aes(PC1,PC2,label=row.names(fit1)))+
  guides(fill = guide_legend(override.aes = list(shape = myshape)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("PC1(",round(pc[1],2),"%",")"),y=paste0("PC2(",round(pc[2],2),"%)"))+
  theme_bw()+theme(panel.grid=element_blank())

ggsave('step19.pca_envfit.pdf',width = 8,height = 6)

