library(tidyverse)
library(igraph)
library(ggraph)
library(ggplot2)
library(ggnetwork)

setwd('D:\\KS项目\\公众号文章\\pyscenic-TF-target-gene-网络图')
#读入的文件是pyscenic中pyscenic grn第一步得到的TF于target的结果
df <- read.csv('sce.adj.csv',header = T)
colnames(df)[3] <- 'Weight'
# rownames(df) = paste(df$TF,df$target,sep = '_')

#我们选择需要的TF去呈现
df_sec <- df[df$TF %in% c("SOX7", "SOX15","TAL1"),]
df_sec <- df_sec[df_sec$Weight >10,] #这里使用Weight筛选下target

#构建网络
gr <- df_sec %>% graph_from_data_frame(directed = T)
#添加一些TF、targrt信息，方便后续数据修饰
V(gr)$type = names(degree(gr))
#定义TF和targrt type
V(gr)$type[V(gr)$type %in% c("SOX7", "SOX15","TAL1")] = 'TF' 
V(gr)$type[V(gr)$type %in% df_sec$target] = 'Target'
V(gr)$size[V(gr)$type =="TF"] = 2
V(gr)$size[V(gr)$type =="Target"] = 1
V(gr)$color	 = 'white'
  

#这里可以调整各种layout布局来展示
#1=======================================================================================
#树的分散形式
p = ggraph(gr, layout = 'sugiyama') + 
  geom_edge_link(aes(color = "#D6404E"), show.legend = F) + 
  geom_node_point(color = 'white')#网络图

#获取网络图数据，添加一些自己需要的信息
pData = p$data
pData = pData[rev(order(pData$type)),]
pData$color[1:3] <- c("#377EB8","#FF7F00", "#4DAF4A")
pData$color[pData$color == "white"] <- 'grey'


#ggplot格式作图，添加上其他内容即可
p + geom_point(data=pData,aes(x,y,color=color,size=size,stroke=1), show.legend = F) + 
  scale_color_manual(values=pData$color) + 
  geom_text(data=subset(pData, type=='Target'),aes(x,y,label=name), 
            size=3,fontface="italic", angle=45, hjust=1)+
  geom_text(data=subset(pData, type=='TF'),aes(x,y,label=name), size=4,fontface="bold")+
  theme_graph()+
  scale_y_discrete(expand=expansion(mult=c(0.5,0.05)))#调整y轴范围，因为有些文字点显示不全
  


#2=======================================================================================
#igraph
p = ggraph(gr, layout = 'fr') + 
  geom_edge_link(aes(color = "#D6404E"), show.legend = F) + 
  geom_node_point(color = 'white')#网络图

#获取网络图数据，添加一些自己需要的信息
pData = p$data
pData = pData[rev(order(pData$type)),]
pData$color[1:3] <- c("#377EB8","#FF7F00", "#4DAF4A")
pData$color[pData$color == "white"] <- 'grey'
  

#ggplot格式作图，添加上其他内容即可
p + geom_point(data=pData,aes(x,y,color=color,size=size,stroke=1), show.legend = F) + 
  scale_color_manual(values=pData$color) + 
  geom_text(data=subset(pData, type=='Target'),aes(x,y,label=name), 
            size=3,fontface="italic")+
  geom_text(data=subset(pData, type=='TF'),aes(x,y,label=name), size=4,fontface="bold")+
  theme_graph()









        