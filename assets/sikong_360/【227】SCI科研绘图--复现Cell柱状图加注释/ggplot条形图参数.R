setwd('E:/生物信息学/复现Cell柱状图加注释')
A <- read.csv('Tumor.CSV',header = T)

library(ggplot2)
library(ggh4x)
A$cellularity <- '' #分组
A$cellularity[which(A$Tumor.cellularity >=15)] = '>=15,SP'
A$cellularity[which(A$Tumor.cellularity <15)] = '<15,LP'


p <- ggplot(A, aes(x=reorder(case_id, -KRAS_VAF), y=KRAS_VAF)) +  # 柱状图，x降序排列
  geom_bar(aes(fill=group), stat='identity') +
  labs(x='Sample ID', y='KRAS VAF') +
  scale_fill_manual(values=c("#309342", "#376CAE", "#1CA4BF", "#D5C643",
                              "#5FBC93", "#D03B23", "#DC7944", "#5DB75E")) +  # 修改fill颜色填充
  theme_bw() +  # ggplot主题
  scale_y_continuous(expand=c(0, 0)) +  # 原点开始坐标，柱子落在x轴上
  theme(panel.grid=element_blank(),
        legend.position.inside = c(0.95, 0.7),  # legend位置坐标调整
        legend.title=element_blank(),  # 去掉legend的title
        axis.text.x=element_text(colour="black", size=6,
                                  angle=90, hjust=-3, vjust=0.1),  # x轴名称及位置坐标调整
        axis.text.y=element_text(colour='black', size=8),  # y轴名称调整
        axis.title.x=element_text(margin=margin(0.5, 1, 0, 1, 'cm'))) +  # x轴标题位置坐标调整
  geom_hline(yintercept=0.075, linetype=2, linewidth=0.5) +  # 添加线条
  annotate(geom='text', label="VAF=0.075", x=102, y=0.12) +  # 添加文字
  geom_segment(aes(x=102, y=0.11, xend=102, yend=0.075),
               arrow=arrow(length=unit(0.2, "cm")))  # 添加箭头


B <- A#重新复制一个文件，用来做分组
B <- B[order(-B$KRAS_VAF),]
library(forcats)
B$case_id <- as.factor(B$case_id)
B$case_id <- fct_inorder(B$case_id)

library(dplyr)
#做一个分组图
Tumor.cellularity <- B$case_id %>% as.data.frame() %>%
  mutate(group=B$cellularity) %>%
  mutate(p="")%>%
  ggplot(aes(p,.,fill=group))+
  geom_tile() + 
  scale_y_discrete(position="right") +
  scale_fill_manual(values = c("#1084A4",
                               "#8D4873"))+
  theme_minimal()+xlab(NULL) + ylab(NULL) +
  theme(axis.text.y = element_blank(),
        axis.text.x =element_blank(),
        axis.ticks.x = element_blank(),
        legend.position = 'none')+
  labs(fill = "Tumor.cellularity")+
  coord_flip()



bottom <- ggplotGrob(Tumor.cellularity)
p+annotation_custom(bottom,xmin=-1,xmax=141.5,ymin=-0.03,ymax=0.01)
#组合，具体位置参数需要慢慢调整






















