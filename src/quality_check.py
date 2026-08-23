"""
质量检查工具 - 用于验证生成的图表是否符合出版标准
"""

import os
import sys
from pathlib import Path


def check_figure_quality(fig_path: str, min_width: int = 800, min_height: int = 600) -> dict:
    """
    检查图表质量

    Args:
        fig_path: 图表文件路径
        min_width: 最小宽度（像素）
        min_height: 最小高度（像素）

    Returns:
        包含检查结果的字典
    """
    result = {
        "valid": True,
        "issues": [],
        "warnings": []
    }

    fig_path = Path(fig_path)

    # 检查文件是否存在
    if not fig_path.exists():
        result["valid"] = False
        result["issues"].append(f"文件不存在: {fig_path}")
        return result

    # 检查文件大小
    file_size = fig_path.stat().st_size
    if file_size < 1024:  # 小于 1KB
        result["warnings"].append(f"文件过小 ({file_size} bytes)，可能是空文件")

    # 检查文件格式
    suffix = fig_path.suffix.lower()
    if suffix not in ['.png', '.pdf', '.svg', '.tiff', '.jpg']:
        result["warnings"].append(f"非标准格式: {suffix}")

    # PNG 检查
    if suffix == '.png':
        try:
            from PIL import Image
            with Image.open(fig_path) as img:
                width, height = img.size
                if width < min_width or height < min_height:
                    result["warnings"].append(
                        f"分辨率过低: {width}x{height} (建议 >= {min_width}x{min_height})"
                    )
                # 检查颜色模式
                if img.mode not in ['RGB', 'RGBA', 'L']:
                    result["warnings"].append(f"非标准颜色模式: {img.mode}")
        except ImportError:
            result["warnings"].append("PIL 未安装，跳过 PNG 检查")
        except Exception as e:
            result["issues"].append(f"PNG 检查失败: {e}")

    return result


def check_color_palette(colors: list) -> dict:
    """
    检查配色方案是否符合出版标准

    Args:
        colors: 颜色列表 (hex 格式)

    Returns:
        检查结果
    """
    result = {
        "valid": True,
        "issues": [],
        "color_count": len(colors)
    }

    # 颜色数量检查
    if len(colors) > 10:
        result["warnings"].append(f"颜色过多 ({len(colors)} 种)，建议不超过 8 种")

    if len(colors) < 2:
        result["warnings"].append("颜色过少，无法区分多个类别")

    # 检查色盲友好性（简单检查）
    # 注意：完整检查需要色盲模拟器
    problematic_combos = [
        ('#000000', '#FFFFFF'),  # 纯黑纯白对比过强
    ]

    for combo in problematic_combos:
        if combo[0] in colors and combo[1] in colors:
            result["warnings"].append(f"检测到高对比度组合: {combo[0]} / {combo[1]}")

    return result


def validate_export_format(fig_path: str, target_format: str = 'pdf') -> dict:
    """
    验证导出格式是否符合期刊要求

    Args:
        fig_path: 文件路径
        target_format: 目标格式 (pdf/svg/tiff)

    Returns:
        验证结果
    """
    result = {
        "valid": True,
        "issues": [],
        "recommendations": []
    }

    fig_path = Path(fig_path)
    suffix = fig_path.suffix.lower()

    # 检查格式
    if suffix != f'.{target_format}':
        result["recommendations"].append(f"建议导出为 {target_format.upper()} 格式")

    # 期刊推荐格式
    journal_standards = {
        'nature': {'primary': '.pdf', 'secondary': '.tiff', 'min_resolution': 300},
        'cell': {'primary': '.pdf', 'secondary': '.tiff', 'min_resolution': 300},
        'science': {'primary': '.pdf', 'secondary': '.tiff', 'min_resolution': 300},
    }

    for journal, specs in journal_standards.items():
        if target_format in specs['primary'].replace('.', ''):
            result["recommendations"].append(f"{journal.capitalize()} 推荐使用 {specs['primary'].upper()} 主文件")
            break

    return result


if __name__ == "__main__":
    # 命令行使用示例
    if len(sys.argv) > 1:
        fig_path = sys.argv[1]
        results = check_figure_quality(fig_path)

        print(f"\n文件: {fig_path}")
        print(f"有效: {results['valid']}")

        if results['issues']:
            print("\n问题:")
            for issue in results['issues']:
                print(f"  ✗ {issue}")

        if results['warnings']:
            print("\n警告:")
            for warning in results['warnings']:
                print(f"  ! {warning}")

        if not results['issues'] and not results['warnings']:
            print("\n✓ 通过所有检查")
    else:
        print("Usage: python quality_check.py <figure_path>")
        print("\nExample:")
        print("  python quality_check.py figure.png")
