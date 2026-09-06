setwd('D:/KS项目/公众号文章/炫酷单细胞聚类图')
devtools::install_github("TheHumphreysLab/plot1cell")
library(plot1cell)

# bioc.packages <- c("DoubletFinder","EnsDb.Hsapiens.v86",
#                    "GEOquery","simplifyEnrichment")
# BiocManager::install(bioc.packages)
# 
# dev.packages <- c("chris-mcginnis-ucsf/DoubletFinder")
# devtools::install_github(dev.packages)


# ============1. Circlize plot to visualize cell clustering and meta data======#

get_metadata <- function(
    seu_obj, 
    reductions = "tsne", 
    coord_scale = 0.8, 
    color
){
  metadata<-seu_obj@meta.data
  metadata$Cluster<-seu_obj@active.ident
  metadata$dim1<-as.numeric(seu_obj[[reductions]]@cell.embeddings[,1])
  metadata$dim2<-as.numeric(seu_obj[[reductions]]@cell.embeddings[,2])
  metadata$x<-transform_coordinates(metadata$dim1, zoom = coord_scale)
  metadata$y<-transform_coordinates(metadata$dim2, zoom = coord_scale)
  color_df<-data.frame(Cluster=levels(seu_obj), Colors=color)
  cellnames<-rownames(metadata)
  metadata$cells<-rownames(metadata)
  metadata<-merge(metadata, color_df, by='Cluster')
  rownames(metadata)<-metadata$cells
  metadata<-metadata[cellnames,]
  metadata
}


prepare_circlize_data <- function(
    seu_obj, 
    scale =0.8
){
  celltypes<-levels(seu_obj)
  cell_colors <- scales::hue_pal()(length(celltypes))
  data_plot <- get_metadata(seu_obj, color = cell_colors, coord_scale = scale)
  data_plot <- cell_order(data_plot)
  data_plot$x_polar2 <- log10(data_plot$x_polar)
  data_plot
}


###Prepare data for ploting
circ_data <- prepare_circlize_data(uterus, scale = 0.8)
set.seed(1234)
cluster_colors<-rand_color(length(levels(uterus)))
group_colors<-rand_color(length(names(table(uterus$orig.ident))))


###plot and save figures
png(filename =  'circlize_plot.png', width = 6, height = 6,units = 'in', res = 300)
plot_circlize(circ_data, do.label = T, pt.size = 1, 
              col.use = cluster_colors ,bg.color = 'white', 
              kde2d.n = 500, repel = T, label.cex = 0.8)
add_track(circ_data, group = "orig.ident", colors = group_colors, track_num = 2)
dev.off()


# ============1. Circlize plot to visualize cell clustering and meta data======#
###Prepare data for ploting
circ_data <- prepare_circlize_data(human_data, scale = 0.8)
cluster_colors<-rand_color(length(levels(human_data)))
group_colors<-rand_color(length(names(table(human_data$group))))
rep_colors<-rand_color(length(names(table(human_data$orig.ident))))

###plot and save figures
png(filename =  'circlize_plot1.png', width = 6, height = 6,units = 'in', res = 300)
plot_circlize(circ_data, do.label = T, pt.size = 1, 
              col.use = cluster_colors ,bg.color = 'white', 
              kde2d.n = 500, repel = T, label.cex = 0.8)
add_track(circ_data, group = "group", colors = group_colors, track_num = 2) 
add_track(circ_data, group = "orig.ident",colors = rep_colors, track_num = 3) 
#添加legend
legend("topright", 
       legend = unique(human_data$group),
       col = group_colors,
       pch = 15,
       cex=0.5,
       pt.cex=2,
       box.lwd = 0,
       bg=NULL,
       y.intersp = 1,
       box.lty=0)


legend("topleft", 
       legend = unique(human_data$orig.ident),
       col = rep_colors,
       pch = 15,
       cex=0.5,
       pt.cex=2,
       box.lwd = 0,
       bg=NULL,
       y.intersp = 1.5,
       box.lty=0)

dev.off()



#2. Dotplot to show gene expression across groups
png(filename =  'dotplot_multiple.png', width = 10, height = 4,units = 'in', res = 300)
complex_dotplot_multiple(seu_obj = human_data, 
                         features = c("CD3E","S100A8","APOE","CXCL3"),
                         group = "group", celltypes = c("Macrophage","T cell","mDC","Neutrophil","Mast"))
dev.off()


png(filename =  'dotplot_multiple2.png', width = 10, height = 4,units = 'in', res = 300)
complex_dotplot_multiple(seu_obj = human_data, 
                         features = c("CD3E","S100A8","APOE","CXCL3"),
                         group = "orig.ident", celltypes = c("Macrophage","T cell","mDC","Neutrophil","Mast"))
dev.off()


#3. Cell proportion change across groups
png(filename =  'cell_fraction.png', width = 8, height = 4,units = 'in', res = 300)
plot_cell_fraction(human_data,  celltypes = c("Macrophage","T cell","mDC","Neutrophil","Mast"), groupby = "group", show_replicate = T, rep_colname = "orig.ident")
dev.off()






