library(psych)
library(reshape2)
library(tidyverse)
library(magrittr)
library(aplot)

env <- read_tsv("env.xls") %>% column_to_rownames(var="sample")
spe <- read_tsv("spe.xls") %>% column_to_rownames(var="sample")
lm_result <- read_tsv("lm_result.xls")
envdata <- read_tsv("envdata.xls")

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
        axis.ticks= element_blank())+
  guides(fill=guide_colorbar(direction="vertical",reverse=F,barwidth=unit(.5,"cm"),
                             barheight=unit(5,"cm")))

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

