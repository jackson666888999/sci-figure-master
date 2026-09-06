library(tidyverse)
library(maps)
library(patchwork)

df <- read.csv("data.csv")

map<-map_data("world")

map_data<-left_join(map,df,by=c("region"="Country"))

map_plot_amer<- ggplot(map_data,aes(x=long, y= lat, group=group, fill=Women))+
  geom_polygon()+
  scale_fill_gradientn(colours = RColorBrewer::brewer.pal(11,"RdBu"),
                       guide="none")+
  coord_map("ortho",orientation=c(10,-90,0))+
  theme_void()

map_plot_afr <- ggplot(map_data, aes(x=long, y= lat, group=group, fill=Women))+
  geom_polygon()+
  scale_fill_gradientn(colours = RColorBrewer::brewer.pal(11,"RdBu"),
                       guide="none")+
  coord_map("ortho",orientation=c(0,20,0))+
  theme_void()

map_plot_amer+map_plot_afr


bar_amer<-df%>%filter(Continent %in% c('Americas'))%>%arrange(Continent, -Women)
bar_amer$id <- seq(1, nrow(bar_amer))
number_of_bar_amer <- nrow(bar_amer)
angle_amer <- 90 - 360 * (bar_amer$id-0.5) /number_of_bar_amer 
bar_amer$hjust <- ifelse( angle_amer < -90, 1, 0)
bar_amer$angle <- ifelse(angle_amer < -90, angle_amer+180, angle_amer)

bar_afr<-df%>%filter(Continent %in% c('Africa'))%>%arrange(Continent, -Women)
bar_afr$id <- seq(1, nrow(bar_afr))
number_of_bar_afr <- nrow(bar_afr)
angle2 <- 90 - 360 * (bar_afr$id-0.5) /number_of_bar_afr
bar_afr$hjust <- ifelse( angle2 < -90, 1, 0)
bar_afr$angle <- ifelse(angle2 < -90, angle2+180, angle2)

p1 <- ggplot(bar_amer, aes(x=as.factor(id), y=Women, fill=Women)) +       
  geom_bar(stat="identity") +
  geom_text(aes(x=as.factor(id), y=Women+3, label=Country,
                hjust=hjust, angle=angle), color="black",
            alpha=0.6, size=3, inherit.aes = FALSE )+ 
  scale_fill_gradientn(limits= c(15,35),
                       colours = RColorBrewer::brewer.pal(11,"RdBu"),
                     guide=guide_colorbar(title.position = "top",
                                          barwidth = 10))+
  ylim(-50,40) +
  theme_void() + 
  coord_polar()+
  theme(legend.position="top",legend.title = element_blank())


p2 <- ggplot(bar_afr, aes(x=as.factor(id), y=Women, fill=Women)) +       
  geom_bar(stat="identity") +
  geom_text(aes(x=as.factor(id), y=Women+3, label=Country, hjust=hjust,
                angle=angle), color="black",
            alpha=0.6, size=3, inherit.aes = FALSE )+ 
  scale_fill_gradientn(limits= c(15,35),
                       colours =RColorBrewer::brewer.pal(11,"RdBu"),
                       guide=guide_colorbar(title.position = "top",
                                            barwidth = 10))+
  ylim(-50,40) +
  theme_void() + 
  coord_polar()+
  theme(legend.position="top",legend.title = element_blank())

americas <- p1 +
  inset_element(map_plot_amer,left = 0.3, bottom = 0.28, right = 0.7, top = 0.72)

africa<- p2 + 
  inset_element(map_plot_afr,left = 0.3, bottom = 0.28, right = 0.7, top = 0.72)

americas+africa


