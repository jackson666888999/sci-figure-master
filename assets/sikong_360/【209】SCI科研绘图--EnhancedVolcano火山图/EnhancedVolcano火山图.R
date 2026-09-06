
library(EnhancedVolcano)
setwd("D:/KS项目/公众号文章/新的火山图")
df <- read.csv("DEGs_trans.csv", header = T)
#根据设置颜色
keyvals <- ifelse(
  df$log2FoldChange < -2 & df$pvalue < 0.01, 'royalblue3',
  ifelse(df$log2FoldChange > 2 & df$pvalue <0.01, 'red3','grey87'))
keyvals[is.na(keyvals)] <- 'grey87'
names(keyvals)[keyvals == 'red3'] <- 'Up'
names(keyvals)[keyvals == 'grey87'] <- 'nosig'
names(keyvals)[keyvals == 'royalblue3'] <- 'down'

EnhancedVolcano(df,#差异文件
                lab = df$gene,#标记基因
                legendPosition = 'none',#不要legend
                x = 'log2FoldChange',
                y = 'pvalue',
                subtitle = NULL,#副标题
                title = "Female vs Male DEGs",#标题
                # ylim = c(0, 50),#y轴范围
                # xlim = c(-0.5, 0.5),#x轴范围
                axisLabSize = 12,#坐标轴标记文字大小
                FCcutoff = 2, #FC阈值
                pCutoff = 0.01,#p阈值
                # pointSize = c(ifelse(abs(df$log2FoldChange)>5 & df$pvalue<0.01, 3, 1)),#突出标记一些点
                labSize = 4,#标记文字大小
                colCustom = keyvals,#颜色
                colAlpha = 0.8,#点不透明度
                gridlines.major = F, 
                gridlines.minor = F,
                border = 'full', #以下都是边框设置
                borderWidth = 0.5, 
                borderColour = 'black')







