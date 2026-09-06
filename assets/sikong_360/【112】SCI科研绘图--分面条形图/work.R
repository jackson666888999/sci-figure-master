library(tidyverse)
library(ggtext)

df <- read_tsv("data.xls")

max_points <-data.frame(x=c(2010, 2015, 2017), y=rep(25,3))
by_gf<- df %>% group_by(gf) %>% summarise(min_year = min(year),
                                          max_year = max(year))

id <- data.frame(name=c("Time", unique(df$gf)),
                 pos = seq(from=1999, to=2019, length.out = 9))

data2 <- read_tsv("data2.xls")

p1 <- ggplot(data=df, aes(x=year))+
  geom_segment(data = data.frame(y = seq(from=0, to=50, by=5)),
               mapping=aes(x=1999, xend=2019, y=y, yend=y), color="white",
               size=0.1, alpha=0.2)+
  geom_segment(mapping=aes(x=year, xend=year, y=0, yend=age_gf), color="#FD7600", size=5)+
  geom_text(mapping=aes(y=age_gf+1.5, label=age_gf), color="#FD7600")+
  scale_y_continuous(limits=c(-20,50), breaks=seq(from=0, to=50, by=5))+
  geom_text(mapping=aes(x=year,label=paste0("",substr(year,3,4)), y=-1.5),color="black")+
  geom_segment(mapping=aes(x=2010, xend=2017, y=30, yend=30), color="black", size=0.15)+
  geom_segment(data=max_points, mapping=aes(x=x, xend=x, y=30, yend=28),
               color="black", size=0.3)

p1 + geom_point(data=max_points, mapping=aes(x=x, y=y+1.5),
             shape=21, fill="grey", color="black", size=11)+
  geom_text(data=max_points, mapping=aes(x=x, y=y+1.5, label=y), color="#FD7600")+
  geom_segment(data=data.frame(x=2000,xend=2002,y=45,color="#FD7600",size=1.5),
               mapping=aes(x=x,xend=xend,y=y, yend=y, color=color, size=size))+
  scale_size_identity()+
  geom_segment(data=by_gf, mapping=aes(x=min_year, xend=max_year, y=-4, yend=-4), color="#FD7600")+
  geom_segment(data=by_gf, mapping=aes(x=min_year, xend=min_year, y=-4, yend=-3), color="#FD7600")+
  geom_segment(data=by_gf, mapping=aes(x=max_year, xend=max_year, y=-4, yend=-3), color="#FD7600")+
  geom_segment(data=id|>filter(name!="Time"),
               mapping=aes(x=pos, xend=pos, y=-13, yend=-10), color="#FD7600")+
  geom_segment(data=data2, mapping=aes(x=x,xend=xend,y=y,yend=yend), color="#FD7600")+
  geom_richtext(data=id,mapping=aes(y=-19.5, x=pos, color="#FD7600",
                                    label=str_replace(name," ","<br>")),
                      fill = NA,label.color = NA, hjust=0.4,
                      show.legend = FALSE, fontface="bold")+
  scale_color_identity()+
  labs(x=NULL,y=NULL)+
  theme_bw()+
  theme(panel.background = element_rect(fill="white", color=NA),
        plot.background = element_rect(fill="white"),
        text = element_text(color="black"),
        plot.margin = margin(t=10,l=10,b=10,r=10),
        panel.grid = element_blank(),
        axis.text.y=element_text(color="black",size=10,face="bold"),
        axis.ticks.y = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x=element_blank())
      
      