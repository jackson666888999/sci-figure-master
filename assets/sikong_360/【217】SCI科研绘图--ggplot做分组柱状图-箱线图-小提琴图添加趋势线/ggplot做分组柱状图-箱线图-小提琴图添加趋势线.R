
setwd('D:\\KS项目\\公众号文章\\ggplot作图添加趋势线')

library(RColorBrewer)
library(ggpubr)
library(ggplot2)
library(cowplot)

#读入表达数据，这是一个完整的数据
Exp <- read.csv("Exp.csv",header=T,row.names=1)
gene <- c("CD28","CD3D","CD8A","LCK",
          "GATA3","EOMES","IL23A","CXCL8",
          "IL1R2","IL1R1","MMP8","MMP9")#我们只需要部分基因演示
Exp <- log2(Exp+1) #因为是FPKM数据，标准化一下
Exp_plot <- Exp[,gene]#提取需要作图得基因表达信息


#加载样本信息，分组信息，每个分组有多个重复
info <- read.csv("info.csv",header=T)
Exp_plot<- Exp_plot[info$Sample,]
Exp_plot$sam=info$Type
Exp_plot$sam <- factor(Exp_plot$sam,
                       levels=c("Asymptomatic",
                                "Mild",
                                "Severe",
                                "Critical"))#固定分组顺序


col <-c("#5CB85C","#337AB7","#F0AD4E","#D9534F")

#小提琴图------------------------------------------------------------------------
plist2<-list()
for (i in 1:length(gene)) {
  
  df<-Exp_plot[,c(gene[i],"sam")]#循环提取每个基因表达信息
  colnames(df)<-c("Expression","sam")#统一命名
  my_comparisons1 <- list(c("Asymptomatic", "Mild")) #设置比较组
  my_comparisons2 <- list(c("Asymptomatic", "Severe"))#设置比较组
  my_comparisons3 <- list(c("Asymptomatic", "Critical"))#设置比较组
  my_comparisons4 <- list(c("Mild", "Severe"))#设置比较组
  my_comparisons5 <- list(c("Mild", "Critical"))#设置比较组
  my_comparisons6 <- list(c("Severe", "Critical"))#设置比较组
  
  
  p = ggplot(df, 
         aes(x=sam, y=Expression)) + 
    geom_point(color='#bbbdbf', position = 'jitter') + #设置散点，颜色以及抖动点
    geom_violin(notch = F, outlier.colour = NA, 
                mapping = aes(fill=as.factor(sam)))+#小提琴图
    geom_smooth(data = df, 
                mapping = aes(x=as.numeric(sam), y=Expression), 
                color='red', se = F, method = 'lm')+#添加拟合线， method = 'lm'，线性
    scale_fill_manual(values = col)+
    theme(axis.line=element_line(colour="black"),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_text(size = 15,angle = 45,vjust = 1,hjust = 1),
          axis.text.y = element_text(size = 15),
          plot.title = element_text(hjust = 0.5,size=15,face="bold"),
          legend.position = "NA")+
    ggtitle(gene[i])+
    stat_compare_means(method="t.test",hide.ns = F,
                       comparisons =c(my_comparisons1,my_comparisons2,my_comparisons3,my_comparisons4,my_comparisons5,my_comparisons6),
                       label="p.signif")
  
  plist2[[i]]<-p
  
}

#cowplot拼图。
plot_grid(plist2[[1]],plist2[[2]],plist2[[3]],
           plist2[[4]],plist2[[5]],plist2[[6]],
           plist2[[7]],plist2[[8]],plist2[[9]],
           plist2[[10]],plist2[[11]],plist2[[12]],ncol=4)



#小提琴图+箱线图--------------------------------------------------------------
plist3<-list()

for (i in 1:length(gene)) {
  
  df<-Exp_plot[,c(gene[i],"sam")]#循环提取每个基因表达信息
  colnames(df)<-c("Expression","sam")#统一命名
  my_comparisons1 <- list(c("Asymptomatic", "Mild")) #设置比较组
  my_comparisons2 <- list(c("Asymptomatic", "Severe"))#设置比较组
  my_comparisons3 <- list(c("Asymptomatic", "Critical"))#设置比较组
  my_comparisons4 <- list(c("Mild", "Severe"))#设置比较组
  my_comparisons5 <- list(c("Mild", "Critical"))#设置比较组
  my_comparisons6 <- list(c("Severe", "Critical"))#设置比较组
  
  
  p = ggplot(df, aes(x=sam, y=Expression)) + 
    geom_point(color='#bbbdbf', position = 'jitter') +
    geom_violin(notch = F, outlier.colour = NA, 
                mapping = aes(fill=as.factor(sam))) +
    geom_boxplot(mapping = aes(fill=as.factor(sam)), width=0.2)+#添加箱式图
    geom_smooth(data = df, 
                mapping = aes(x=as.numeric(sam), y=Expression), 
                color='red', se = F, method = 'lm')+
    scale_fill_manual(values = col)+
    theme(axis.line=element_line(colour="black"),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_text(size = 15,angle = 45,vjust = 1,hjust = 1),
          axis.text.y = element_text(size = 15),
          plot.title = element_text(hjust = 0.5,size=15,face="bold"),
          legend.position = "NA")+
    ggtitle(gene[i])+
    stat_compare_means(method="t.test",hide.ns = F,
                       comparisons =c(my_comparisons1,my_comparisons2,my_comparisons3,my_comparisons4,my_comparisons5,my_comparisons6),
                       label="p.signif")
  
  plist3[[i]]<-p
  
}


