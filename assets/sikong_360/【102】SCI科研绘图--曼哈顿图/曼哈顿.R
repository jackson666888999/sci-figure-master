#---------------------------------------------------------------------#
#---可开发票---可开发票---可开发票---可开发票---可开发票---可开发票---#
#---关注B站：R语言分析作图--------------------------------------------#
#---关注公众号：R语言分析作图-----------------------------------------#
#---关注小红书：R语言分析作图-----------------------------------------#
#---论文、商业合作加微信：STRBiotech----------------------------------#
#---任何辅导、代做等付费内容都可开发票以供科研经费报销----------------#
#---私人辅导、代做、系统性GEO\TCGA等数据挖掘课程加微信：STRBiotech----#
#---------------------------------------------------------------------#

#引用本次要用的包
library(ggplot2)

#加载我们的数据
dat <- read.csv("result.csv")
#将每个otu分为上调、下调以及不显著 根据P<0.05 和 LogFC是否大于1 以及是否小于-1 来决定
dat$change <- ifelse(dat$P.Value < 0.05 & abs(dat$logFC)>1, ifelse(dat$logFC<0 ,"depleted","enriched"),"nosig")
#将p值取一下负对数，方便显示
dat$P.Value <- -log(dat$P.Value)

p <- ggplot(dat, aes(Phylum, P.Value))+#添加数据
  geom_jitter(aes(color =  Phylum, shape = change, size = logFC),width = 0.5)+#添加抖动的点，颜色根据门水平，形状根据change 大小根据LogFC
  scale_y_continuous(expand = c(0,0),limits = c(0,30))+#更改y轴范围
  scale_size_continuous(range = c(1,3.5))+#更改点的大小极值
  scale_shape_manual(values = c(6,17,16))+#更改形状
  scale_color_manual(values = c("#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#2878b5","#9ac9db"))+#更改颜色
  geom_hline(yintercept = -log(0.05), size = 0.5, linetype = "dashed", color = "red")+
  labs(x = "", y = "-Log(Pvalue)")+
  theme_classic()+ #更改主题
  theme(legend.position = "top")#更改图例位置  也可以是 left bottom right top  none  c(0.8,0.8)
p  

ggsave("曼哈顿图.pdf", p, width = 7, height = 4.5)  

  