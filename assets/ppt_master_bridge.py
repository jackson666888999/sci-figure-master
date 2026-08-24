#!/usr/bin/env python3
"""
PPT Master Bridge — 原生 .pptx 生成桥接模块
基于 hugohe3/ppt-master (48.9k⭐)

支持：
- 从主题/大纲生成 .pptx
- 从 Markdown/Word/PDF/URL 生成
- 从已有 PPTX 修改
- 数据驱动图表和表格
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class PptMasterBridge:
    """ppt-master 桥接模块"""

    SKILL_DIR = Path(r"E:\workbuddy\.workbuddy\skills\ppt-master\repo")
    NODE_BIN = r"C:\Users\hyl\.workbuddy\binaries\node\versions\22.22.2\node.exe"

    def __init__(self, skill_dir: Optional[str] = None):
        self.skill_dir = Path(skill_dir or self.SKILL_DIR)
        self._ensure_installed()

    def _ensure_installed(self) -> bool:
        """检查 ppt-master 是否已安装"""
        if not self.skill_dir.exists():
            print(f"[ppt-master] 技能目录不存在: {self.skill_dir}")
            print(f"[ppt-master] 请先安装: git clone https://github.com/hugohe3/ppt-master.git")
            return False
        return True

    def generate(
        self,
        topic: str,
        outline: Optional[List[str]] = None,
        markdown_content: Optional[str] = None,
        output_path: Optional[str] = None,
        style: str = "academic",
        page_count: int = 10,
        template: Optional[str] = None
    ) -> Dict:
        """
        生成 PPTX

        Args:
            topic: 主题描述
            outline: 页面大纲列表
            markdown_content: Markdown 内容（替代 outline）
            output_path: 输出路径（默认为当前目录）
            style: 风格 ("academic" | "business" | "minimal" | "dark")
            page_count: 页数
            template: 模板路径（可选）

        Returns:
            {
                "status": "success" | "failed",
                "pptx_path": "output.pptx",
                "pages": 10,
                "prompt_used": "..."
            }
        """
        if not self._ensure_installed():
            return {"status": "error", "message": "ppt-master 未安装"}

        # 构建 prompt
        if markdown_content:
            content_source = markdown_content
        elif outline:
            content_source = "\n".join(f"{i+1}. {line}" for i, line in enumerate(outline))
        else:
            content_source = topic

        prompt = f"""
请生成一份关于 "{topic}" 的学术汇报 PPT。

风格要求: {style}
页数: {page_count}

内容大纲:
{content_source}

输出要求:
- 原生 .pptx 格式
- 每页包含标题、要点、图表（如有数据）
- 学术风格：简洁、专业、高对比度
- 配色建议：深色背景 + 浅色文字，或纯白背景 + 深色文字
"""
        # 调用 ppt-master CLI
        # ppt-master 通过 Claude Code / Cursor 等 Agent 使用
        # 这里返回 prompt 供用户自行使用
        output_path = output_path or os.path.join(os.getcwd(), f"{topic[:20]}.pptx")

        return {
            "status": "ready",
            "prompt": prompt.strip(),
            "output_path": output_path,
            "pages": page_count,
            "style": style,
            "skill_dir": str(self.skill_dir)
        }

    def generate_from_markdown(
        self,
        markdown_path: str,
        output_path: Optional[str] = None,
        style: str = "academic"
    ) -> Dict:
        """从 Markdown 文件生成 PPTX"""
        with open(markdown_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.generate(
            topic=Path(markdown_path).stem,
            markdown_content=content,
            output_path=output_path,
            style=style
        )

    def generate_from_pptx(
        self,
        input_pptx: str,
        output_path: Optional[str] = None,
        modifications: Optional[List[str]] = None
    ) -> Dict:
        """从已有 PPTX 修改生成"""
        prompt = f"""
请修改这份 PPT：{input_pptx}

修改要求:
{chr(10).join(modifications or ["优化样式，保持学术风格"])}

输出: 原生 .pptx
"""
        output_path = output_path or input_pptx
        return {
            "status": "ready",
            "prompt": prompt.strip(),
            "output_path": output_path
        }


# 便捷函数
def generate_pptx(
    topic: str,
    outline: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    style: str = "academic",
    page_count: int = 10
) -> Dict:
    """快捷生成函数"""
    bridge = PptMasterBridge()
    return bridge.generate(
        topic=topic,
        outline=outline,
        output_path=output_path,
        style=style,
        page_count=page_count
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "XNP 乌灵菌粉多组学机制轴"

    result = generate_pptx(
        topic=topic,
        outline=[
            "封面：XNP 多组学机制轴",
            "研究背景",
            "菌群 6 方法共识",
            "血清代谢物",
            "MOFA Factor3",
            "单细胞信号通路",
            "睡眠行为恢复",
            "讨论"
        ],
        style="academic",
        page_count=8
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
