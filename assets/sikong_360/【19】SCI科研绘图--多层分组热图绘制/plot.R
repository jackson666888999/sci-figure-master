library(tidyverse)
library(ggh4x)
library(MetBrewer)

df <- read_tsv("data.tsv") %>% pivot_longer(-gene) %>% 
  extract(col = name, into ="group1",regex = "([^\\s]+).*",remove = FALSE) %>% 
  mutate(group1=case_when(group1=="Basal" ~ "Bas",
                         group1=="Luminal" ~ "Lum")) %>% 
  mutate(group2 = case_when(
    grepl("1-.", name) ~ "Bio rep 1",
    grepl("2-.", name) ~ "Bio rep 2",
    grepl("3-.", name) ~ "Bio rep 3",
    TRUE ~ "Other"
  ))

df$gene <- factor(df$gene,levels = df$gene %>% unique() %>% rev())
  
df %>% 
  ggplot(.,aes(interaction(name,group1),gene,color=value,fill=value))+
  geom_tile()+
  geom_point(data=df %>% filter(is.na(value)),shape=4,size=4,color="black")+
  facet_grid(.~group2,scales = "free_x",switch = "x")+
  guides(x="axis_nested")+
  scale_x_discrete(expand=c(0,0),position = 'top')+
  scale_y_discrete(expand=c(0,0))+
  scale_fill_gradientn(colors=met.brewer("Cassatt1"),na.value = NA)+
  scale_color_gradientn(colors=met.brewer("Cassatt1"),na.value = NA)+
  labs(x=NULL,y=NULL,fill="Row \n z-score",color="Row \n z-score") +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_text(color="black",size=8,face="italic"),
        axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank(),
        strip.background = element_blank(),
        strip.text = element_text(color="black",size=9,face="bold"),
        panel.background = element_blank(),
        plot.background = element_blank(),
        legend.spacing.x = unit(0.1,"cm"),
        panel.spacing.x =unit(0.01,"cm"),
        panel.border=element_rect(fill=NA,color="black",size=0.5,linetype="solid"),
        ggh4x.axis.nestline.x = element_line(size=0.5,color="black"),
        ggh4x.axis.nesttext.x = element_text(colour ="black",angle=0,size=10,vjust=0,hjust=0.5,face="bold",
                                             margin = margin(b=3)),
        plot.margin=unit(c(0.2,0.2,0.2,0.2),units=,"cm"))
  

