library(tidyverse)
library(gapminder)
library(patchwork)
library(ggbeeswarm)
library(ggsci)
library(multcompView)
library(magrittr)




data <- read_tsv("data.txt") %>% filter(continent !="Oceania") %>% 
  select(2,3,4)

make_plot <- function(data) {
  plot <- ggplot(data,aes(x=continent,y=lifeExp.x,fill=continent))+
    geom_violin(scale = "width", width = 0.8) +
    geom_quasirandom(aes(colour =continent ),size = 0.5) +
    geom_text(aes(label=Tukey,y=lifeExp.y+3))+
    labs(x=NULL,y=NULL,title = unique(data$year))+
    scale_fill_aaas()+
    scale_color_npg()+
    theme(legend.position = "non",
          plot.title = element_text(hjust = 0.5,vjust=0.5,color = "black",face="bold",
                                    size=10),
          panel.background = element_blank(),
          axis.line = element_line(color="black"),
          axis.line.x.top  = element_line(color="black"), 
          axis.text.x.top = element_blank(),
          axis.ticks.y.right=element_blank(),
          axis.text.y.right = element_blank(),
          axis.ticks.x.top=element_blank(),
          axis.text.y=element_text(color="black",size=6,face="bold"),
          axis.text.x = element_text(color="black",size=6,face="bold"))+
    guides(x.sec="axis",y.sec = "axis")
    
  return(plot)
}


p <- split(data,list(data$year))
aov_data <- data.frame()

for(i in 1:12) {
  anova <- aov(lifeExp ~ continent,data=p[i] %>% as.data.frame() %>% 
                 set_colnames(c("continent","year","lifeExp")))
  
  Tukey <- TukeyHSD(anova)
  cld <- multcompLetters4(anova,Tukey)
  
  dt <- p[i] %>% as.data.frame() %>% 
    set_colnames(c("continent","year","lifeExp")) %>%
    group_by(continent,year) %>%
    summarise(lifeExp=max(lifeExp)) %>% 
    ungroup()
  
  cld <- as.data.frame.list(cld$`continent`)
  dt$Tukey <- cld$Letters
  
  aov_data  <- rbind(aov_data,dt)
}

list <- data %>% left_join(.,aov_data,by=c("continent","year")) %>% 
  split(.$year) %>%
  map(make_plot)

wrap_plots(list, ncol = 4, nrow = 3)

  