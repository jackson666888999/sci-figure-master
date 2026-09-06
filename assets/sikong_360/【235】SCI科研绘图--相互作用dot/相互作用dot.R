setwd("E:/生物信息学/互作点图")
A <- read.csv("相互点图.csv", header = T,row.names = 1)
library(forcats)
A$B <- as.factor(A$B)#将B这一列转为因子
A$B <- fct_inorder(A$B)#排序，让其按照我们文件顺序显示

library(ggplot2)
ggplot(A,aes(x=B,y= A,color=A)) + 
  geom_point(aes(size=Value)) +#加入点，大小用Value表示
  scale_size(rang = c(0,10)) +#调整气泡大小
  scale_x_discrete(position = "bottom" ,expand=c(0.2,0))+#调整x轴范围
  labs(x=NULL,y=NULL)+#不要坐标轴标题
  theme_bw()+#ggplot主题
  theme(axis.text.x=element_text(angle=90,hjust = 1,vjust=0.5),#x轴文字调整
        panel.border = element_blank(),#不要边框
        axis.text =element_text(size = 12, color = "black"),#坐标轴文字调整
        axis.ticks = element_blank())+#坐标轴指标去除
  scale_colour_manual(name ="other", values =c('#efb306',#修改默认颜色
                                               '#eb990c',
                                               '#e8351e',
                                               '#cd023d',
                                               '#852f88',
                                               '#4e54ac',
                                               '#0f8096'))+
  guides(color=F)#去除颜色legend




#Cell <- read.table("22222.txt",header = T,sep = "\t")
#ggplot(Cell,aes(x=receptor,y= factor)) + 
#  geom_point(aes(size=Sum.Log2FC.),color="dodgerblue1") +
#  scale_size(rang = c(0,8)) + ###调整气泡大小 
#  scale_x_discrete(position = "bottom" ,expand=c(0.2,0))+
#  labs(x=NULL,y=NULL)+
#  theme_bw()+
#  theme(axis.text.x=element_text(angle=90,hjust = 1,vjust=0.5))