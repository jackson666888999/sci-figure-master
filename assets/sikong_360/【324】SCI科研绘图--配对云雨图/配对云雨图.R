
setwd('C:/Users/34790/Desktop/配对云雨图')
df <- read.csv('df.csv', header = T)
library(ggplot2)
df$Family.ID <- as.factor(df$Family.ID)#将配对ID设置为因子，为了后续好配对
ggplot(df,aes(x=Disease.state,y=Richness,fill=Disease.state))+
  geom_violin(width =0.8, color=NA)+ #小提琴
  geom_boxplot(alpha =0.5,size=1,outlier.shape = NA,width=0.2)+#箱线图
  geom_rect(aes(xmin = 0.98, 
                ymin = -Inf,
                xmax = 2.02, 
                ymax = Inf),
            fill = "white", 
            size =1.5)+ #加一个分面
  geom_jitter(aes(group=Family.ID,color=Disease.state),
              size = 2,
              shape=16,
              stroke = 0.15, 
              show.legend = FALSE, 
              position = position_dodge(0.05))+#抖动点
  geom_line(aes(group = Family.ID), 
            color = 'grey40', 
            lwd = 0.5,
            position = position_dodge(0.05))+#连线
  theme_bw() + 
  theme(text = element_text(size=10, colour = "black")) + 
  theme(panel.grid =element_blank(),
        axis.text.x = element_text(colour = "black", size = 14),
        axis.text.y = element_text(colour = "black", size = 14),
        axis.title.y = element_text(color = 'black', size = 14),
        axis.title.x = element_blank(),
        legend.position = 'none')+
  labs(title = "", y = "Expression", x=" ")+
  scale_fill_manual(values = c('#E69F00', "#009E73"))




library(gghalves)
ggplot(df,aes(x=Disease.state,y=Richness,fill=Disease.state))+
  geom_half_violin(data=subset(df, Disease.state=='Patient'),#显示一半
                   position = position_nudge(x = 0),side="l",color=NA)+#side="l"表示朝向左边
  geom_half_boxplot(data=subset(df, Disease.state=='Patient'),
                    position = position_nudge(x = 0),side='l', width=0.2)+
  geom_half_violin(data=subset(df, Disease.state=='Relative'),
                   position = position_nudge(x = 0),side="r",color=NA)+#side="r"表示朝向右边
  geom_half_boxplot(data=subset(df, Disease.state=='Relative'),
                    position = position_nudge(x = 0),side='r', width=0.2)+
  geom_jitter(aes(group=Family.ID,color=Disease.state),
              size = 2,
              shape=16,
              stroke = 0.15, 
              show.legend = FALSE, 
              position = position_dodge(0.05))+
  geom_line(aes(group = Family.ID), 
            color = 'grey40', 
            lwd = 0.5,
            position = position_dodge(0.05))+
  theme_bw() + 
  theme(text = element_text(size=10, colour = "black")) + 
  theme(panel.grid =element_blank(),
        axis.text.x = element_text(colour = "black", size = 14),
        axis.text.y = element_text(colour = "black", size = 14),
        axis.title.y = element_text(color = 'black', size = 14),
        axis.title.x = element_blank(),
        legend.position = 'none')+
  labs(title = "", y = "Expression", x=" ")+
  scale_fill_manual(values = c('#E69F00', "#009E73"))
  
  
  










  