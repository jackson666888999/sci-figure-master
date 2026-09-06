rm(list=ls())#clear Global Environment
#设置工作目录
setwd('D:\\软件\\夸克云盘\\下载\\PLS-PM')
##载入所需的软件包
library(plspm)
library(vegan)
library(dplyr)
library(ape)
##载入所需的数据表格
otu <- read.table("OTU.txt",header = T,row.names = 1)
env <- read.table("env.txt",header = T,row.names = 1)
env<-env[colnames(otu),]

##在这里，我们取用alpha多样性指数和beta多样性指数PC1，来表征群落的结构，
Shannon <- diversity(otu, index = "shannon", MARGIN = 2, base = exp(1))
Simpson <- diversity(otu, index = "simpson", MARGIN = 2, base =  exp(1))
alpha <- cbind(Shannon,Simpson)

dist <- vegdist(t(otu),method = "bray")
pcoa <- pcoa(dist, correction = "none", rn = NULL)
PC1 = pcoa$vectors[,1]

##合并每个样本点的有效数据
df <- cbind(alpha,env,PC1)
##下面开始我们的模型构建
space <- c(0,1,1,1)
climate <-c(0,0,1,1)
soil <- c(0,0,0,1)
community <- c(0,0,0,0)
path <- cbind(space,climate,soil,community)
rownames(path)<-colnames(path)##建立下三角矩阵
##画出模型的路径图
innerplot(path)

##接下来在潜变量中添加相应的显变量
blocks <- list(
  space = 'Latitude',
  climate = c('Temperature','Precipitation'),
  soil = c('TN','TOC'),
  community = "PC1"
)
blocks##检查各个潜变量的显变量，是否添加成功

##指定因果关系，A表示：下三角矩阵中列是行的因
modes <- rep('A',4)
modes

##运行plspm函数并构建模型
pls <- plspm(df, path, blocks,modes = modes)
pls
pls$outer_model
##初步的模型图可视化
p <- innerplot(pls, colpos = 'red', colneg = 'blue', 
               show.values = TRUE, lcol = 'gray', box.lwd = 0) 

pls$inner_model
pls$inner_summary #用于评价方差解释度，>0.6较好，<0.3较差，其余适中
pls$gof
pls$effects

##我们开始引入metadata，转变数据类型，重新做一遍模型
meta <- read.table("metadata_16S.txt",header = T,row.names = 1)
dat <- cbind(alpha,env,PC1,meta$Group)
colnames(dat)[colnames(dat)=="meta$Group"] <- "Group"
dat$Group <- factor(dat$Group)

##下面开始我们的模型构建
area <- c(0,1,1,1)
climate <-c(0,0,1,1)
soil <- c(0,0,0,1)
community <- c(0,0,0,0)
path1 <- cbind(area,climate,soil,community)
rownames(path1)<-colnames(path1)##建立下三角矩阵
##画出模型的路径图
innerplot(path1)
##把space改为area，放弃原有的纬度指标
blocks1 <- list(
  area = 'Group',
  climate = c('Temperature','Precipitation'),
  soil = c('TN','TOC'),
  community = "PC1"
)
##这时开始设定数据类型scaling，注意一一对应
scaling1 <- list(
  area = 'NOMINAL',##area的Group是定类数据，其余是数值型
  climate = c('NUM','NUM'),
  soil = c('NUM','NUM'),
  community = "NUM"
)
##之后开始重新制作模型
pls1 <- plspm(dat, path=path1, blocks = blocks1,scaling = scaling1,modes = modes)
pls1
pls1$outer_model
##初步的模型图可视化
p1 <- innerplot(pls1, colpos = 'red', colneg = 'blue', 
               show.values = TRUE, lcol = 'gray', box.lwd = 0) 

pls1$inner_model
pls1$inner_summary #用于评价方差解释度，>0.6较好，<0.3较差，其余适中
pls1$gof
pls1$effects

