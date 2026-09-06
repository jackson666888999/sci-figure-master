library(tidyverse)
library(UpSetR)
library(ggplotify)
library(cowplot)
library(ggrepel)

otu_RA <- read_tsv("data.xls") %>% column_to_rownames(var="OTUID")

p1 <- UpSetR::upset(otu_RA, 
              nset = 7, # 集合数
              nintersects = 10, # 绘制交叉数目
              order.by = "freq", # 排序方式
              mb.ratio = c(0.7,0.3), #  条形图与点图之间的比例
              point.size = 1.8,line.size = 1,mainbar.y.label = "Intersection size",
              sets.x.label = "Set Size",
              main.bar.color = "#2a83a2",
              sets.bar.color = "#3b7960",
              queries = list(list(query = intersects,
                                  params = list("BS","RS","RE","VE","SE","LE","P"),
                                  active = T,color="#d66a35",
                                  query.name = "BS vs RS vs RE vs VE vs SE vs LE vs P")))

p2 <- tribble(~group, ~perc,~A,
        "24%",24,5,
        "76%",76,5) %>% 
  ggplot(aes(A,perc,fill=group))+
  geom_col()+
  coord_polar(theta="y")+
  xlim(0,6)+
  labs(title="Number of overlapped OTUs:1364\nNumber of total OTUs in xylem: 1792")+
  scale_fill_manual(values=c("#75C500","#5686C3"))+
  theme_void()+
  theme(legend.position = "non",
        plot.title = element_text(hjust=0.5,vjust=-62,color="black",size=6.8),
        plot.margin = unit(c(-2,0,-1,0),unit="cm"))+
  geom_text_repel(data=. %>% filter(group=="76%"),
                  aes(label=group,x=5,y=60),
                  nudge_x=-2.5,
                  nudge_y=0,size=4,
                  box.padding = 1,segment.curvature=-0.1,hjust=1)


p1 %>% as.grob() %>% ggdraw()+
  theme(plot.margin = unit(c(0,0,-0.8,-3),unit="cm"))+
  draw_plot(p2,scale=0.4,x=0.25,y=0.22)

ggsave(file="venn.pdf",width=5.6,height=4.3,unit="in",dpi=300)

otu_select <- read_tsv("data.xls") %>% filter_all(all_vars(. > 0))

write.table(as.matrix(otu_select),"otu_overlap.txt",sep = '\t',quote = FALSE,col.names = NA)
