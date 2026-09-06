#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
rm(list=ls())
list.files()
library(vegan)
library(maptools)
library(ggplot2)
library(ggrepel)
library(dplyr)
genus<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
genus<-as.data.frame(t(genus))

env <- read.delim('env.txt',row.names = 1,header = T)
otu.dist <- vegdist(genus,method="bray")
#Pcoa
otu_pcoa<- cmdscale(otu.dist,eig=TRUE)
pc12 <- as.data.frame(otu_pcoa$points[,1:2])

env<-env[rownames(pc12),]
fit<-envfit(otu_pcoa,env,permutations = 999,na.rm = TRUE)

summary(fit)
fit
sink('step17.envfit_pcoa.txt',append=FALSE)
envfit(otu_pcoa,env,permutations = 999,na.rm = TRUE)
sink(file=NULL)
fit1<-as.data.frame(fit$vectors$arrows)
pc12$samples<-rownames(pc12)
groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'
groups$group<-factor(groups$group,levels = groups$group[!duplicated(groups$group)])

pc<-round(otu_pcoa$eig/sum(otu_pcoa$eig)*100,digits = 2)
pc12<-merge(pc12,groups,by='samples')

fit1<-fit1*0.5

mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,22,21,22)

ggplot() +
  #geom_text_repel(data = st,aes(RDA1,RDA2,label=row.names(st)),size=4)+#Show a Square
  geom_point(data = pc12,aes(V1,V2,shape=group,fill=group),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values = myshape)+
  #scale_color_manual(values=rep())+
  geom_segment(data = fit1,aes(x = 0, y = 0, xend = Dim1, yend = Dim2), 
               arrow = arrow(angle=12.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "red")+
  geom_text_repel(data = fit1,aes(Dim1,Dim2,label=row.names(fit1)))+
  guides(fill = guide_legend(override.aes = list(shape = 21)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("PCoA1(",round(pc[1],2),"%",")"),y=paste0("PCoA2(",round(pc[2],2),"%)"))+
  theme_bw()+theme(panel.grid=element_blank())

ggsave('step17.pcoa_envfit.pdf',width = 8,height = 6)




