# 排版规范

## 字体设置

所有图表使用无衬线字体，默认首选 Arial 或 Helvetica。

### Python (matplotlib)

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# 字体设置
mpl.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
})

# 移除顶部和右侧 spine
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 刻度向内
ax.tick_params(direction='in', top=False, right=False)
```

### R (ggplot2)

```r
library(ggplot2)

# 字体设置
theme_set(theme_minimal(base_family = "Arial"))

# 或自定义
custom_theme <- theme(
  text = element_text(family = "Arial"),
  axis.text = element_text(size = 10),
  axis.title = element_text(size = 11),
  plot.title = element_text(size = 12),
  legend.text = element_text(size = 9),
  panel.border = element_blank(),
  panel.grid.major = element_blank(),
  panel.grid.minor = element_blank(),
  axis.line = element_line(color = "black")
)
```

## 刻度规范

- X 轴刻度向内或向外，不要双向
- 刻度线长度: 2-3pt
- 避免过多刻度标签，使用合适的间隔
- 科学计数法标注在轴标题而非刻度

## 图例规范

- 默认放在图表外部右侧
- 使用直接标注替代图例（当类别少于 5 个时）
- 图例背景透明，无边框
- 图例标题使用斜体

## 图片尺寸

按目标期刊栏宽设置：

| 期刊 | 单栏宽度 | 双栏宽度 |
|------|---------|---------|
| Nature | 89mm | 183mm |
| Science | 90mm | 180mm |
| Cell | 88mm | 177mm |

## 常见问题

1. **字体渲染不一致**: 使用 `type="cairo"` (R) 或确保字体文件可用
2. **中文显示**: 需要额外配置中文字体
3. **高分辨率导出**: PDF 优先，PNG 至少 300dpi
