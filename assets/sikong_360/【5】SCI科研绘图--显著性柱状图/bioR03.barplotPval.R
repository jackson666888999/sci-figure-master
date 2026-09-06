


library(ggplot2)          #引用包
inputFile="input.txt"     #输入
outFile="barplot.pdf"     #输出
setwd("D:\\biowolf\\bioR\\03.barplotPval")          #工作目录
rt = read.table(inputFile, header=T, sep="\t", check.names=F)     #读取

#????按FDR排序
labels=rt[order(rt$FDR,decreasing =T),"Term"]
rt$Term = factor(rt$Term,levels=labels)

#绘制
p=ggplot(data=rt)+geom_bar(aes(x=Term, y=Count, fill=FDR), stat='identity')+
    coord_flip() + scale_fill_gradient(low="red", high = "blue")+ 
    xlab("Term") + ylab("Gene count") + 
    theme(axis.text.x=element_text(color="black", size=10),axis.text.y=element_text(color="black", size=10)) + 
    scale_y_continuous(expand=c(0, 0)) + scale_x_discrete(expand=c(0,0))+
    theme_bw()
ggsave(outFile,width=7,height=5)      #保存图片


