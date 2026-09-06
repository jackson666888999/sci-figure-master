#test
rm(list=ls())
library(ggpubr)
library(RColorBrewer)
library(ggrepel)
library(ropls)
library(dplyr)
library(reshape2)
mymetabolite<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
mymetabolite<-as.data.frame(t(mymetabolite))
groups<-read.delim('group1.txt',header = T)
colnames(groups)[1]<-'samples'
mymetabolite<-mymetabolite[groups$samples,]
groups$group<-factor(groups$group,levels = unique(groups$group))
mymetabolite<-as.matrix(mymetabolite)
mygroup<-groups$group
oplsda = opls(mymetabolite, mygroup,predI = 1,orthoI=NA)#
#plot(oplsda@scoreMN[,1],oplsda@orthoScoreMN[,1])
pc12 <- as.data.frame(cbind(t1=oplsda@scoreMN[,1],t2=oplsda@orthoScoreMN[,1]))
pc <- round(oplsda@modelDF$R2X[1:2]*100,digits = 2)
colnames(pc12) <- c("pc_x","pc_y")
pc12['samples'] <- rownames(pc12)
pc12 <- merge(pc12,groups,by="samples")
mycol<-c( "#E41A1C", "#377EB8" )
myshape<-c(21,21)
ggplot(data = pc12,aes(x=pc_x,y=pc_y)) +
  #geom_text_repel(data = pc12,aes(PC1,PC2,label=samples),size=4)+#
  geom_point(aes(fill=group,shape=group),size=3,color='black')+
  stat_ellipse(aes(x=pc_x,y=pc_y, fill= group), geom = 'polygon',linetype = 1, alpha=0.2,
               level = 0.95,show.legend = F) +
  scale_fill_manual(values=mycol)+
  scale_color_manual(values=mycol)+
  scale_shape_manual(values =myshape)+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("T score(",round(pc[1],2),"%",")"),y=paste0("Orthogonal T score(",round(pc[2],2),"%",")"),
       title = 'OPLS-DA')+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank(),
                   axis.text = element_text(size=10),
                   axis.title = element_text(size=12))
ggsave('step14.oplsda_score_plot.pdf',width = 6,height = 4)
