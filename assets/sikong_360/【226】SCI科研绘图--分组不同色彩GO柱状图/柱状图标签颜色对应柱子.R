setwd("E:/生物信息学/分组不同色彩GO柱状图")
A <- read.csv("GO.csv", header = T)
library(ggplot2)
library(forcats)
A$Description <- as.factor(A$Description)
A$Description <- fct_inorder(A$Description)

#基础柱状图
ggplot(A)+
  geom_bar(aes(Description, Count),stat = "identity")+
  coord_flip()

#修改
ggplot(A,aes(Description, Count))+
  geom_bar(aes(fill=Cluster),stat = "identity")+
  geom_text(aes(label=Count, y=Count+5),size=3)+
  coord_flip()+
  labs(x='',y='Gene count', title = 'GO enrichment of cluster')+
  scale_fill_manual(values = c('#852f88',
                               '#eb990c',
                               '#0f8096'))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = 'none',
        axis.ticks.y = element_blank(),
        plot.title = element_text(hjust = 0.5, size = 10))
  
#修改标签颜色
table(A$Cluster)#查看每个cluster有多少元素
#Cluster1 Cluster2 Cluster3 
#13       12       13 
col <- c(rep("#852f88",13),rep("#eb990c",12),rep("#0f8096",13))#将每个元素赋予柱状图的颜色


ggplot(A,aes(Description, Count)) +
  geom_bar(aes(fill=Cluster), stat = "identity") +
  geom_text(aes(label=Count, y=Count+5), size=3) +
  coord_flip() +
  labs(x='', y='Gene count', title = 'GO enrichment of cluster') +
  scale_fill_manual(values = c('#852f88',
                              '#eb990c',
                              '#0f8096')) + #修改柱状图颜色
  theme_bw() +
  theme(panel.grid = element_blank(),
        legend.position = 'none',
        axis.ticks.y = element_blank(),
        plot.title = element_text(hjust = 0.5, size = 10), #标题居中，修改字体大小
        axis.text.y = element_text(size=rel(0.85), colour = "black"), #修改y轴文字大小，颜色
        plot.margin=unit(x=c(top.mar=0.2, right.mar=0.2,
                             bottom.mar=0.2, left.mar=0.2),
                         units="inches")) #微调图的大小





