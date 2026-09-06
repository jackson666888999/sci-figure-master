setwd('D:/KS项目/公众号文章/嵌套扇形图')
library(Seurat)
df <- table(uterus$celltype, uterus$integrated_snn_res.0.1, uterus$orig.ident)
df <- as.data.frame(df)
colnames(df) <- c('celltype', 'cluster','orig.ident','cellnumber')
df$cluster <- paste('cluster','',df$cluster)
df <- df[,c('cellnumber','orig.ident','celltype','cluster')]
write.csv(df, file = 'scRNA_cell.csv')


#linux的下载
#shell
conda install krona
ktImportText scRNA_cell.txt -o sc_pie.html

#软件
# https://github.com/marbl/Krona/releases/



