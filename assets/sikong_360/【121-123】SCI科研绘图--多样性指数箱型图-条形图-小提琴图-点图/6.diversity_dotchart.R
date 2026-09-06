#test
rm(list=ls())
library(reshape2)
library(tidyverse)
library(ggpubr)
library(rstatix)
df1<-read.delim('step3.diversity.index.txt',header = T)
mygroup<-read.delim('group.txt',header = T)
colnames(mygroup)[1:2]<-c('sample','group')

mygroup$group<-factor(mygroup$group,levels = unique(mygroup$group))
df2<-merge(df1,mygroup,by='sample')
myindex<-'Richness'

df2$new<-df2[,myindex]

stat.test <- df2 %>%
  wilcox_test(new ~ group) 

# Box plots
stat.test <- stat.test %>% 
  add_xy_position(x = "group", dodge = 0.8,step.increase = 0.1)

stat.test$y.position
mycol<-c("#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072")

stat.test$p.adj.signif<-cut(stat.test$p,breaks =c(0,0.001,0.01,0.05,1),
                            labels = c('***','**','*','ns')  )


ggdotplot(df2, x = "group", y = "new", fill = "group")+
  stat_pvalue_manual(stat.test,   label = "p.adj.signif", tip.length = 0.02,
                     size = 6,
                     hide.ns = T)+ 
  scale_fill_manual(values = mycol)+
  labs(y=myindex,x=NULL)+
  theme_bw()+theme(legend.title = element_blank(),
                   legend.position = 'none',
                   axis.title = element_text(face = 'bold',size=12))




stat.test2<-as.data.frame(apply(stat.test,2,as.character))
write.table(stat.test2,paste0('step6.',myindex,'.dot.pdf.stat.xls'),row.names = F,sep = '\t',quote = F)

ggsave(paste0('step6.',myindex,'.dot.pdf'),width = 4,height = 4)

