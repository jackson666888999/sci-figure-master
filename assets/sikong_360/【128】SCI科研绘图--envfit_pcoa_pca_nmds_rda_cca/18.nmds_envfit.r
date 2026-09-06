#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
#test
rm(list=ls())
library(dplyr)
library(vegan)
library(ggpubr)
library(RColorBrewer)
library(ggplot2)
library(ggrepel)
options(stringsAsFactors=F)

genus<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
genus<-na.omit(genus)
genus<-as.data.frame(t(genus))
env <- read.delim('env.txt',row.names = 1,header = T)

dist <- vegdist(genus, method="bray",na.rm = T)
dist <- as.matrix(dist)
nmds_result<-  metaMDS(dist,k=2)
stress <- paste0("Stress=",round(nmds_result$stress,3))

nmds12 <- as.data.frame(nmds_result$points)

env<-env[rownames(nmds12),]
fit<-envfit(nmds_result,env,permutations = 999,na.rm = TRUE)
warnings()
summary(fit)
fit
sink('step18.nmds_envfit1.txt',append=FALSE)
envfit(nmds_result,env,permutations = 999,na.rm = TRUE)
sink(file=NULL)
fit1<-as.data.frame(fit$vectors$arrows)
nmds12$samples<-rownames(nmds12)
groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'
nmds12<-merge(nmds12,groups,by='samples')

fit1<-fit1
mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,22,21,22)
ggplot() +
  #geom_text_repel(data = st,aes(RDA1,RDA2,label=row.names(st)),size=4)+#Show a Square
  geom_point(data = nmds12,aes(MDS1,MDS2,fill=group,shape=group),size=4)+
  #scale_color_manual(values=rep())+
  geom_segment(data = fit1,aes(x = 0, y = 0, xend = NMDS1, yend = NMDS2), 
               arrow = arrow(angle=22.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "red")+
  scale_fill_manual(values = mycol)+
  #stat_ellipse(data = nmds12,aes(MDS1,MDS2,color=group), level = 0.95)+
  geom_text_repel(data = fit1,aes(NMDS1,NMDS2,label=row.names(fit1)))+
  scale_shape_manual(values =myshape)+
  guides(fill = guide_legend(override.aes = list(shape = 21)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x='NMDS1',y="NMDS2",title = stress)+
  theme_bw()+theme(panel.grid=element_blank())

ggsave('step18.nmds_envfit.pdf',width = 8,height = 6)



