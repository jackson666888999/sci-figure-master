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

groups<-read.delim('group2.txt',header = T)
colnames(groups)[1]<-'samples'
nmds12<-merge(nmds12,groups,by='samples')
nmds12$group1<-factor(nmds12$group1,levels = unique(groups$group1))
nmds12$group2<-factor(nmds12$group2,levels = unique(groups$group2))

mycol<- c("#E41A1C" ,"#377EB8")
myshape<-21:22

ggplot() +
  geom_point(data = nmds12,aes(MDS1,MDS2,fill=group1,shape=group2),size=4)+
  scale_fill_manual(values=mycol)+
  scale_shape_manual(values = myshape)+
 # geom_text()
  #guides(fill = guide_legend(override.aes = list(shape = 21)))+
  geom_hline(yintercept=0,linetype=2) + 
  geom_vline(xintercept=0,linetype=2)+
  labs(x='NMDS1',y="NMDS2",title = stress)+
  theme_bw()+theme(panel.grid=element_blank(),
                   legend.title = element_blank())+
  guides(fill=guide_legend(override.aes = list(shape=21)))

ggsave('step13.twogroup_nmds.pdf',width = 8,height = 6)

