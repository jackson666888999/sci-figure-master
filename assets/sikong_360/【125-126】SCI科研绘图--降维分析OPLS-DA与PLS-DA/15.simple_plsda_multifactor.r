#test
rm(list=ls())
library(ggpubr)
library(RColorBrewer)
library(ggrepel)
library(ropls)
mymetabolite<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
mymetabolite<-as.data.frame(t(mymetabolite))
groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'
mymetabolite<-mymetabolite[groups$samples,]
groups$group<-factor(groups$group,levels = unique(groups$group))
mymetabolite<-as.matrix(mymetabolite)
mygroup<-groups$group
plsda = opls(mymetabolite, mygroup,predI = 2,orthoI=0)

# sample scores plot
pc12 = plsda@scoreMN %>%  as.data.frame() 

pc <- round(plsda@modelDF$R2X[1:2]*100,digits = 2)

colnames(pc12) <- c("pc_x","pc_y")
pc12['samples'] <- rownames(pc12)
pc12 <- merge(pc12,groups,by="samples")
mycol<-c( "#377eb8","#EC7014","#7EC87E","#BDADD3", "#E31A1C",'#FFFFFF')
myshape<-c(21,21,21,21,21)
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
  labs(x=paste0("P1(",round(pc[1],2),"%",")"),y=paste0("P2 (",round(pc[2],2),"%",")"),
       title = "PLS-DA")+
  #scale_y_continuous(limits=c(-10, 10))+
  #scale_x_continuous(limits=c(-15, 10))+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank(),
                   axis.title = element_text(face = 'bold',size=16),
                   axis.text.x = element_text(size = 12,color="black"),
                   axis.text.y = element_text(size = 12,color="black"))

ggsave('step15.plsda_score_plot.pdf',width = 6,height = 4)


