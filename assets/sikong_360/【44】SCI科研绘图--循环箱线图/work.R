library(tidyverse)
library(ggsci)
library(purrr)

df <- read_tsv("data.txt") %>% filter(gene_id !="H2BC4")

df %>% 
  ggplot(aes(WHO_temp_severity, logCPM)) +
  geom_violin(aes(fill = WHO_temp_severity)) +
  stat_boxplot(geom="errorbar",width=0.1)+ 
  geom_boxplot(width = 0.15,fill="white") +
  facet_wrap(.~gene_id,scale="free")+
  labs(x=NULL,y=NULL)+
  scale_fill_npg()+
  theme_test() +
  theme(legend.position = "none",
        plot.title =  element_text(color="black",size=10,vjust = 0.5,hjust=0.5),
        axis.text = element_text(color = "black", face = "bold",size=8),
        strip.background = element_blank(),
        strip.text.x = element_text(color="black",face="bold",size=11))

#-------------------------------------------
df <- read_tsv("data.txt") %>% filter(gene_id !="H2BC4")

gene_ids <- unique(df$gene_id)

plots <- list()

for (gene in gene_ids) {
  p <- df %>% 
    ggplot(aes(WHO_temp_severity, logCPM)) +
    geom_violin(aes(fill = WHO_temp_severity)) +
    stat_boxplot(geom="errorbar",width=0.1)+ 
    geom_boxplot(width = 0.15,fill="white") +
    ggtitle(gene)+
    labs(x = NULL, y = NULL) +
    scale_fill_npg()+
    theme_test() +
    theme(legend.position = "none",
          plot.title =  element_text(color="black",size=10,vjust = 0.5,hjust=0.5),
          axis.text = element_text(color = "black", face = "bold",size=8))

  plots[[gene]] <- p
  
  ggsave(paste0("plot_", gene, ".pdf"), plot = p,dpi=300,width = 3.9,height = 2.9,units="in")
}

save(plots,file = "plots.RData")

load("plots.RData")
#-----------------------------------------------------------------------------
df <- read_tsv("data.txt") %>% filter(gene_id !="H2BC4")
gene_ids <- unique(df$gene_id)

# 使用 map 函数循环执行每个 gene_id
plot_list <- map(gene_ids, function(gene_ids) {
  df %>% 
    ggplot(aes(WHO_temp_severity, logCPM)) +
    geom_violin(aes(fill = WHO_temp_severity)) +
    stat_boxplot(geom="errorbar",width=0.1)+ 
    geom_boxplot(width = 0.15,fill="white") +
    ggtitle(gene_ids)+
    labs(x = NULL, y = NULL) +
    scale_fill_npg()+
    theme_test() +
    theme(legend.position = "none",
          plot.title =  element_text(color="black",size=10,vjust = 0.5,hjust=0.5),
          axis.text = element_text(color = "black", face = "bold",size=8))
  
})

# 将结果单独保存
map2(plot_list, gene_ids, function(plot, gene_ids) {
  ggsave(plot, filename = paste0("plot_", gene_ids, ".pdf"),
         dpi=300,width = 3.9,height = 2.9,units="in")
})






