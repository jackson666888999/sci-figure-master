library(tidyverse)
library(networkdata)
library(ggraph)
library(graphlayouts)
library(ggforce)
library(igraph)

dt <- read_tsv("GO.xls") %>%
  select(3,geneID,Count) %>% 
  head(6) %>% 
  filter(Description !="cutin biosynthetic process") %>% 
  separate_rows(.,geneID,convert = T,sep="/")

nodes <- data.frame(
  Id = c(unique(dt$Description),
         unique(dt$geneID))
) %>% as_tibble() %>% 
  dplyr::mutate(NodeType = c(rep("Description", length(unique(dt$Description))),
                             rep("geneID", length(unique(dt$geneID)))
  )) %>%
  left_join(dt[, c("Description","Count")], 
            by = c("Id"="Description")) %>%
  dplyr::distinct(Id,.keep_all=TRUE)

edges <- dt %>% select(1,2) %>% distinct()

p2 <- graph_from_data_frame(edges, directed=TRUE, vertices=nodes)


as_data_frame(p2 , what="vertices")

as_data_frame(p2, what="edges")

ggraph(p2,layout="stress") +
  geom_edge_link0(edge_colour = "grey66", edge_width = 0.5)+
  geom_node_point(aes(fill = NodeType),shape = 21,size=3,show.legend = F)+
  geom_node_point(aes(fill = NodeType,color=NodeType,
                      size=Count),shape = 21,show.legend = F)+
  geom_node_text(aes(label = name),
                 repel = TRUE) +
  scale_fill_manual(values = c("#5686C3", "#75C500", "#424242"))+
  scale_color_manual(values = c("#5686C3", "#75C500", "#424242"))+
  theme_graph()






