
setwd("D:/KS项目/公众号文章/ggplot点线图")
df <- read.csv("点线图.csv", header = T)
#做这个图其实需要三个要素就足够了，一个是点的平均值
#另外就是线的最大值和最小值

#分别计算下
df$mean <- rowMeans(df[,3:6])
df$Max <- apply(df[,3:6], 1, function(x){max(x)})
df$Min <- apply(df[,3:6], 1, function(x){min(x)})


library(ggplot2)
library(forcats)
df$Phenotype <- as.factor(df$Phenotype)
df$Phenotype <- fct_inorder(df$Phenotype)

#设置下坐标轴文字颜色
col <- c(rep("black",13),rep("red",6))

#method1
ggplot(data=df,aes(x=Phenotype,y=mean))+
  geom_errorbar(aes(ymin=Min,ymax=Max),width=0, color='#00798C')+
  geom_point(size=5, color='#00798C')+
  theme_classic()+
  theme(axis.text.x = element_text(colour = 'black',size = 10,angle=45,vjust = 1,hjust = 1, color = col),
        axis.text.y = element_text(colour = 'black',size = 10),
        axis.title.x = element_blank(),
        axis.title.y = element_text(colour = 'black',size = 12))+
  ylab("SRC")+
  geom_hline(yintercept =0,linetype=1,size=0.5)


#method2
ggplot(data=df,aes(x=Phenotype,y=mean))+
  geom_pointrange(aes(ymin=Min,ymax=Max),size=1)

#method3
#geom_linerange也可以
ggplot(data=df,aes(x=Phenotype,y=mean))+
  geom_linerange(aes(ymin=Min,ymax=Max),size=1)+
  geom_point(size=5)




