setwd('D:/KS项目/公众号文章/pheatmap和ggplot的结合')
df <- read.csv('df.csv', header = T)
data <- df[df$PreferredSymbol %in% c("DNMT3A", "TET2", "NOTCH1", "JAK2", "U2AF2", "JAK3", "ASXL1"), ]
data1 <- data[, c("Participant_ID","Largest_VAF","wave","PreferredSymbol")]

#行注释
data.anno <- data1[ , colnames(data1) %in% c("wave", "Participant_ID")]
data.anno <- unique(data.anno)
rownames(data.anno) <- data.anno$Participant_ID


for_order <- reshape2::dcast(as.data.frame(data1),
                             PreferredSymbol~Participant_ID, value.var="Largest_VAF")
for_order[is.na(for_order)] = 0
rownames(for_order) <- for_order$PreferredSymbol
for_order <- for_order[ , !(colnames(for_order) %in% c("PreferredSymbol")) ]
cluster_order <- pheatmap(for_order, annotation_col = data.anno, 
                          show_rownames = F, show_colnames = F,
                          annotation_names_col = F)


#气泡图

p <- ggplot(data, aes(Participant_ID, PreferredSymbol))+
  geom_point(aes(size = Largest_VAF,colour = Variant_Classification), alpha=0.3)+
  scale_size(range = c(0,15)) +
  xlab("") + 
  ylab("")+theme_minimal() + 
  theme(panel.background = element_blank(), axis.line = element_line(colour = "black"),
                                 legend.text=element_text(size=11),
        axis.text.x = element_blank(),
        axis.text.y = element_text(color="black", size=9),
        axis.text=element_text(size=16),
        axis.title=element_text(size=16, face = "bold"))+
  scale_y_discrete(limits=rev(cluster_order$tree_row$labels[cluster_order$tree_row$order]))+
  scale_x_discrete(limits=(cluster_order$tree_col$labels[cluster_order$tree_col$order]))+
  guides(colour = guide_legend(override.aes = list(size=5), 
                               title = c("Variant Classification")),
         size = guide_legend(title = c("VAF")))+
  scale_colour_manual(values=c(Frame_Shift_Del="#00BBDA",
                               Frame_Shift_Ins="#E18A00",
                               Missense_Mutation="#BE9C00",
                               Nonsense_Mutation="#24B700",
                               Splice_Region="#00C1AB",
                               Splice_Site="#F8766D"))

