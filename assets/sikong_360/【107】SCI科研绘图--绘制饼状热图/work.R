library(tidyverse)
library(scatterpie)
library(ggsci)
library(cowplot)
library(jjAnno)


p <- read_tsv("data1.txt") %>% 
  filter(Compartments %in% c("BS","RS","RE","VE","SE","LE")) %>% 
  select(1,2,Compartments) %>% 
  left_join(.,read_tsv("data2.txt") %>% column_to_rownames(var="FAPROTAX") %>% t() %>% 
              as.data.frame() %>%
              rownames_to_column(var="Compartments") %>% 
              pivot_longer(-Compartments),by="Compartments") %>% 
  filter(Compartments=="BS",
         SampleID %in% c(read_tsv("data1.txt") %>% select(1) %>% 
                           distinct() %>% head(10) %>% pull())) %>% 
  select(-value,-Compartments) %>% 
  group_by(SampleID,name) %>% count(Phylum) %>% 
  pivot_wider(.,names_from=Phylum,values_from = n)

df <- p %>% left_join(.,p %>% select(name) %>% distinct() %>% rownames_to_column(var="lat"),by="name") %>% 
  mutate(long=case_when(SampleID =="BCCCK1" ~1,SampleID =="BCCCK2" ~2,SampleID =="BCCCK3" ~3,
                        SampleID =="BCCNPK1" ~4,SampleID =="BCCNPK2" ~5,SampleID =="BCCNPK3" ~6,
                        SampleID =="BCCNPKM1" ~7,SampleID =="BCCNPKM2" ~8,SampleID =="BCCNPKM3" ~9,
                        SampleID =="BHLCK1" ~10),lat=as.numeric(lat))

p1 <- ggplot(aes(x=long,y=lat),data=df) +
  geom_tile(color="black",fill="white")+
  geom_scatterpie(aes(x=long,y=lat,r=0.4),data=df, color=NA,
                           cols=c("Abditibacteriota","Acidobacteriota","Actinobacteriota",
                                  "Alphaproteobacteria","Bacteroidota")) +
                             coord_equal()+
  scale_fill_nejm()+
  scale_x_discrete(expand = c(0,0))+
  scale_y_discrete(expand = c(0,0))+
  theme_test()+
  theme(axis.text.x=element_text(angle = 90,vjust = 0.5,hjust = 1),
        axis.ticks = element_blank(),
        axis.text.y=element_blank(),
        axis.title = element_blank(),
        legend.title = element_blank(),
        legend.key=element_blank(),   # 图例键为空
        legend.text = element_text(color="black",size=9), # 定义图例文本
        legend.spacing.x=unit(0.1,'cm'), # 定义文本书平距离
        legend.key.width=unit(0.5,'cm'), # 定义图例水平大小
        legend.key.height=unit(0.5,'cm'), # 定义图例垂直大小
        legend.background=element_blank())

p2 <- df %>% select(name,lat) %>% arrange(lat) %>% mutate(type="A") %>% 
  ggplot(aes(type,name))+
  coord_cartesian(clip="off")+
  scale_x_discrete(expand = c(0,0))+
#  scale_y_discrete(expand = c(0,0))+
  theme(panel.background = element_rect(fill="white"),
        axis.ticks = element_blank(),
        axis.text.y=element_text(color="black"),
        axis.title=element_blank(),axis.text.x=element_blank())

ggdraw(xlim=c(-0.45,1))+ 
  draw_plot(p2,x=-0.4)+
  draw_plot(p1,x=0.06)


