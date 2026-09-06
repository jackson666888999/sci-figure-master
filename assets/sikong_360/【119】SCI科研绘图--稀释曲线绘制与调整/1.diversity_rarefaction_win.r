rm(list=ls())

setwd("G:/R模板/不会画图请找我会员特供/001.零基础24分钟学会稀释曲线绘制与调整--微生物研究数据分析必修课")
library(devtools)
#install_github('luffyluffy/GUniFrac')
library(GUniFrac)
library(picante)
library(ggplot2)
library(foreach)
library(doParallel)
library(dplyr)
numCores<-4
registerDoParallel(numCores)

alpha <- function(x, tree = NULL, base = exp(2)) {
  est <- vegan::estimateR(x)
  Sobs <- est[1, ]
  Chao <- est[2, ]
  ACE <- est[4, ]
  Shannon <- vegan::diversity(x, index = 'shannon')
  Simpson <- vegan::diversity(x, index = 'simpson')	#Gini-Simpson 指数
  Pielou <- Shannon / log(Sobs, base)
  goods_coverage <- 1 - rowSums(x == 1) / rowSums(x)
  result <- data.frame(Sobs, Shannon, Simpson, Pielou, Chao, ACE, goods_coverage)
  if (!is.null(tree)) {
    PD_whole_tree <- pd(x, tree, include.root = FALSE)[1]
    names(PD_whole_tree) <- 'PD_whole_tree'
    result <- cbind(result, PD_whole_tree)
  }
  result
}

df<-read.delim("feature-table.txt",header = T,row.names = 1,check.names=F,skip = 1)
otu <- t(df)#transform
stat1<-data.frame(cbind(sample=rownames(otu),totalreads=rowSums(otu)))
stat1$totalreads<-as.numeric(stat1$totalreads)
ggplot(data=stat1,aes(x=sample,y=totalreads))+
  geom_bar(stat='identity')+coord_flip()+theme_bw()

write.table(stat1,'stat.txt',row.names = F,sep = '\t',quote = F)
##
select1<-stat1$sample[stat1$totalreads>=5000]
otu<-otu[select1,]


depth<- 20000##less than the maximum depth
number_iteration<-200

depths<-c(1, seq(100,depth,by=number_iteration))
rarefaction<-NULL

final<-foreach (j=1:1,.combine=rbind) %do% {
    rarefaction<-foreach(mydepth=depths,.combine=rbind) %dopar%{
        df2<-GUniFrac::Rarefy(otu, depth =mydepth)$otu.tab.rff
        df3<-alpha(x=df2)
        df3$depth<-mydepth
        df3$sample<-rownames(df3)
        df3
    }
    rarefaction
}


write.table(final,'diversity_rarefaction_all.txt',row.names = F,sep = '\t',quote = F)
final1<-as.data.frame(final %>% group_by(sample,depth)%>% summarise_all(mean) )
write.table(final1,'diversity_rarefaction.txt',row.names = F,sep = '\t',quote = F)




##
#install.packages("reshape2")
#install.packages("showtext")
library(ggplot2)
library(reshape2)
library(dplyr)
library(RColorBrewer)
library(showtext)
showtext_auto(enable = T)
df<-read.delim('diversity_rarefaction.txt',header = T)
df<-na.omit(df)
df1<-melt(df,id.vars = c('sample','depth'))
df1$sample<-factor(df1$sample)
width_name<-0.12*length(levels(factor(df1$sample)))
width<-max(7,width_name)
df1<-df1[df1$depth>1,]
ggplot(data=df1,aes(x=depth,y=value,color=sample))+
  #geom_line(size=1)+
  geom_smooth(se=F,formula = y ~ log(x))+
  facet_wrap(~variable,scales = 'free')+
  theme_classic()

ggsave('step1.all_diversity_rarefaction.pdf',width = width+5,height = 10)
for (i in colnames(df)[-c(1:2)]){
 # i<-colnames(df)[5]
  ggplot(data=df,aes_string(x='depth',y=i,color='sample'))+
    #geom_line(size=1)+
    geom_smooth(se=F,formula = y ~ log(x))+
    theme_classic()+
    labs(x='Number of Sequences',y=i)
  ggsave(paste0('step1.',i,'_diversity_rafaction.pdf'),width=width,height = 5)
}



