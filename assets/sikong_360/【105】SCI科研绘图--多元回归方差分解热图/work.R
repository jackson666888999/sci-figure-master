library(psych)
library(reshape2)
library(tidyverse)
library(magrittr)
library(relaimpo)
library(MASS)
library(aplot)

#读取环境变量和物种丰度矩阵
env <- read_tsv("env.xls") %>% column_to_rownames(var="sample")
spe <- read_tsv("spe.xls") %>% column_to_rownames(var="sample")

# 构建空白数据框
metdata <- data.frame()
envdata <- data.frame()

# 循环计算环境变量和物种丰度的多元线性回归和方差分解
for (i in colnames(spe)){
  spe_name <- i
  env_spe <- cbind(env, spe[spe_name])
  colnames(env_spe)[ncol(env_spe)] <- 'spe'
  # 使用lm()，分别拟合所有环境变量与物种丰度的多元线性回归
  fit <- lm(spe~., data = env_spe)
#  stepAIC()执行后向选择以减少环境变量降低共线性并尽量保证解释率，获取最优模型
  fit_simple <- stepAIC(fit, direction = 'backward')
  crf <- calc.relimp(fit_simple,rela=FALSE)
  env_improtance <- crf$lmg %>% as.data.frame() %>% 
    rownames_to_column(var="env") %>% 
    mutate(spe=i) %>% set_colnames(c("env","importance","spe"))
  
  envdata <- rbind(envdata,env_improtance)
  
  lm_stat <- summary(fit_simple)
  lm_stat$r.squared   #提取回归的原始 R2
  radj <- lm_stat$adj.r.squared  # 矫正好的R2
  F <- lm_stat$fstatistic 
  pvalue <- pf(F[1], F[2], F[3], lower.tail = FALSE) #获取回归的 p 值
  metdata[i,1]= radj
  metdata[i,2]= pvalue
}

# 数据整合
lm_result <- metdata %>% as.data.frame() %>% 
  rownames_to_column(var="id") %>% set_colnames(c("id","radj","pvalue")) %>% 
  mutate(p_signif=symnum(pvalue, corr = FALSE, na = FALSE,  
                         cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1), 
                         symbols = c("***", "**", "*", "", " ")))


# 相关性分析
spearman <- corr.test(env, spe, method = 'spearman', adjust = 'none')


p1 <- melt(spearman$r) %>% mutate(pvalue=melt(spearman$p.adj)[,3],
                                  p_signif=symnum(pvalue, corr = FALSE, na = FALSE,  
                                                  cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1), 
                                                  symbols = c("***", "**", "*", "", " "))) %>% 
  set_colnames(c("env","spe","r","p","p_signif")) %>% 
  ggplot(.,aes(spe,env))+
  geom_tile(aes(fill=r))+
  geom_text(aes(label=p_signif),size=3,color="white",hjust=0.5,vjust=0.7)+
  geom_point(data = envdata,aes(x = spe, y = env,size = importance*100),shape=21) +
  scale_size_continuous(range = c(0,8)) +
  labs(x = NULL,y = NULL,color=NULL,fill=NULL,size = 'Importance (%)')+
  scale_color_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11,"RdBu")))+
  scale_x_discrete(expand=c(0,0))+
  scale_y_discrete(expand=c(0,0),position = 'left') +
  theme(axis.text.x=element_text(angle =50,hjust =1,vjust =1,color="black",size = 10),
        axis.text.y=element_text(color="black",size =10),
        axis.ticks= element_blank(),
        legend.background = element_blank(),
        legend.key = element_blank())

p2 <- ggplot(lm_result,aes(id,radj*100,label=p_signif))+
  geom_col(fill = '#4882B2',width = 0.6)+
  geom_text(aes(label=p_signif),size=5,color="black",hjust=0.5,vjust=0.5)+
  labs(title = 'Explained variation (%)',x=NULL,y=NULL)+
  theme(panel.grid = element_blank(), panel.background = element_blank(), 
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        title=element_text(size=8,color="black"),
        axis.text.y = element_text(color = 'black'), 
        axis.line = element_line(color = 'black'),axis.ticks = element_line(color = 'black')) +
  scale_y_continuous(expand = c(0,0.5),limits = c(0,100))

p1 %>% insert_top(p2,height = 0.2)

