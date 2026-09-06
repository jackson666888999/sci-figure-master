library(tidyverse)

df = data.frame()
df = data.frame(matrix(df, nrow=200, ncol=2))
colnames(df) <- c("cluster", "name")
df$cluster <- sample(20, size = nrow(df), replace = TRUE)
df$fruit <- sample(c("banana", "apple", "orange", "kiwi", "plum"), size = nrow(df), replace = TRUE)

df %>% as_tibble() %>% 
  mutate(cluster = factor(cluster, 
                          names(sort(table(fruit == 'apple',cluster)[2,]))),
         fruit = factor(fruit, c('apple', 'kiwi','banana', 
                                 'orange', 'plum'))) %>% 
                                   ggplot(aes(x = cluster, fill = fruit))+
  geom_bar(position = position_stack(reverse = TRUE))+
  scale_y_discrete(expand = c(0,0))+
  labs(y=NULL)+
  coord_flip() +
  ggthemes::theme_wsj() +
  ggthemes::scale_fill_ptol()+
  theme(axis.text.y=element_text(color="black",size=8,margin=margin(r=1)),
        axis.text.x=element_text(color="black",size=9,margin=margin(t=8)),
        axis.title.x = element_text(size=11,margin=margin(t=8),color="black",face="bold"),
        plot.margin=unit(c(0.3,0.3,0.3,0.3),units=,"cm"), 
        panel.background = element_blank(),   # 移除灰色背景框
        axis.line = element_line(color="black"),
        axis.ticks.length.x = unit(-.2, "cm"),
        legend.key = element_blank(),
        legend.background = element_blank(),
        legend.title = element_blank(),
        legend.text=element_text(size=8,color="black"),
        legend.spacing.x=unit(0.1,'cm'),
        legend.key.width=unit(0.4,"cm"),
        legend.key.height=unit(0.4,"cm"))
  