plot_grid(plist3[[1]],plist3[[2]],plist3[[3]],
          plist3[[4]],plist3[[5]],plist3[[6]],
          plist3[[7]],plist3[[8]],plist3[[9]],
          plist3[[10]],plist3[[11]],plist3[[12]],ncol=4)





#小提琴图+箱线图+曲线拟合----------------------------------------------------------
plist4<-list()

for (i in 1:length(gene)) {
  
  df<-Exp_plot[,c(gene[i],"sam")]#循环提取每个基因表达信息
  colnames(df)<-c("Expression","sam")#统一命名
  my_comparisons1 <- list(c("Asymptomatic", "Mild")) #设置比较组
  my_comparisons2 <- list(c("Asymptomatic", "Severe"))#设置比较组
  my_comparisons3 <- list(c("Asymptomatic", "Critical"))#设置比较组
  my_comparisons4 <- list(c("Mild", "Severe"))#设置比较组
  my_comparisons5 <- list(c("Mild", "Critical"))#设置比较组
  my_comparisons6 <- list(c("Severe", "Critical"))#设置比较组
  
  
  p = ggplot(df, aes(x=sam, y=Expression)) + 
    geom_point(color='#bbbdbf', position = 'jitter') +
    geom_violin(notch = F, outlier.colour = NA, 
                mapping = aes(fill=as.factor(sam))) +
    geom_boxplot(mapping = aes(fill=as.factor(sam)), width=0.2)+
    geom_smooth(data = df, 
                mapping = aes(x=as.numeric(sam), y=Expression), 
                color='red', se = F, method = 'loess')+ #修改拟合方法，曲线趋势拟合
    scale_fill_manual(values = col)+
    theme(axis.line=element_line(colour="black"),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_text(size = 15,angle = 45,vjust = 1,hjust = 1),
          axis.text.y = element_text(size = 15),
          plot.title = element_text(hjust = 0.5,size=15,face="bold"),
          legend.position = "NA")+
    ggtitle(gene[i])+
    stat_compare_means(method="t.test",hide.ns = F,
                       comparisons =c(my_comparisons1,my_comparisons2,my_comparisons3,my_comparisons4,my_comparisons5,my_comparisons6),
                       label="p.signif")
  
  plist4[[i]]<-p
  
}


plot_grid(plist4[[1]],plist4[[2]],plist4[[3]],
          plist4[[4]],plist4[[5]],plist4[[6]],
          plist4[[7]],plist4[[8]],plist4[[9]],
          plist4[[10]],plist4[[11]],plist4[[12]],ncol=4)



#柱状图+散点图+拟合----------------------------------------------------------------
plist5<-list()

for (i in 1:length(gene)) {
  
  df<-Exp_plot[,c(gene[i],"sam")]#循环提取每个基因表达信息
  colnames(df)<-c("Expression","sam")#统一命名
  my_comparisons1 <- list(c("Asymptomatic", "Mild")) #设置比较组
  my_comparisons2 <- list(c("Asymptomatic", "Severe"))#设置比较组
  my_comparisons3 <- list(c("Asymptomatic", "Critical"))#设置比较组
  my_comparisons4 <- list(c("Mild", "Severe"))#设置比较组
  my_comparisons5 <- list(c("Mild", "Critical"))#设置比较组
  my_comparisons6 <- list(c("Severe", "Critical"))#设置比较组
  
  
  p = ggplot(df, aes(x=sam, y=Expression)) + 
    geom_bar(width = 0.5, aes(fill=sam), stat = 'summary')+ #柱状图
    geom_point(color='#bbbdbf', position = 'jitter') +
    geom_smooth(data = df, 
                mapping = aes(x=as.numeric(sam), y=Expression), 
                color='red', se = F, method = 'lm')+
    scale_fill_manual(values = col)+
    theme(axis.line=element_line(colour="black"),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_text(size = 15,angle = 45,vjust = 1,hjust = 1),
          axis.text.y = element_text(size = 15),
          plot.title = element_text(hjust = 0.5,size=15,face="bold"),
          legend.position = "NA")+
    ggtitle(gene[i])+
    stat_compare_means(method="t.test",hide.ns = F,
                       comparisons =c(my_comparisons1,my_comparisons2,my_comparisons3,my_comparisons4,my_comparisons5,my_comparisons6),
                       label="p.signif")
  
  plist5[[i]]<-p
  
}


plot_grid(plist5[[1]],plist5[[2]],plist5[[3]],
          plist5[[4]],plist5[[5]],plist5[[6]],
          plist5[[7]],plist5[[8]],plist5[[9]],
          plist5[[10]],plist5[[11]],plist5[[12]],ncol=4)













