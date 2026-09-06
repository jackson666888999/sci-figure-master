library(tidyverse)
library(scales)
library(camcorder)
library(shadowtext)
library(ggh4x)

df <- read_tsv("data-1.xls") %>% 
  # 由于海湾战争的缘故Kuwait的数据比较异常因此在此剔除
  filter(country != "Kuwait", continent != "Oceania") %>% 
  arrange(year) %>% 
  group_by(country) %>% 
  mutate(label = if_else(year == max(year), country,"")) %>% 
  ungroup()

ridiculous_strips <- strip_themed(
  text_x = elem_list_text(colour=c("#9C8D58","#EDB749","#3CB2EC","red"),
                          face=c("bold","bold","bold"),size=c(10,10,10,10)),
  background_x = elem_list_rect(fill = c("#E8F2FC","#E8F2FC","#E8F2FC","#E8F2FC")))

ggplot(df,aes(x = gdpPercap, y = lifeExp,group = country)) + 
  geom_path(aes(size = year), color = "salmon") +
  geom_point(data = df %>% filter(label != ""),color = "brown") +
  geom_shadowtext(data = df %>% filter(label != ""),aes(alpha = 0.5,label=label), hjust = 0, nudge_y = 1,
                  nudge_x = 1000, check_overlap = TRUE,
                  color = "#020271", size=3.5, bg.colour = "#E8F2FC", bg.r = 0.08) +
  facet_wrap2(vars(continent),scales = "free_y",axes = "y",remove_labels = "x",
              strip = ridiculous_strips)+
  scale_size_continuous(range = c(0.3, 0.8)) +
  scale_alpha_identity() +
  scale_x_continuous(labels = label_number()) +
  coord_cartesian(clip = "off") +
  theme_minimal() +
  theme(panel.spacing.x = unit(0.1,"cm"),
        panel.spacing.y = unit(0.15,"cm"),
        axis.title = element_blank(),
        plot.background = element_rect(fill="white"),
        strip.background = element_rect(color="#E8F2FC"),
        strip.text.x = element_text(size=9,color="black"),
        axis.text = element_text(color="black"),
        plot.margin = margin(10,60,10,10),
        legend.position = "non")

