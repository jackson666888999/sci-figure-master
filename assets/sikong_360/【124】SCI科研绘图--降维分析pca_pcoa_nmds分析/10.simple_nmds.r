#test
library(vegan)
library(ggplot2)
library(RColorBrewer)
library(scales)

genus<- read.delim('step2.even.5000.feature-table.txt',header = T, row.names = 1,check.names = F)
#genus<-as.data.frame(t(scale(genus)))
genus<-as.data.frame(t(genus))
dist <- vegdist(genus, method="bray")
dist <- as.matrix(dist)
nmds_result<-  metaMDS(dist,k=2)
stress <- paste0("Stress=",scientific(nmds_result$stress,digits = 3))

nmds12 <- as.data.frame(nmds_result$points)
nmds12$samples<-rownames(nmds12)

groups<-read.delim('group.txt',header = T)
colnames(groups)[1]<-'samples'

nmds12<-merge(nmds12,groups,by='samples')

mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')
myshape<-21:25
ggplot() +
  geom_point(data = nmds12,aes(MDS1,MDS2,shape=group,fill=group),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values =myshape )+
 # geom_text()
  #guides(fill = guide_legend(override.aes = list(shape = 21)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x='NMDS1',y="NMDS2",title = stress)+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank())

ggsave('step10.nmds.pdf',width = 8,height = 6)
library(ggrepel)
ggplot(data = nmds12,aes(MDS1,MDS2,shape=group,fill=group,label=samples)) +
  geom_point(size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values = 21:25)+
  geom_text_repel(max.overlaps =30)+
  #guides(fill = guide_legend(override.aes = list(shape = 21)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x='NMDS1',y="NMDS2",title = stress)+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank())


ggsave('step10.nmds_with_name.pdf',width = 8,height = 6)
