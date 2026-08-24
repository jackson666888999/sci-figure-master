#!/usr/bin/env python3
"""
PPT Skill 路由扩展 — 支持 4 大顶级 PPT Skill 路由
集成: ppt-master, frontend-slides, guizang-ppt-skill, html-ppt-skill
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 桥接模块
from ppt_master_bridge import PptMasterBridge, generate_pptx
from frontend_slides_bridge import FrontendSlidesBridge, generate_slides


class PptSkillRouter:
    """PPT Skill 路由器"""

    # Skill 评分（基于 GitHub stars + 实测）
    SKILL_SCORES = {
        "ppt-master": {"stars": 48945, "type": "pptx", "rating": 5.0, "best_for": "client",
                       "skill_dir": Path(r"E:\workbuddy\.workbuddy\skills\ppt-master\repo")},
        "frontend-slides": {"stars": 28037, "type": "html", "rating": 4.8, "best_for": "technical",
                            "skill_dir": Path(r"E:\workbuddy\.workbuddy\skills\frontend-slides\repo")},
        "guizang-ppt-skill": {"stars": 24738, "type": "html", "rating": 4.7, "best_for": "creative",
                              "skill_dir": Path(r"E:\workbuddy\.workbuddy\skills\guizang-ppt-skill\repo")},
        "html-ppt-skill": {"stars": 8033, "type": "html", "rating": 4.5, "best_for": "quick",
                           "skill_dir": Path(r"E:\workbuddy\.workbuddy\skills\html-ppt-skill\repo")},
        "tencent-pptx": {"stars": 0, "type": "pptx", "rating": 4.6, "best_for": "chinese"},
    }

    # 场景 → Skill 推荐映射
    SCENE_ROUTING = {
        "学术汇报": ["ppt-master", "tencent-pptx"],
        "组会": ["ppt-master", "tencent-pptx"],
        "答辩": ["ppt-master"],
        "技术分享": ["frontend-slides", "html-ppt-skill"],
        "Demo": ["frontend-slides"],
        "创意提案": ["guizang-ppt-skill"],
        "客户交付": ["ppt-master", "tencent-pptx"],
        "社交媒体": ["guizang-ppt-skill", "html-ppt-skill"],
        "快速演示": ["html-ppt-skill"],
        "数据驱动": ["ppt-master"],
    }

    @classmethod
    def suggest_skill(cls, scene: str, deliverable: str = "any") -> List[str]:
        """推荐 Skill"""
        skills = cls.SCENE_ROUTING.get(scene, ["ppt-master"])
        if deliverable == "pptx":
            skills = [s for s in skills if cls.SKILL_SCORES.get(s, {}).get("type") == "pptx"] or skills
        elif deliverable == "html":
            skills = [s for s in skills if cls.SKILL_SCORES.get(s, {}).get("type") == "html"] or skills
        return skills

    @classmethod
    def generate(
        cls,
        topic: str,
        scene: str = "学术汇报",
        deliverable: str = "any",
        outline: Optional[List[str]] = None,
        markdown_path: Optional[str] = None,
        output_path: Optional[str] = None,
        style: str = "academic",
        page_count: int = 10
    ) -> Dict:
        """智能选择最佳 Skill 并生成"""
        recommended = cls.suggest_skill(scene, deliverable)
        primary_skill = recommended[0]

        if primary_skill == "ppt-master":
            bridge = PptMasterBridge()
            if markdown_path:
                result = bridge.generate_from_markdown(markdown_path, output_path, style)
            else:
                result = bridge.generate(topic, outline, output_path, style, page_count)
            result["skill_used"] = primary_skill
            return result

        elif primary_skill == "frontend-slides":
            bridge = FrontendSlidesBridge()
            if markdown_path:
                with open(markdown_path, "r", encoding="utf-8") as f:
                    content = f.read()
                result = bridge.generate(topic, outline=None, markdown_content=content,
                                         output_path=output_path, style=style)
            else:
                result = bridge.generate(topic, outline, output_path, style, page_count)
            result["skill_used"] = primary_skill
            return result

        else:
            return {
                "status": "skill_not_implemented",
                "skill": primary_skill,
                "message": f"Skill '{primary_skill}' 桥接模块待实现",
                "recommendation": f"请先安装: git clone https://github.com/.../{primary_skill}.git ~/.workbuddy/skills/{primary_skill}"
            }

    @classmethod
    def list_skills(cls) -> List[Dict]:
        """列出所有可用 Skill"""
        return [
            {
                "name": name,
                "stars": info["stars"],
                "type": info["type"],
                "rating": info["rating"],
                "best_for": info["best_for"],
                "installed": info.get("skill_dir", Path()).exists()
            }
            for name, info in cls.SKILL_SCORES.items()
        ]


# 便捷函数
def generate_presentation(
    topic: str,
    scene: str = "学术汇报",
    deliverable: str = "any",
    **kwargs
) -> Dict:
    """快捷生成演示文稿"""
    return PptSkillRouter.generate(topic, scene, deliverable, **kwargs)


def get_skill_recommendation(scene: str, deliverable: str = "any") -> List[str]:
    """获取 Skill 推荐"""
    return PptSkillRouter.suggest_skill(scene, deliverable)


def list_ppt_skills() -> List[Dict]:
    """列出所有 PPT Skill"""
    return PptSkillRouter.list_skills()


if __name__ == "__main__":
    import json
    print("=== PPT Skill 路由测试 ===")
    print()
    print("可用 Skill:")
    for s in PptSkillRouter.list_skills():
        status = "✅" if s["installed"] else "⬜"
        print(f"  {status} {s['name']}: {s['stars']}⭐ {s['type']} ({s['best_for']})")
    print()
    print("场景推荐:")
    for scene in ["学术汇报", "技术分享", "客户交付", "快速演示"]:
        skills = PptSkillRouter.suggest_skill(scene)
        print(f"  {scene}: {', '.join(skills)}")
