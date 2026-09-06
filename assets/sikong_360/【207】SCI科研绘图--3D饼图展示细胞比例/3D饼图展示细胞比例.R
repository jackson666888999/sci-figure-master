setwd('D:\\KS项目\\公众号文章\\3D饼图展示细胞比例')

library(Seurat)
library(plotrix)#绘制3D饼图
human_data <- readRDS("D:/KS项目/human_data.rds")

cellratio <- as.data.frame(table(human_data$group, human_data$celltype))
BM <- subset(cellratio, Var1=='BM')
GM <- subset(cellratio, Var1=='GM')
# write.csv(BM, file = "BM.csv")
# write.csv(GM, file = "GM.csv")


#plot
par(mfrow = c(1,2), xpd=TRUE)

pie3D(x=BM$Freq,
      radius=1,#饼图半径
      height=0.1,#饼图高度
      theta=pi/6,#视角
      explode=0,#饼图错位展示
      main="Celltype fraction of BM",#饼图标题
      col=c("#d2981a", "#a53e1f", "#457277", "#8f657d", "#8dcee2"),#分组颜色
      border = "black",#边框线颜色
      shade = 0.5,#图形阴影
      labels=paste0(c(BM$Var2),
                    "\n",
                    round(BM$Freq/sum(BM$Freq) * 100,2), "%"),#图形标签，这里展示了celltype比例，如果你已经设置好标签，那么直接用设置好的即可，不用在计算
      mar=c(2,2,2,3),#饼图周围边距，根据显示文字调整
      labelcol = "black",#标签颜色
      labelcex = 0.8#标签字体大小
)




pie3D(x=GM$Freq,
      radius=1,#饼图半径
      height=0.1,#饼图高度
      theta=pi/6,#视角
      explode=0,#饼图错位展示
      main="Celltype fraction of GM",#饼图标题
      col=c("#d2981a", "#a53e1f", "#457277", "#8f657d", "#8dcee2"),#分组颜色
      border = "black",#边框线颜色
      shade = 0.5,#图形阴影
      labels=paste0(c(GM$Var2),
                    "\n",
                    round(GM$Freq/sum(BM$Freq) * 100,2), "%"),#图形标签，这里展示了celltype比例，如果你已经设置好标签，那么直接用设置好的即可，不用在计算
      mar=c(2,2,2,3),#饼图周围边距，根据显示文字调整
      labelcol = "black",#标签颜色
      labelcex = 0.8#标签字体大小
)


#================================================================================

#调整标签位置
#有时候可能会对默认的位置不满意或者有文字重叠
#可以自行调整下
A = pie3D(x=BM$Freq,
          radius=1,#饼图半径
          height=0.1,#饼图高度
          theta=pi/6,#视角
          explode=0,#饼图错位展示
          main="BM",#饼图标题
          col=c("#d2981a", "#a53e1f", "#457277", "#8f657d", "#8dcee2"),#分组颜色
          border = "black",#边框线颜色
          shade = 0.5,#图形阴影
          labels=paste0(c(BM$Var2),
                        "\n",
                        round(BM$Freq/sum(BM$Freq) * 100,2), "%"),#图形标签，这里展示了celltype比例，如果你已经设置好标签，那么直接用设置好的即可，不用在计算
          mar=c(2,2,2,3),#饼图周围边距，根据显示文字调整
          labelcol = "black",#标签颜色
          labelcex = 0.8#标签字体大小
)

A
# [1] 1.961312 4.319378 5.117877 5.776638 6.158420
#这里面A是一个数字向量，代表的是最大面积那个扇形开始
#逆时针顺序。比如在我们演示的这个数据中，Mast是最后一个，也就是A[5],
#它和Neutro离的太近了，调整下。直接修改A向量的数字即可
#想要修改哪个就修改哪个

A[5] <- 6.5

#最后增加一个参数labelpos
pie3D(x=BM$Freq,
      labelpos=A,
      radius=1,#饼图半径
      height=0.1,#饼图高度
      theta=pi/6,#视角
      explode=0,#饼图错位展示
      main="BM",#饼图标题
      col=c("#d2981a", "#a53e1f", "#457277", "#8f657d", "#8dcee2"),#分组颜色
      border = "black",#边框线颜色
      shade = 0.5,#图形阴影
      labels=paste0(c(BM$Var2),
                    "\n",
                    round(BM$Freq/sum(BM$Freq) * 100,2), "%"),#图形标签，这里展示了celltype比例，如果你已经设置好标签，那么直接用设置好的即可，不用在计算
      mar=c(2,2,2,3),#饼图周围边距，根据显示文字调整
      labelcol = "black",#标签颜色
      labelcex = 0.8#标签字体大小
)


#================================================================================
#如果想要各个扇形错位，调整explode即可
pie3D(x=BM$Freq,
      labelpos=A,
      radius=1,#饼图半径
      height=0.1,#饼图高度
      theta=pi/6,#视角
      explode=0.1,#饼图错位展示
      main="BM",#饼图标题
      col=c("#d2981a", "#a53e1f", "#457277", "#8f657d", "#8dcee2"),#分组颜色
      border = "black",#边框线颜色
      shade = 0.5,#图形阴影
      labels=paste0(c(BM$Var2),
                    "\n",
                    round(BM$Freq/sum(BM$Freq) * 100,2), "%"),#图形标签，这里展示了celltype比例，如果你已经设置好标签，那么直接用设置好的即可，不用在计算
      mar=c(2,2,2,3),#饼图周围边距，根据显示文字调整
      labelcol = "black",#标签颜色
      labelcex = 0.8#标签字体大小
)

