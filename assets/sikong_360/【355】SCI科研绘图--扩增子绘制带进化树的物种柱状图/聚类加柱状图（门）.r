# 聚类加柱状图（门）

# 一、数据处理

# 加载必要的包
library(dplyr)
library(tidyr)
library(tidyverse)

# 设置工作路径
setwd("C:\\Users\\34790\\Desktop\\16S")

# 读取数据
feature_table <- read.csv("modified-feature-table.csv", check.names = FALSE)
taxonomy_table <- read.csv("modified-taxonomy.csv", check.names = FALSE)

# 更改工作路径
setwd("C:\\Users\\34790\\Desktop\\16S\\物种堆积柱状图")

# 定义分类层级提取函数（无需修改）
extract_taxon <- function(taxon_str, level) {
  sapply(strsplit(taxon_str, "; "), function(x) {
    target <- grep(paste0("^", level, "__"), x, value = TRUE)
    ifelse(length(target) > 0, 
           sub(paste0("^", level, "__"), "", tail(target, 1)),
           "Unclassified")
  })
}

# ------------------ 核心修改点 -------------------
# 将 "c" 改为 "p"，"Class" 改为 "Phylum"
merged_data <- taxonomy_table %>%
  mutate(Phylum = extract_taxon(Taxon, "p")) %>%  # 提取门级分类
  select(ASV_ID, Phylum) %>%                      # 选择门列
  inner_join(feature_table, by = "ASV_ID") %>% 
  select(-ASV_ID)

# 按门聚合数据（修改列名）
class_abundance <- merged_data %>%
     filter(Phylum != "Unclassified") %>%        # 过滤未分类门
     group_by(Phylum) %>%                         # 按门分组
     summarise(across(everything(), sum)) %>%
     column_to_rownames("Phylum")                 # 列名设为门名称

# 查看前6行
head(class_abundance)

# 保存结果（修改文件名）
write.csv(class_abundance, "phylum.csv", quote = FALSE)

# ------------------ 后续分析同理 -------------------
# 提取丰度top20的门
data <- read.csv("phylum.csv", row.names = 1, check.names = FALSE)

row_sums <- rowSums(data, na.rm = TRUE)
top20 <- data[order(-row_sums), ][1:20, ]

write.csv(top20, "top20_phyla.csv")
cbind(top20, Total = row_sums[rownames(top20)])

# 二、绘图

# 设置工作路径
setwd("C:\\Users\\34790\\Desktop\\16S")

# 加载包
library(ggtree)
library(ggplot2)
library(dplyr)
library(reshape2)
library(randomcoloR)
library(vegan)

# 导入门级数据 ---------------------------------------------------------
Phylum <- read.csv("top20_phyla.csv", row.names = 1, check.names = FALSE)  # 修改文件名

# 生成颜色方案 ---------------------------------------------------------
phylum_count <- nrow(Phylum)  # 变量名修改
palette <- distinctColorPalette(phylum_count)

# 计算比例数据 ---------------------------------------------------------
Phylum_prop <- apply(Phylum, 2, prop.table)  # 修改数据对象名称
write.csv(Phylum_prop, "Phylum-比例.csv", row.names = TRUE)  # 修改文件名

# 重新加载比例数据
Phylum <- read.csv("Phylum-比例.csv", row.names = 1, check.names = FALSE)

# 样本聚类分析 ---------------------------------------------------------
dis_bray <- vegdist(t(Phylum), method = 'bray')  # 数据对象名称修改
tree <- hclust(dis_bray, method = 'average')

# 绘制基础聚类树
ggtree(tree) +  
  geom_tippoint(size = 2) +
  geom_tiplab(hjust = -0.5) + 
  theme_tree2()

# 分组处理 ------------------------------------------------------------
tree <- ape::as.phylo(tree)
group <- read.csv("Group.csv", row.names = 1)
group_list <- split(row.names(group), group$group)

# 分组着色树
p1 <- ggtree(groupOTU(tree, group_list), aes(color = group), size = 1) +   
  geom_tippoint(size = 2, show.legend = FALSE) +    
  geom_tiplab(hjust = -0.3, size = 3, show.legend = FALSE) +    
  theme_tree2() +
  xlim_tree(0.19)

# 准备堆叠图数据 -------------------------------------------------------
Phylum$Phylum <- factor(rownames(Phylum), levels = rev(rownames(Phylum)))  # 变量名修改
Phylum_draw <- melt(Phylum, id.vars = 'Phylum')  # 修改id列名称
Phylum_draw <- Phylum_draw[c(2, 3, 1)]  # 列顺序调整

# 组合图形 ------------------------------------------------------------
p2 <- p1 +   
  geom_facet(
    panel = 'Relative abundance (%)', 
    data = Phylum_draw, 
    geom = geom_bar,              
    mapping = aes(x=100 * value, fill = Phylum), 
    color = NA,             
    orientation = 'y', 
    width = 0.8, 
    stat = 'identity'
  ) +   
  theme(
    legend.title  = element_text(
      size = 14, 
      family = 'serif',
      hjust = 0  # 标题左对齐 
    ), 
    legend.text  = element_text(
      size = 14, 
      family = 'serif',
      hjust = 0   # 文本左对齐 
    ),
    legend.position  = "right",  
    legend.box  = "vertical",      
    legend.box.just  = "left",     # 容器整体左对齐 
    legend.justification  = "left",# 内容左对齐 
    legend.box.margin  = margin(0, 0, 0, 5),  # 左侧留白 
    legend.spacing.y  = unit(5, "mm")        # 增大两图例间距 
  ) +     
  scale_fill_manual(values = c(palette)) +
  guides(
    colour = guide_legend(
      order = 1, 
      title.position  = "top",
      title.hjust  = 0  # 分组标题强制左对齐 
    ),  
    fill = guide_legend(
      order = 2, 
      title.position  = "top",
      title.hjust  = 0  # 分类标题强制左对齐 
    )
  )

p2
# 导出图形 ------------------------------------------------------------
ggsave("Clustered_StackedBar_Phylum.pdf", p2, width = 16, height = 10, dpi = 300)  # 修改文件名
