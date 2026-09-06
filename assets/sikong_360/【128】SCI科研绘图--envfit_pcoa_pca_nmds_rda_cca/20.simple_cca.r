#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
library(vegan)
library(ggplot2)
library(ggrepel)
library(dplyr)
env<-read.delim("env.txt",header = T,row.names = 1)
genus<-read.table("step2.even.5000.feature-table.txt",header = T,row.names = 1)
mygroups<-read.delim('group.txt',header = T,stringsAsFactors = F)
colnames(mygroups)<-c('sample','group')
mygroups$group<-factor(mygroups$group,levels = mygroups$group[!duplicated(mygroups$group)])

genus<-genus[,mygroups$sample]

env<-env[mygroups$sample,]
genus1 <- scale(genus,center=F,scale=T)
decorana1<-decorana(t(genus1))
decorana1
#more than 3.5 using cca

env <- as.data.frame(scale(env,center=F,scale=T))

#spp=t(decostand(sp,method = "hellinger"))#Convert response variables
spp<-t(genus1)
#envc=log10(env)#Converting explanatory variables
uu<-cca(spp~.,env,scaling=2)#RDA Analysis
uu

anova.cca(uu,by='terms')
#anova(uu,by='axis')
#anova.cca(uu,by='margin')
envfit(uu, env, perm = 999)
ii<-summary(uu)  #View analysis results
sp<-as.data.frame(ii$species[,1:2])*2#Depending on the drawing result, the drawing data can be enlarged or reduced to a certain extent, as follows
#only show top 10genus
genus$mysum<-rowSums(genus)
genus$mygenus<-rownames(genus)
topgenus<-as.data.frame(genus %>%arrange(desc(mysum)))[1:10,]
sp=sp[topgenus$mygenus,]/2
st=as.data.frame(ii$sites[,1:2])
yz=as.data.frame(ii$biplot[,1:2])*2
st$sample<-rownames(st)
st<-merge(st,mygroups,by='sample')

mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,21,21,21)
ggplot() +
  geom_text_repel(data = st,aes(CCA1,CCA2,label=sample),size=4,max.overlaps = 20)+#Show a Square
  geom_point(data = st,aes(CCA1,CCA2,shape=group,fill=group),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values = myshape)+
  
  #show top contribute species
  #geom_segment(data = sp,aes(x = 0, y = 0, xend = CCA1, yend = CCA2), arrow = arrow(angle=22.5,length = unit(0.35,"cm"), type = "closed"),linetype=1, size=0.6,colour = "red")+
  #geom_text_repel(data = sp,aes(CCA1,CCA2,label=row.names(sp)))+
  geom_segment(data = yz,aes(x = 0, y = 0, xend = CCA1, yend = CCA2), 
               arrow = arrow(angle=22.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "blue")+
  geom_text_repel(data = yz,aes(CCA1,CCA2,label=row.names(yz)),max.overlaps = 10)+
  labs(x=paste("CCA 1 (", format(100 *ii$cont[[1]][2,1], digits=4), "%)", sep=""),
       y=paste("CCA 2 (", format(100 *ii$cont[[1]][2,2], digits=4), "%)", sep=""))+
  geom_hline(yintercept=0,linetype=2,size=0.5,color='gray') + 
  geom_vline(xintercept=0,linetype=2,size=0.5,color='gray')+
  guides(shape=guide_legend(title=NULL,color="black"),
         fill=guide_legend(title=NULL))+
  theme_bw()+theme(panel.grid=element_blank())

ggsave('step20.simple_cca.pdf',width = 8,height = 7)
