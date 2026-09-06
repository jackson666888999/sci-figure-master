setwd('D:/KS项目/公众号文章/ggplot做split小提琴图')
library(devtools)
install_github("JanCoUnchained/ggunchained")
library(ggunchained) 
library(ggplot2)
library(ggpubr)

df <- read.csv('df.csv',header = T,row.names = 1)
colnames(df) <- c('gene','sample','group')
#常规作图，geom_split_violin函数即可
ggplot(df, aes(x = sample,y = gene, fill = group))+
  geom_split_violin(colour=NA, scale = 'width')+
  scale_fill_manual(values = c("limegreen", "navy"))+
  theme_bw()+
  labs(title = "Mmp8", y="Expression", x = "")+#标题设置
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.y = element_text(size = 10, color="black"),
        panel.background = element_blank(),
        axis.text.x = element_text(size = 10, color="black",angle = 90),
        axis.title.y = element_text(size = 12, color="black"))


#我们还可以进行修饰，添加显著性检验标记等等
ggplot(df, aes(x = sample,y = gene, fill = group))+
  geom_split_violin(colour=NA, scale = 'width')+
  scale_fill_manual(values = c("limegreen", "navy"))+
  theme_bw()+
  labs(title = "Mmp8", y="Expression", x = "")+#标题设置
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.y = element_text(size = 10, color="black"),
        panel.background = element_blank(),
        axis.text.x = element_text(size = 10, color="black",angle = 90),
        axis.title.y = element_text(size = 12, color="black"))+
  stat_summary(fun = mean,
               fun.min = function(x){quantile(x)[2]},
               fun.max = function(x){quantile(x)[4]},
               geom = "pointrange",
               size=0.3,
               position = position_dodge(width = 0.5),
               color='white')+
  ylim(0,5)+
  stat_compare_means(aes(group = group), label = "p.signif",label.y = 4.5)
