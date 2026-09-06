library(tidyverse)
library(ggsci)
library(ggh4x)

df <- read_csv("data.csv") %>%
  filter(age %in% c("1 to 4","5 to 9","10 to 14","15 to 19",
                    "20 to 24","25 to 29","30 to 34","35 to 39","40 to 44",
                    "45 to 49","50 to 54","55 to 59","60 to 64","65 to 69",
                    "70 to 74","75 to 79","80 to 84","85 to 89","90 to 94",
                    "95 plus"),
         year %in% c("1990","2010"),metric=="Rate") %>% 
  filter(location %in% c("Global","High SDI","High-middle SDI",
                         "Middle SDI","Low-middle SDI","Low SDI")) %>%
  select(measure,location,sex,year,age,val) %>% 
  mutate(year=as.character(year)) %>% 
  mutate(across("age",str_replace,"95 plus","95+")) %>% 
  mutate(across("age",str_replace,"1 to 4","<5")) %>% 
  mutate(across("measure",str_replace,"Incidence","Incidence rate (per 100k)")) %>%
  mutate(across("measure",str_replace,"Deaths","Deaths rate (per 100k)")) %>%
  mutate(measure=case_when(measure=="DALYs" ~ 
                             "DALYs rate (per 100k)",
                           TRUE ~ as.character(measure))) %>% 
  arrange(measure)

df$age <- factor(df$age,levels=c(df$age %>% as.data.frame() %>% distinct() %>% filter(.!="5 to 9") %>% 
                                   dplyr::rename(age=".") %>% 
                                   add_row(age="5 to 9",.before = 2) %>% pull()
))


df$year <- factor(df$year,levels=c("1990","2010"))

# save(df,file="data.Rdata") 保存中间变量

load("data.Rdata") # 加载中间变量

df %>% arrange(year) %>% filter(measure=="DALYs rate (per 100k)",sex=="Male") %>% 
  unite(.,col="location",location,measure,sep=" ",
        remove = T,na.rm = F) %>% 
  ggplot()+
  geom_line(aes(val,age),size=2.5,color="grey80")+
  geom_point(aes(val,age,color=year),size=4)+
  facet_wrap2(vars(location), nrow = 2, ncol = 3, trim_blank = FALSE)+
  xlab(NULL)+ylab(NULL)+
  scale_color_manual(values = c("#009688","#762a83"))+
  theme_bw()+
  theme(
    axis.title.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.ticks.x = element_line(color = "#4a4e4d"),
    axis.text=element_text(color="black",face="bold"),
    strip.text = element_text(color="black",face="bold"),
    panel.background = element_rect(fill = "white",color = "white"),
    plot.background = element_rect(fill = "white"),
    panel.spacing = unit(0,"lines"),
    plot.title = element_blank(),
    legend.text = element_text(color="black",face="bold"),
    legend.title = element_blank(),
    legend.key=element_blank(),  
    legend.spacing.x=unit(0.1,'cm'), 
    legend.key.width=unit(0.4,'cm'), 
    legend.key.height=unit(0.4,'cm'), 
    legend.background=element_blank(), 
    legend.position = c(0.07,1), legend.justification = c(1,1))
