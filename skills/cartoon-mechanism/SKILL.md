---
name: cartoon-mechanism
description: >-
  科研卡通机制图生成子技能。专攻"代码画不了的科研示意图/卡通图"：信号通路、肠脑轴、细胞互作、药物靶标网络等机制可视化。
  中文提示词驱动，调 AI 生图 + bioicons SVG 素材组装，强制证据分级标注，输出可编辑 SVG/PDF。
  触发词：机制图、卡通图、示意图、信号通路、肠脑轴、细胞互作、靶标网络、画不了的代码图、科研插图、BioRender替代。
---

# Cartoon Mechanism — 科研卡通机制图生成

专攻代码无法绘制、需概念表达的科研示意图。对标 BioRender，但**提示词驱动 + 中文优先 + 矢量可编辑**。

## 工作流

```
用户中文描述
  ↓ [1] 解析：主体(细胞/器官/分子) + 关系(激活/抑制/连接) + 证据等级
  ↓ [2] 生成底图：调 generate-image / PaperBanana（负向提示词禁AI感）
  ↓ [3] 素材叠加：从 bioicons 取 SVG 图标（细胞/神经元/肠道/分子）
  ↓ [4] 标注：证据分级 *实验 †数据库 ‡预测 §文献
  ↓ [5] 后处理：去渐变/发光 → 转 SVG 可编辑
  ↓ [6] QA：反AI感清单 + 证据逻辑链
  ↓ 输出：SVG(可编辑) + PDF(投稿) + PPTX(汇报)
```

## 提示词模板（中文→英文）

```python
def build_cartoon_prompt(scene_zh: str, evidence: dict, style="top_journal"):
    base = f"scientific mechanism illustration of {scene_zh}, "
    style_c = ("white background, asymmetric layout, colorblind-friendly, "
               "high contrast, sans-serif labels, minimal flat design, "
               "clear arrow connections, no text overflow")
    negative = ("blue-purple gradient, neon glow, rounded card UI, "
                "decorative bubbles, 3D render, stock photo, cartoon mascot style")
    marks = " | ".join([f"{k}:{v}" for k,v in evidence.items()])
    return {"positive": base+style_c, "negative": negative, "evidence": marks}
```

## 证据分级标注示例
- 肠脑轴：肠道(†GEO数据) → 迷走神经(*电生理) → 脑(§文献)
- 药物靶标：化合物(‡预测) → 蛋白(*SPR验证) → 通路(†KEGG)

## 素材库
- bioicons.com (1000+ SVG 生物图标)
- NIH BIOART
- 本地 assets/cartoon-icons/（可扩充）

## 输出规格
- SVG：Inkscape/AI 可编辑
- PDF：投稿 600dpi
- PPTX：组会汇报

## QA 清单（强制）
- [ ] 证据符号与正文一致
- [ ] 无 AI 渐变/发光
- [ ] 箭头方向语义正确（激活=箭头，抑制=平头）
- [ ] 字体统一 Arial
