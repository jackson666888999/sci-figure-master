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
pc12$samples<-rownames(pc12)
groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'

pc<-round(otu_pcoa$eig/sum(otu_pcoa$eig)*100,digits = 2)
pc12<-merge(pc12,groups,by='samples')
pc12$group<-factor(pc12$group,levels = unique(groups$group))
colnames(pc12)[2:3]<-c('PC1','PC2')
mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-c(21,21,21,21)


otu.dist<-as.matrix(otu.dist)
otu.dist<-otu.dist[groups$samples,groups$samples]
adist<-as.dist(otu.dist)
ADONIS<-adonis(adist~groups$group)
ADONIS
TEST<-ADONIS$aov.tab$`Pr(>F)`[1]
R2adonis<-round(ADONIS$aov.tab$R2[1],digits = 3)
sink('step9.adonis.txt')
print(ADONIS)
sink()

Fvalue<-round(ADONIS$aov.tab$F.Model[1],digits = 3)


ggplot(data = pc12,aes(PC1,PC2)) +
  #geom_text_repel(data = pc12,aes(PC1,PC2,label=samples),size=4)+#
  geom_point(aes(fill=group,shape=group),size=3,color='black')+
  stat_ellipse(aes(x = PC1, y =PC2, color = group), linetype = 1, level = 0.95,show.legend = F) +
  scale_shape_manual(values =myshape)+
  scale_fill_manual(values=mycol)+
  scale_color_manual(values=mycol)+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("PCoA1(",round(pc[1],2),"%",")"),y=paste0("PCoA2(",round(pc[2],2),"%)"))+
  ggtitle(label = paste(  'PERMANOVA:F=', Fvalue,', p=',TEST,sep = ''))+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank(),
                   axis.text = element_text(size=10),
                   axis.title = element_text(size=12))

ggsave('step9.pcoa.pdf',width = 6,height = 4)

write.table(otu_pcoa$points, paste0('step9.',"pcoa_by_group_sites.xls"), sep="\t", col.names=NA,quote = F)
write.table(otu_pcoa$eig/sum(otu_pcoa$eig), paste0('step9.',"pcoa_by_group_importance.xls"), sep="\t",quote = F)


#

ggplot(data = pc12,aes(PC1,PC2)) +

  geom_point(aes(fill=group,shape=group),size=3,color='black')+
 # stat_ellipse(aes(x = PC1, y =PC2, color = group), linetype = 1, level = 0.95,show.legend = F) +
  scale_shape_manual(values =myshape)+
  geom_text_repel(data = pc12,aes(PC1,PC2,label=samples),size=4)+#
  scale_fill_manual(values=mycol)+
  scale_color_manual(values=mycol)+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x=paste0("PCoA1(",round(pc[1],2),"%",")"),y=paste0("PCoA2(",round(pc[2],2),"%)"))+
 ggtitle(label = paste(  'PERMANOVA:F=', Fvalue,', p=',TEST,sep = ''))+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank(),
                   axis.text = element_text(size=10),
                   axis.title = element_text(size=12))

ggsave('step9.pcoa_with_name.pdf',width = 6,height = 4)
