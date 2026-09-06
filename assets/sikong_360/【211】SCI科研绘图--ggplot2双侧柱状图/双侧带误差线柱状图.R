

df <- read.csv('df.csv', header = T)
# df <- df[-c(10:12), ]
write.csv(df, file="df.csv")
df <- cbind(df[,1:7], df[,8:14]* -1) #将下调的设置为-，只是为了区分画图，不代表表达为-

library(tidyr)
data <-gather(df, gene, value, 1:14)#宽数据转长数据,然后对数据分组。
data$group <- ''
# data$group <- ifelse(data$value >0, "Up_regulation", "Down_regulation")

#接下来做柱状图
ggplot(data, aes(fill=group, y=value, x=reorder(gene,-value)))+
  geom_bar(position=position_dodge(),#组内柱子间距为0
           stat="summary",
           width=0.9,#宽度
           size=1)+ #bar图
  stat_summary(fun.data = 'mean_se', 
               geom = "errorbar", 
               colour = "black",
               width = 0.2,
               position=position_dodge(0.7))+#添加误差线
  scale_fill_manual(values = c('#F69CA4','#EE2024'))+
  theme(axis.text.x = element_blank())+ 
  theme(axis.text.y = element_text(size = 12, color="black"),
        axis.line.y = element_line(color = 'black'),
        axis.title.y = element_text(size = 14, color="black"))+#y轴文字设置
  theme(axis.title.x = element_blank(),
        axis.ticks.x = element_blank())+
  theme(panel.grid = element_blank(),
        panel.background = element_blank())+
  theme(legend.position = 'none')+#不要legend
  geom_hline(aes(yintercept=0),linetype=1,cex=1,color='black')+
  labs(title = "", y="Relative expression", x = "")+#标题设置
  annotate(geom = 'text', label="Up_regulation", x=3.5, y=-15,size=4)+#添加文字
  annotate("segment", x = 0.5, xend = 7.5, y = -10, yend = -10, color='black')+ #添加线段
  annotate(geom = 'text', label="Down_regulation", x=11.5, y=15,size=4)+
  annotate("segment", x = 8.5, xend = 13.5, y = 10, yend = 10, color='black')
  

#当然了，如果你乐意，还可以加上散点，让样本量更加清晰，这也是很多杂志的要求
ggplot(data, aes(fill=group, y=value, x=reorder(gene,-value)))+
  geom_bar(position=position_dodge(),#组内柱子间距为0
           stat="summary",
           width=0.9,#宽度
           size=1)+ #bar图
  stat_summary(fun.data = 'mean_se', 
               geom = "errorbar", 
               colour = "black",
               width = 0.2,
               position=position_dodge(0.7))+#添加误差线
  scale_fill_manual(values = c('#F69CA4','#EE2024'))+
  theme(axis.text.x = element_blank())+ 
  theme(axis.text.y = element_text(size = 12, color="black"),
        axis.line.y = element_line(color = 'black'),
        axis.title.y = element_text(size = 14, color="black"))+#y轴文字设置
  theme(axis.title.x = element_blank(),
        axis.ticks.x = element_blank())+
  theme(panel.grid = element_blank(),
        panel.background = element_blank())+
  theme(legend.position = 'none')+#不要legend
  geom_hline(aes(yintercept=0),linetype=1,cex=1,color='black')+
  labs(title = "", y="Relative expression", x = "")+#标题设置
  geom_jitter(data = data, aes(y = value,x=reorder(gene,-value)),
              size = 3, shape = 16,
              color="grey60",
              stroke = 0.15, show.legend = FALSE, 
              position = position_jitterdodge(jitter.height=0.5,
                                              jitter.width = 0.1,
                                              dodge.width = 0.8))





  
  
