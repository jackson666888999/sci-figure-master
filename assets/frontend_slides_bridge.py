#!/usr/bin/env python3
"""
Frontend Slides Bridge — HTML 网页演示文稿桥接模块
基于 zarazhangrui/frontend-slides (28k⭐)

支持：
- 从零生成 HTML 演示文稿
- PPTX → HTML 转换
- 12+ 模板风格选择
- 演讲者模式
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class FrontendSlidesBridge:
    """frontend-slides 桥接模块"""

    SKILL_DIR = Path(os.path.expanduser("~/.workbuddy/skills/frontend-slides"))
    if not SKILL_DIR.exists():
        SKILL_DIR = Path(r"E:\workbuddy\.workbuddy\skills\frontend-slides\repo")
    AVAILABLE_STYLES = {
        "style-a": "简约学术（推荐）",
        "style-b": "科技深色",
        "style-c": "纸与墨（水墨风）",
        "style-d": "复古胶片",
        "style-e": "瑞士网格",
        "style-f": "渐变色"
    }

    def __init__(self, skill_dir: Optional[str] = None):
        self.skill_dir = Path(skill_dir or self.SKILL_DIR)
        self._ensure_installed()

    def _ensure_installed(self) -> bool:
        if not self.skill_dir.exists():
            print(f"[frontend-slides] 技能目录不存在: {self.skill_dir}")
            print(f"[frontend-slides] 请先安装: git clone https://github.com/zarazhangrui/frontend-slides.git")
            return False
        return True

    def generate(
        self,
        topic: str,
        outline: Optional[List[str]] = None,
        markdown_content: Optional[str] = None,
        output_path: Optional[str] = None,
        style: str = "style-c",
        audience: str = "academic",
        page_count: int = 10
    ) -> Dict:
        """生成 HTML 演示文稿"""
        if not self._ensure_installed():
            return {"status": "error", "message": "frontend-slides 未安装"}

        if markdown_content:
            content_source = markdown_content
        elif outline:
            content_source = "\n".join(f"{i+1}. {line}" for i, line in enumerate(outline))
        else:
            content_source = topic

        output_path = output_path or os.path.join(os.getcwd(), f"{topic[:20]}.html")

        prompt = f"""
请生成一份关于 "{topic}" 的 HTML 演示文稿。

风格: {style} ({self.AVAILABLE_STYLES.get(style, '')})
受众: {audience}
页数: {page_count}

内容:
{content_source}

要求:
- 单文件 HTML（内联 CSS/JS）
- 支持键盘/触摸翻页
- 学术风格：专业、清晰、高对比度
- 适当配图（使用 CSS 图形或 emoji）
"""
        return {
            "status": "ready",
            "prompt": prompt.strip(),
            "output_path": output_path,
            "pages": page_count,
            "style": style,
            "skill_dir": str(self.skill_dir)
        }

    def convert_pptx_to_html(
        self,
        input_pptx: str,
        output_path: Optional[str] = None,
        style: str = "style-c"
    ) -> Dict:
        """将 PPTX 转换为 HTML"""
        prompt = f"""
请将这份 PPT 转换为 HTML 网页版：{input_pptx}

风格: {style}

要求:
- 保留所有文字和图片
- 转换为单文件 HTML
- 支持键盘翻页
"""
        output_path = output_path or input_pptx.replace(".pptx", ".html")
        return {
            "status": "ready",
            "prompt": prompt.strip(),
            "output_path": output_path
        }


def generate_slides(
    topic: str,
    outline: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    style: str = "style-c"
) -> Dict:
    """快捷生成函数"""
    bridge = FrontendSlidesBridge()
    return bridge.generate(topic=topic, outline=outline, output_path=output_path, style=style)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "XNP 多组学机制轴"

    result = generate_slides(
        topic=topic,
        outline=["封面", "背景", "方法", "结果", "讨论"],
        style="style-c"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
