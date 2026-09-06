#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
library(vegan)
library(ggplot2)
library(ggrepel)
library(dplyr)
rm(list=ls())
env<-read.delim("env.txt",header = T,row.names = 1)
genus<-read.delim("step2.even.5000.feature-table.txt",header = T,row.names = 1)
mygroup<-read.delim('group.txt',header = T,stringsAsFactors = F)

mygroup$group<-factor(mygroup$group,levels = mygroup$group[!duplicated(mygroup$group)])
colnames(mygroup)<-c('sample','group')
genus<-genus[,mygroup$sample]

env<-env[mygroup$sample,]

genus1 <- scale(genus,center=F,scale=T)
env <- as.data.frame(scale(env,center=F,scale=T))


#spp=t(decostand(sp,method = "hellinger"))#Convert response variables
spp<-t(genus1)
#envc=log10(env)#Converting explanatory variables
decorana1<-decorana(spp)
decorana1
##
#Axis lengths 
#more than 3.5 using cca

uu<-rda(spp~.,env,scaling=2)#RDA Analysis
uu

#anova.cca(uu,by='terms')
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
yz=as.data.frame(ii$biplot[,1:2])*5
#grp=read.delim('group.txt',header = T,stringsAsFactors = F,row.names = 1)#Grouping by Square Type
#colnames(grp)="group"
#grp$group<-factor(grp$group,levels = levels(mygroup$group))
#grp<-grp[rownames(st),,drop=F]
st$sample<-rownames(st)
st<-merge(st,mygroup,by='sample')

mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,21,21,21)

ggplot() +
  #geom_text_repel(data = st,aes(RDA1,RDA2,label=row.names(st)),size=4)+#Show a Square
  geom_point(data = st,aes(RDA1,RDA2,shape=group,fill=group),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values = myshape)+
  # geom_segment(data = sp,aes(x = 0, y = 0, xend = RDA1, yend = RDA2),  arrow = arrow(angle=22.5,length = unit(0.35,"cm"), type = "closed"),linetype=1, size=0.6,colour = "red")+
  #geom_text_repel(data = sp,aes(RDA1,RDA2,label=row.names(sp)))+
  geom_segment(data = yz,aes(x = 0, y = 0, xend = RDA1, yend = RDA2), 
               arrow = arrow(angle=22.5,length = unit(0.25,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "blue")+
  geom_text_repel(data = yz,aes(RDA1,RDA2,label=row.names(yz)))+
  labs(x=paste("RDA 1 (", format(100 *ii$cont[[1]][2,1], digits=4), "%)", sep=""),
       y=paste("RDA 2 (", format(100 *ii$cont[[1]][2,2], digits=4), "%)", sep=""))+
  geom_hline(yintercept=0,linetype=2,size=0.5) + 
  geom_vline(xintercept=0,linetype=2,size=0.5)+
  guides(shape=guide_legend(title=NULL,color="black"),
         fill=guide_legend(title=NULL))+
  theme_bw()+theme(panel.grid=element_blank())

ggsave('step21.simple_rda.pdf',width = 8,height = 7)
