# 加载所需的R包
package.list <- c("tidyverse", "reshape", "psych", "RColorBrewer", "magrittr", "ggh4x")
for (package in package.list) {
  if (!require(package, character.only = TRUE, quietly = TRUE)) {
    install.packages(package)
    library(package, character.only = TRUE)
  }
}

# 读取数据文件
table1 <- read.delim("env.xls", header = TRUE, sep = "\t", row.names = 1, check.names = FALSE)
table2 <- read.delim("genus.xls", header = TRUE, sep = "\t", row.names = 1, check.names = FALSE) %>%
  t() %>% as.data.frame()

# 计算相关性并调整p值
pp <- corr.test(table1, table2, method = "pearson", adjust = "fdr")
cor <- pp$r
pvalue <- pp$p

# 将相关性矩阵和p值矩阵转换为数据框
library(reshape2)  # 确保加载reshape2包
cor_df <- melt(cor) %>% set_colnames(c("env", "genus", "r"))
pvalue_df <- melt(pvalue) %>% set_colnames(c("env", "genus", "p"))

# 合并相关性和p值数据框
df <- left_join(cor_df, pvalue_df, by = c("env", "genus")) %>%
  mutate(p_signif = symnum(p, corr = FALSE, na = FALSE,
                          cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1),
                          symbols = c("***", "**", "*", "", " ")))

# 读取注释文件并合并到df数据框
annotation <- read_tsv('annotation.xls', show_col_types = FALSE)
df <- df %>% left_join(annotation, by = "genus")

# 确保 r 是数值型
df$r <- as.numeric(df$r)

# 绘制热图
ggplot(df, aes(env, genus, col = r, fill = r)) +
  geom_tile(color = "grey80", fill = "white", size = 0.3) +
  geom_point(aes(size = abs(r)), shape = 21) +
  geom_text(aes(label = p_signif), size = 4, color = "white", hjust = 0.5, vjust = 0.7) +
  facet_grid2(group ~ ., scale = "free_y", switch = "y", strip = ridiculous_strips) +
  labs(x = NULL, y = NULL, color = NULL, fill = NULL) +
  scale_color_gradientn(colours = rev(RColorBrewer::brewer.pal(11, "RdBu"))) +
  scale_fill_gradientn(colours = rev(RColorBrewer::brewer.pal(11, "RdBu"))) +
  scale_x_discrete(expand = c(0, 0),
                   labels = c("NH4+" = "NH4+",
                             "NO2-" = "NO2-",
                             "CuSO4" = "CuSO4")) +
  scale_y_discrete(expand = c(0, 0), position = 'right') +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1,
                                   color = "black", face = "bold", size = 10),
        axis.text.y = element_text(color = "black", face = "bold", size = 10),
        axis.ticks = element_blank(),
        panel.spacing.y = unit(0, "cm")) +
  scale_size(range = c(1, 10), guide = NULL) +
  guides(color = guide_colorbar(direction = "vertical", reverse = FALSE, barwidth = unit(.5, "cm"),
                               barheight = unit(15, "cm")))