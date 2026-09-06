library(tidyverse)
library(ggthemes)

sub_design = read.table("metadata.txt", header=T, row.names=1, sep="\t")
beta = read.table("weighted_unifrac.txt",header=T, row.names=1, sep="\t", comment.char="")
idx = rownames(sub_design) %in% rownames(beta)
sub_design=sub_design[idx,]
sub_beta=beta[rownames(sub_design),rownames(sub_design)]
pcoa = cmdscale(sub_beta, k=3, eig=T)
points = as.data.frame(pcoa$points)
colnames(points) = c("x", "y", "z")
eig = pcoa$eig
points = cbind(points, sub_design[match(rownames(points), rownames(sub_design)), ])
Compartments=factor(points$Compartments,levels = c("BS","RS","RE","VE","SE","LE","P"))
Treatment=factor(points$Treatment,levels = c("CK","NPK","NPKM"))
library(ggplot2)
col=c("#1F78B4","#A6CEE3","#B2DF8A","#33A02C","#FB9A99","#FDBF6F","#E31A1C")
p= ggplot(points, aes(x=x, y=y,color=Compartments,shape=Treatment))+ geom_point(size=3)+ 
  labs(x=paste("PCoA 1 (", format(100 * eig[1] / sum(eig), digits=4), "%)", sep=""),
       y=paste("PCoA 2 (", format(100 * eig[2] / sum(eig), digits=4), "%)",sep=""))+
  scale_colour_manual(values = col)

mytheme = theme_classic() + theme(axis.text.x = element_text(size = 8),axis.text.y = element_text(size = 8))+
  theme(axis.title.y= element_text(size=12))+theme(axis.title.x = element_text(size = 12))+
  theme(legend.title=element_text(size=5),legend.text=element_text(size=5))
p=p+mytheme

p
#---------------优化后的代码

sub_design <- read.table("metadata.txt", header=T, row.names=1, sep="\t")
beta = read.table("weighted_unifrac.txt",header=T, row.names=1, sep="\t", comment.char="")
sub_design <- sub_design[rownames(sub_design) %in% rownames(beta),]

pcoa <- cmdscale(read.table("weighted_unifrac.txt", header = TRUE, row.names = 1,sep = "\t",
                            comment.char = "#")[rownames(sub_design),rownames(sub_design)], k = 3, eig = TRUE)

points <- as.data.frame(pcoa$points) %>%rename(x = V1, y = V2, z = V3) %>%
  rownames_to_column(var="row.names") %>% 
  left_join(sub_design %>% rownames_to_column(var="row.names"),by = "row.names")

points$Compartments <- factor(points$Compartments,levels = c("BS", "RS", "RE", "VE", "SE", "LE", "P"))
points$Treatment <- factor(points$Treatment,levels = c("CK", "NPK", "NPKM"))

col <- c("#1F78B4", "#A6CEE3", "#B2DF8A", "#33A02C", "#FB9A99", "#FDBF6F", "#E31A1C")

ggplot(points, aes(x = x, y = y, color = Compartments, shape = Treatment)) +
  geom_point(size = 3) +
  labs(x = paste("PCoA 1 (", format(100 * pcoa$eig[1] / sum(pcoa$eig), digits = 4), "%)", sep = ""),
       y = paste("PCoA 2 (", format(100 * pcoa$eig[2] / sum(pcoa$eig), digits = 4), "%)", sep = "")) +
  scale_colour_manual(values = col) +
  theme_set(theme_classic()) +
  theme(axis.text.x = element_text(size = 8,color="black"),
        axis.text.y = element_text(size = 8,color="black"),
        axis.title.y = element_text(size = 12,color="black"),
        axis.title.x = element_text(size = 12,color="black"),
        legend.title = element_text(size = 8,color="black"),
        legend.text = element_text(size = 8,color="black"))


