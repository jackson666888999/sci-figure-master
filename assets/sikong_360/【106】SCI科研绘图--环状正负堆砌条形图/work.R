library(tidyverse)

data1 <- mtcars %>% head(6) %>% 
  mutate_if(is.numeric, function(x) x+10) %>% 
  log10() %>% as.data.frame() %>% 
  rownames_to_column("type") %>%
  pivot_longer(-type) %>%
  mutate(type=factor(type)) %>% arrange(type)

empty_bar <- 0
data1$id <- seq(1,nrow(data1))
label_data <- data1
number_of_bar <- nrow(label_data)
angle <-  90 - 360 * (label_data$id-0.5) /number_of_bar    
label_data$hjust<-ifelse( angle < -90, 1, 0)
label_data$angle<-ifelse(angle < -90, angle+180, angle)


colors <-c("#FED439FF","#709AE1FF",
           "#D5E4A2FF","#197EC0FF","#F05C3BFF","#46732EFF",
           "#71D0F5FF","#370335FF","#075149FF","#C80813FF","#91331FFF",
           "#1A9993FF","#FD8CC1FF")

data1 %>% bind_rows(data1 %>% mutate(value=-value)) %>% 
ggplot(.,aes(id,value,fill=name))+
  geom_bar(stat="identity",alpha=0.8)+
  scale_fill_manual(values = colors)+
  labs(x=NULL,y=NULL)+
  ylim(-7,10)+
  coord_polar(start =0)+
  theme_void()+
  theme(
    legend.text = element_text(color="black"),
    legend.title=element_blank(),
    legend.spacing.x=unit(0.2,'cm'),
    legend.key=element_blank(),
    legend.key.width=unit(0.3,'cm'),
    legend.key.height=unit(0.3,'cm'),
    legend.position=c(0.5,0.5))+
  # 添加标签
  geom_text(data=label_data,aes(x=id, y=value+1,label=type,hjust=hjust),
            fontface="plain",size=2.5,show.legend = F,color="black",
            angle= label_data$angle,inherit.aes = FALSE)+
  scale_color_manual(values = colors)+
  # 添加外圈
  geom_segment(aes(x=0, y=8,xend=66.5,yend =8),size=1.5,color="#3B9AB2",
               arrow = arrow(length = unit(0, "npc"),type="closed"))+
  geom_segment(aes(x=0, y=-0.1,xend=66.5,yend =-0.1),size=0.3,color="black",
               arrow = arrow(length = unit(0, "npc"),type="closed"))


