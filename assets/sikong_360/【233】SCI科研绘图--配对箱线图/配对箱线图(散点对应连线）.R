setwd('D:/KS项目/公众号文章/配对箱线图颜色配对')
df <- read.csv('df.csv', header = T)
library(ggplot2)
library(ggpubr)
#1
ggplot(data=df, aes(x = Disease.state, y = Richness,
                    color=Disease.state)) +#病人和对照颜色区分
  geom_boxplot(alpha =0.5,size=1,outlier.shape = NA)+#箱线图，outlier.shape的数值不要显示
  scale_color_manual(limits=c("Patient","Relative"), 
                     values=c("#E29827","#922927"))+#修改color，并对应相关的组
  stat_compare_means(method = "t.test",paired = TRUE, 
                     comparisons=list(c("Patient", "Relative")))+#配对t检验
  geom_jitter(alpha = 0.3,size=3, aes(fill=indi),shape=21)+#抖动点，不同点设置不同的fill，用fill避免与前面的冲突
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.1)))+#让y轴稍微长一点，留出空间标注显著性
  facet_wrap(~sample, scales = "free_y")+#分面
  theme_bw() + 
  theme(panel.grid =element_blank(),
        axis.text = element_text(size = 10,colour = "black"),
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        legend.position = 'top')+
  labs(y='Expression')


#2
ggplot(data=df, aes(x = Disease.state, y = Richness,
                    color=Disease.state)) +
  geom_boxplot(alpha =0.5,size=1,outlier.shape = NA)+
  scale_color_manual(limits=c("Patient","Relative"), 
                     values=c("#E29827","#922927"))+
  stat_compare_means(method = "t.test",paired = TRUE, 
                     comparisons=list(c("Patient", "Relative")))+
  geom_jitter(alpha = 0.3,size=3, aes(fill=indi),shape=21)+
  geom_line(aes(group = Family.ID), 
            color = 'grey40', lwd = 0.5)+
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.1)))+
  facet_wrap(~sample, scales = "free_y")+
  theme_bw() + 
  theme(panel.grid =element_blank(),
        axis.text = element_text(size = 10,colour = "black"),
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        legend.position = 'top')+
  labs(y='Expression')

#3
ggplot(data=df, aes(x = Disease.state, y = Richness,
                    color=Disease.state)) +
  geom_boxplot(alpha =0.5,size=1,outlier.shape = NA)+
  scale_color_manual(limits=c("Patient","Relative"), 
                     values=c("#E29827","#922927"))+
  stat_compare_means(method = "t.test",paired = TRUE, 
                     comparisons=list(c("Patient", "Relative")))+
  geom_jitter(size=3, aes(fill=indi),
              shape=21,position = position_dodge(0.5))+
  geom_line(aes(group = Family.ID), 
            color = 'grey40', lwd = 0.5,position = position_dodge(0.5))+ #添加连线
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.1)))+
  facet_wrap(~sample, scales = "free_y")+
  theme_bw() + 
  theme(panel.grid =element_blank(),
        axis.text = element_text(size = 10,colour = "black"),
        axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.ticks.x = element_blank(),
        legend.position = 'top')+
  labs(y='Expression')
