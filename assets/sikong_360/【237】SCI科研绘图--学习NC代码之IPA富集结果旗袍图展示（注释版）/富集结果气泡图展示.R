
setwd('D:\\KS项目\\公众号文章\\学习SCI论文代码-富集气泡图展示')

library(stringi)
library(tidyr)
library(colorspace)
library(ggplot2)
library(stringr)

#read data
IPA_Z <- read_excel("ipa.xls",skip=1, sheet = 1, col_names=F)
IPA_P <- read_excel("ipa.xls",skip=1, sheet = 2, col_names=F)


#这里遇到第一个问题，发现列名没有了，可能原因是xls文件设置的原因，先不管了
#后来想着两个文件分别保存为csv文件读取好了，结果因为通路有希腊字母，总是显示乱码
#不论添加encoding参数也没有用。后来发现是另存的时候没有选择uft-8，所以要注意

ipa_p <- read.csv("ipa.csv", header = T)
colnames(IPA_Z) <- colnames(ipa_p)
colnames(IPA_P) <- colnames(ipa_p)


# 替换字符：replace Greek symbols,把希腊字母换成英文
#其实替换与否都不重要，主要是学习一下代码
Greek <- c("α","β","γ","κ","θ")
English <- c("a","b","r","k","th")
IPA_Z$Canonical.Pathways <- stri_replace_all_regex(IPA_Z$Canonical.Pathways,
                                                     pattern=Greek,
                                                     replacement = English,
                                                     vectorize=F)
IPA_P$Canonical.Pathways <- stri_replace_all_regex(IPA_P$Canonical.Pathways,
                                                     pattern=Greek,
                                                     replacement = English,
                                                     vectorize=F)



# Order data frame rows according to vector with specific order
#如果你打开两个文件比对一下，很快就会发现，两者的通路排列是不一样的
#最好统一一下，以便于后面文件合并以及其他处理

#这里使用match函数，就很方便了，总之统一通路位置
IPA_P<-IPA_P[match(IPA_Z$Canonical.Pathways,IPA_P$Canonical.Pathways),]

#后面我们需要使用ggplot2作图，需要长数据格式，现在的数据格式是宽数据（pheatmap做热图用现在的数据格式即可）
#下面这句代码的意思你可以通俗地理解为，我们需要固定一列通路，然后将后面的列转化
#行转化为"Cell_types"列，数值转化为"Zscore"列，这样就变成了3列的数据了，对应通路与细胞以及数值
IPA_Z <- pivot_longer(IPA_Z, cols= 2:21,names_to = "Cell_types",values_to = "Zscore")
IPA_P <- pivot_longer(IPA_P, cols= 2:21,names_to = "Cell_types",values_to = "-log(P)")
#合并数据，因为两者顺序一致，所以直接cbind即可，
IPA_Z <- cbind(IPA_Z,`-log(P)`=IPA_P$`-log(P)`)


#字符处理
# trim the name of cell types
IPA_Z$Cell_types<- gsub("_uGvs1G.*","",IPA_Z$Cell_types)#将_uGvs1G.*及其后面的字符替换掉
#这里就涉及到很多人经常问到的问题，在画图的时候想要调整细胞或者通路顺序
#使用factor即可。levels里面设置向量。
IPA_Z$Cell_types<-factor(IPA_Z$Cell_types, levels = unique(IPA_Z$Cell_types)) # order the x axis

#替换数据，在excel中，有些数值是N/A，替换为NA或者其他数值
# Replacing character values with NA in a data frame
IPA_Z[ IPA_Z == "N/A" ] <- NA
IPA_Z$Zscore <- as.numeric(IPA_Z$Zscore)


#作图
#数据过滤，把p值不显著的过滤掉，使用filter函数
#需要注意一下，有些小伙伴使用filter会莫名其妙出现错误，。。。object找不到
#记得加载dplyr包就没有问题了
library(dplyr)
data  = IPA_Z %>%  filter(`-log(P)`>1.3)


#plot
ggplot(data=data, aes(x=Cell_types, y = Canonical.Pathways, 
                      color = Zscore, size = `-log(P)`)) + #设置变量，xy轴，大小颜色
  geom_point() + #点图展示
  scale_y_discrete(labels=function(y) str_wrap(y, width=80)) + #这里是一个比较新的内容，
  #在富集分析的dotplot中有时候通路太长会把文字换行展示，这里起到的就是这个作用
  #labels=function(y) str_wrap(y, width=80)定义了一个函数，该函数使用stringr包的str_wrap()函数来自动换行标签文本，确保每行不超过80个字符宽。
  #字符长短按照自己实际需求设定
  ylab('Canonical Pathways') + #y轴标签
  cowplot::theme_cowplot() +#主题
  theme(axis.text.x = element_text(size=9.5, angle=45, vjust = 1, hjust = 1),#x轴文字大小、角度、位置调整
        axis.text.y = element_text(size=7.5))+#y轴文字大小调整
  theme(axis.line  = element_blank()) + #不要坐标轴线
  theme(axis.ticks = element_blank()) + #不要坐标轴ticks
  scale_color_continuous_divergingx('RdBu',rev=T,limits = c(-3,3), 
                                    oob = scales::squish, name = 'z-score',
                                    na.value="transparent") + #颜色修改
  labs(size="-log10(adj.P)") #legend中size的标题



#最后保存图片，设置长宽
ggsave("IPA.pdf", width = 10, height = 9,limitsize = FALSE)












