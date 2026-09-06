#test
###written by 983499199@qq.com; Huimin Zhang
##https://shop113546122.taobao.com/
###video reccord 
library(ggplot2)
rm(list=ls())
input1<-'feature-table.txt'

df1<-read.delim(input1,skip = 1,header = T,row.names = 1,check.names = F)
csum<-as.data.frame(colSums(df1))
colnames(csum)<-'taxnumber'
summary(csum$taxnumber)
csum$sample<-rownames(csum)
csum2<-csum[order(csum$taxnumber,decreasing = T),]
csum2$sample<-factor(csum2$sample,levels = rev(csum2$sample))
ggplot(data=csum2,aes(x=sample,y=taxnumber,fill=taxnumber))+
  geom_bar(stat='identity')+
  coord_flip()


#
mydepth<-5000
ggplot(data=csum2,aes(x=sample,y=taxnumber,fill=taxnumber))+
  geom_bar(stat='identity')+
  coord_flip()+
  geom_hline(yintercept  =mydepth,color='red',lty=2)

ggsave(paste0('step2.even.',mydepth,'.',input1,'.pdf'),width = 5,height = 7)
###define rarefaction depth

# mydepth<-min(csum$taxnumber)###
df2<-df1[,csum$sample[csum$taxnumber>=mydepth]]

library(GUniFrac)
df3<-t(df2)
df4<-Rarefy(df3, depth =mydepth)$otu.tab.rff
df5<-as.data.frame(t(df4))
colSums(df5)
df5<-df5[rowSums(df5)>0,]
write.table(cbind(tax=rownames(df5),df5),paste0('step2.even.',mydepth,'.',input1),sep = '\t',quote = F,row.names = F)

