#


#install.packages("fmsb")
library(fmsb)             
inputFile="input.txt"     
outFile="radar.pdf"       
col="red"                 #定义颜色
  setwd("G:/R模板/R语言绘制50个SCI图的输入文件及代码/R语言绘制50个SCI图的输入文件及代码/26雷达图")     

data <- read.csv("G:/R模板/R语言绘制50个SCI图的输入文件及代码/R语言绘制50个SCI图的输入文件及代码/26雷达图/input.csv", header = T, row.names = 1)
data=as.data.frame(t(data))       #转置
maxValue=ceiling(max(47000)*10)/10  #设置刻度
data=rbind(rep(maxValue,ncol(data)),rep(-maxValue,ncol(data)),data)

#输出结果
#pdf(file=outFile,height=7,width=7)
radarchart( data, axistype=1, 
            pcol=col,                    #线条颜色
            plwd=2 ,                     #线条粗细
            plty=1,                      #虚线，实线
            cglcol="grey",               #背景线条颜色
            cglty=1,                     #背景线条虚线，实线1
            caxislabels=seq(0,47000,2400),    #坐标刻度
            cglwd=1.2,                   #背景线条粗细
            axislabcol="blue",           #刻度颜色
            vlcex=0.8                    #字体大小
)
#dev.off()



