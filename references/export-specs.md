# 导出规范

## 推荐导出格式

### 优先顺序

1. **PDF** — 线图、散点图、柱状图等矢量图表的首选
2. **TIFF** — 热图、密度图、显微图像等需要高分辨率的场景
3. **PNG** — 预览用，300dpi 以上
4. **SVG** — Web 发布，可编辑

### 不推荐

- **JPEG** — 有损压缩，不适合科学图表
- **低分辨率 PNG** — 屏幕预览可以，出版物不行

## Python 导出示例

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(89/25.4, 6/25.4), dpi=300)
# ... 绘图代码 ...

# 导出 PDF (矢量)
fig.savefig('figure.pdf', format='pdf', bbox_inches='tight')

# 导出 TIFF (光栅，300dpi)
fig.savefig('figure.tiff', format='tiff', dpi=300, bbox_inches='tight')

# 导出 PNG (预览)
fig.savefig('figure.png', format='png', dpi=300, bbox_inches='tight')
```

## R 导出示例

```r
# PDF
pdf("figure.pdf", width = 89/25.4, height = 6, units = "in")
# ... 绘图代码 ...
dev.off()

# TIFF
tiff("figure.tiff", width = 89/25.4, height = 6, res = 300, units = "in")
# ... 绘图代码 ...
dev.off()
```

## 字体嵌入

### Python (matplotlib)

```python
import matplotlib.font_manager as fm

# 检查字体
fm.findfont('Arial')

# 导出时嵌入字体
fig.savefig('figure.pdf', format='pdf', embed_font=True)
```

### R

```r
# 使用 extrafont 包嵌入字体
library(extrafont)
font_import()
loadfonts()

# 导出 PDF 时嵌入
pdf("figure.pdf", width = 8, height = 6)
# ... 绘图 ...
dev.off()

# 检查字体
fonttable()
```

## 常见问题排查

1. **字体缺失**: 确保目标系统有相同字体，或使用系统字体
2. **PDF 太大**: 检查是否有嵌入大图片，考虑压缩
3. **TIFF 颜色异常**: 确认色彩模式 (RGB vs CMYK)
4. **矢量图失真**: 检查是否有光栅元素混入
