#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
rm(list=ls())
library(vegan)
library(ggpubr)
library(reshape2)
library(patchwork)
library(ggsci)

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

mycol<-c('#E41A1C','#377EB8','#4DAF4A','#984EA3')

p<-ggscatter(pc12, x = "PC1", y = "PC2",
             color = "group", shape = "group", palette = mycol, size=3,
             ellipse = TRUE, conf.int.level = 0.95,
             star.plot = T
             )+
  #xlab(paste0("PCoA",PC1,"(",round(pc[PC1],2),"%",")"))+
  ylab(paste0("PCoA2(",round(pc[2],2),"%",")"))+
  geom_hline(yintercept = 0, color = '#B3B3B3', linetype = "solid")+
  geom_vline(xintercept = 0, color = '#B3B3B3', linetype = "solid")+
  theme(axis.title.x = element_blank(),
        axis.title.y=element_text(face='bold',size=15),
        legend.position = "top",legend.title = element_blank(),
        panel.border = element_rect(color = "black",size = 1.0,fill = NA),
        text = element_text(size=12)) 


p

otu.dist<-as.matrix(otu.dist)
otu.dist<-otu.dist[groups$samples,groups$samples]
adist<-as.dist(otu.dist)
ADONIS<-adonis(adist~groups$group)

ADONIS


TEST<-ADONIS$aov.tab$`Pr(>F)`[1]
R2adonis<-round(ADONIS$aov.tab$R2[1],digits = 3)
sink('step19.adonis.txt')
print(ADONIS)
sink()


p<-p+ggtitle(label =expr(paste(bold(Bray)," ",bold(Curtis),bold(","),bold(Adnois:R^2),bold('='),bold(!!R2adonis),
                               bold(","),bold(P),bold('='),!!TEST))) +
  theme(title = element_text(size = 10))

cp <- combn(levels(pc12$group),2)
comp <- list()
for(i in 1:ncol(cp)){
  comp[[i]] <- cp[,i]
}

comp[c(1,6)]

pl<-ggboxplot(pc12, x="group", y="PC2", fill = "group", palette = mycol) +
  stat_compare_means(comparisons = comp, label = "p.signif",method="wilcox.test")+
  theme(panel.border = element_rect(color = "black",size = 1.0,fill = NA),
        #axis.text.y = element_blank(),
        #axis.ticks.y= element_blank(),
        #axis.title.y = element_blank(),
        legend.position = "none",
        axis.text = element_text(face='bold'),
        axis.title.x = element_blank(),
        axis.text.x = element_text(size = 12,angle = 60,hjust = 1,face='bold'),
        axis.title.y = element_blank())

pl
pt<-ggboxplot(pc12, x="group", y="PC1", fill = "group", palette = mycol) + coord_flip() +
  stat_compare_means(comparisons = comp, label = "p.signif",method="wilcox.test") +
  scale_x_discrete(limits = rev(levels(pc12$group)))+
  ylab(paste0("PCoA1(",round(pc[1],2),"%",")"))+
  theme(panel.border = element_rect(color = "black",size = 1.0,fill = NA),
        #axis.text.x = element_blank(),
        #axis.ticks.x = element_blank(),
        #axis.title.x = element_blank(),
        legend.position = "none",
        axis.text = element_text(size = 12, angle = 0,face='bold'),
        axis.title.y=element_blank(),
        axis.title.x = element_text(size = 15,face='bold'))

p0 <- ggplot() + theme(panel.background = element_blank())

p+pl+pt+p0+plot_layout(ncol = 2,nrow = 2,heights = c(4,1),widths = c(4,1))
ggsave('step16.pcoa_boxplot.pdf',width=8,height=7)
write.table(otu_pcoa$points, "step16.pcoa_sites.xls", sep="\t", col.names=NA)
write.table(otu_pcoa$eig/sum(otu_pcoa$eig), "step16.pcoa_importance.xls", sep="\t")




