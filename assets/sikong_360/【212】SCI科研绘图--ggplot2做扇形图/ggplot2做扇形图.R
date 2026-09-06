
library(ggplot2)
library(dplyr)
value <- c(24.2, 21.9, 7.6, 5.2,4.3,3.2,2.6,2.6,1.8,1.8,24.8)
disease <- c("Heart disease", "Cancer","injuries", "CPD",
               "Stroke",'Type2 diabetes',"AD","Suicide",
               "IP","Chronic liver disease","Other")
Group <- c("male","male","male","male","male","male",
             "male","male","male","male","male")
A <- data.frame(Group, disease,value)#构建一个数据
A$disease <- factor(A$disease, levels = A$disease)#按照既定顺序
ggplot(A, aes(x = "",y = value,fill = disease)) +
  geom_bar(width = 1,stat = "identity",color = "white")



#构建扇形图数据
A <- A %>% 
  mutate(prop = value/sum(value)) %>% #计算占比比例
  arrange(desc(disease)) %>% #排序(堆叠柱状图的顺序，不能乱，否则有问题)
  mutate(pos = cumsum(prop)-0.5*prop)#计算y轴位置

A$xend <- ifelse(A$prop < 0.2, 2, 1.8)


#作图
ggplot(A, aes(x = "",y = prop,fill = disease)) +
  geom_bar(width = 1,stat = "identity",color = "white") +
  coord_polar("y",start = 0,clip = "off")+
  geom_segment(aes(x = 1.5,
                   y = pos,
                   xend = xend,
                   yend = pos),
               size =0.5,color = 'black')+#添加指示线
  geom_label(aes(y = pos,
                 x = xend,
                 label = paste(disease,scales::percent(prop))),
             size = 4,
             color = "white") +#添加文字
  theme(legend.position = "none") +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.ticks = element_blank(), 
        axis.text.y = element_blank(),
        axis.text.x = element_blank(),
        legend.title=element_blank(), 
        panel.border = element_blank(),
        panel.background = element_blank())+#去除没用的ggplot背景，坐标轴
  xlab("")+ylab('')+#添加颜色
  scale_fill_manual(values = c("#aeae5c", "#FB8072", "#1965B0", "#7BAFDE",
                              "#882E72","#B17BA6", "#FF7F00", "#FDB462",
                              "#E7298A", "#E78AC3","#33A02C"))
  
  
  
  
ggplot(A, aes(x = "",y = prop,fill = disease)) +
  geom_bar(width = 1,stat = "identity",color = "white") +
  coord_polar("y",start = 0,clip = "off")+
  geom_segment(aes(x = 1.5,
                   y = pos,
                   xend = xend,
                   yend = pos),
               size =0.5,color = 'black')+#添加指示线
  geom_text(aes(y = pos,
                 x = xend,
                 label = paste(disease,scales::percent(prop))),
             size = 4,
             color = "black") +#添加文字
  theme(legend.position = "none") +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.ticks = element_blank(), 
        axis.text.y = element_blank(),
        axis.text.x = element_blank(),
        legend.title=element_blank(), 
        panel.border = element_blank(),
        panel.background = element_blank())+#去除没用的ggplot背景，坐标轴
  xlab("")+ylab('')+#添加颜色
  scale_fill_manual(values = c("#aeae5c", "#FB8072", "#1965B0", "#7BAFDE",
                                        "#882E72","#B17BA6", "#FF7F00", "#FDB462",
                                        "#E7298A", "#E78AC3","#33A02C"))
  
  
  