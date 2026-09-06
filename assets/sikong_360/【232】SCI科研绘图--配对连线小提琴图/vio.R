
BiocManager::install("vioplot")
library(vioplot)
library(dplyr)
setwd("D:/KS科研分享与服务_公众号文章/vioplot配对连线小提琴图")
df <- read.csv("df.csv", header = T)

###添加颜色
cols <- data.frame(Disease.state=c('Patient','Relative'),
                   color = c('#E69F00', "#55B4EA"))
df_merge <- full_join(df, cols, by = "Disease.state")

# colnames(df)
# [1] "sample.id"     "DonorID"       "Family.ID"     "Disease.state" "Richness"  


####产生随机数，用于后期抖动点设置
df_merge$dummy <- 1
df_merge$dummy[df_merge$Disease.state != "Patient" ] <- 2
df_merge$dummy  <- df_merge$dummy + sample(-100 : 100, nrow(df_merge), replace = T)/2000


#提取数据
var.pat <- df$Richness[df$Disease.state == "Patient"]
var.rel <- df$Richness[df$Disease.state == "Relative"]

#做基本小提琴图
vioplot(var.pat,  var.rel, drawRect = F,
        names = c("Patients", "Relatives"),
        col=unique(df_merge$color),
        ylim = c(0,240))

#添加网格线
# grid(NULL, lty = 6, col = "grey", nx=10)


#添加中值
segments(.7, mean(var.pat),1.3, mean(var.pat), lwd = 2)
segments(1.7, mean(var.rel), 2.3, mean(var.rel), lwd = 2)


###接下来就考虑连线和添加点
map.pat <- df_merge[df_merge$Disease.state == "Patient", ]
map.rel <- df_merge[df_merge$Disease.state == "Relative", ]
families <- sort(unique(df_merge$Family.ID))

for(i in 1: length(families)){
  #分别获取两个分组数据
  map.pat.i <- map.pat[map.pat$Family.ID ==  families[i], ]
  map.rel.i <- map.rel[map.rel$Family.ID ==  families[i], ]
  #获取分组每个ID在不同组中的值
  var.pat.i <- var.pat[map.pat$Family.ID ==  families[i] ]
  var.rel.i <- var.rel[map.rel$Family.ID ==  families[i] ]
  
  segments(y0 = var.pat.i,  x0 =  map.pat.i$dummy,
                 y1 =  var.rel.i, x1 =  map.rel.i$dummy,
                 col = 8)

  points(map.pat.i$dummy, var.pat.i, pch = 21, bg = 8)
  points(map.rel.i$dummy, var.rel.i, pch = 21, bg = 8)
  
}


title(ylab ="Richness", cex=1.5)
#显著性检验
res <- t.test(df_merge$Richness ~ df_merge$Disease.state, paired = T)
res
segments(1, 210,2,210, lwd = 2)
text(x=1.5, y=220, labels="Pvalue = 8.324e-09")









