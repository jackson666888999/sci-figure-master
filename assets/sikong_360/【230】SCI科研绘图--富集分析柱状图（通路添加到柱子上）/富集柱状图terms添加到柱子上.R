setwd("D:/KS项目/公众号文章/富集柱状图文字添加到柱子上")
library(ggplot2)
df <- read.csv("enrich.csv", header = T)
df$LogP <- -df$LogP#读入文件，logp处理一下

#文字标签坐标
df$labelx=rep(0,nrow(df))#x轴位置
df$labely=seq(nrow(df),1)#y轴位置

ggplot(data = df, 
       aes(LogP, reorder(Description,LogP))) + #reorder一下，让其按照从大到小排列
  geom_bar(stat="identity",
           alpha=0.5,
           fill="#FE8D3C",
           width = 0.8) + 
  geom_text(aes(x=labelx,#添加文字
                y=labely,
                label = Description),
            size=3.5, 
            hjust =0)+
  theme_classic()+
  theme(axis.text.y = element_blank(),
        axis.line.y = element_blank(),
        axis.title.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.line.x = element_line(colour = 'black', linewidth = 1),
        axis.text.x = element_text(colour = 'black', size = 10),
        axis.ticks.x = element_line(colour = 'black', linewidth = 1),
        axis.title.x = element_text(colour = 'black', size = 12))+
  xlab("-log10(qvalue)")+
  ggtitle("Enrichment")+
  scale_x_continuous(expand = c(0,0))




















