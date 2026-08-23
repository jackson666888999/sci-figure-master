"""
配色验证工具 - 检查配色方案是否符合出版标准和色盲友好性
"""

import sys
from pathlib import Path


def hex_to_rgb(hex_color: str) -> tuple:
    """将 hex 颜色转换为 RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """将 RGB 转换为 hex"""
    return f'#{r:02x}{g:02x}{b:02x}'


def get_relative_luminance(r: int, g: int, b: int) -> float:
    """计算相对亮度 (WCAG 2.1)"""
    # sRGB 线性化
    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)

    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def get_contrast_ratio(color1: str, color2: str) -> float:
    """计算两个颜色之间的对比度"""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    l1 = get_relative_luminance(r1, g1, b1)
    l2 = get_relative_luminance(r2, g2, b2)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def check_contrast_pair(color1: str, color2: str, min_ratio: float = 4.5) -> dict:
    """检查一对颜色的对比度"""
    ratio = get_contrast_ratio(color1, color2)

    return {
        "color1": color1,
        "color2": color2,
        "contrast_ratio": round(ratio, 2),
        "passes_AA": ratio >= 4.5,
        "passes_AAA": ratio >= 7.0,
        "status": "✓" if ratio >= min_ratio else "✗"
    }


def analyze_palette(colors: list) -> dict:
    """
    分析配色方案

    Args:
        colors: hex 颜色列表

    Returns:
        分析结果
    """
    results = {
        "colors": colors,
        "pairs": [],
        "issues": [],
        "warnings": [],
        "recommendations": []
    }

    # 检查颜色数量
    if len(colors) > 12:
        results["warnings"].append(f"颜色过多 ({len(colors)} 种)，建议用于分类数据时不超过 10 种")

    if len(colors) < 2:
        results["warnings"].append("颜色过少，无法区分多个类别")
        return results

    # 检查对比度
    for i, c1 in enumerate(colors):
        for j, c2 in enumerate(colors):
            if i < j:
                pair_result = check_contrast_pair(c1, c2)
                results["pairs"].append(pair_result)

                if pair_result["contrast_ratio"] < 3.0:
                    results["warnings"].append(
                        f"低对比度: {c1} vs {c2} ({pair_result['contrast_ratio']}:1)"
                    )

    # 检查常见色盲问题
    # 红绿色盲最常见，检查红色和绿色之间的区分度
    red_colors = [c for c in colors if hex_to_rgb(c)[0] > 150 and hex_to_rgb(c)[1] < 100]
    green_colors = [c for c in colors if hex_to_rgb(c)[1] > 150 and hex_to_rgb(c)[0] < 100]

    if red_colors and green_colors:
        for rc in red_colors:
            for gc in green_colors:
                ratio = get_contrast_ratio(rc, gc)
                if ratio < 4.5:
                    results["warnings"].append(
                        f"色盲风险: 红 {rc} 与绿 {gc} 对比度不足 ({ratio:.1f}:1)"
                    )

    # 推荐
    if results["warnings"]:
        results["recommendations"].append("考虑使用 Okabe-Ito 或 ColorBrewer 等色盲友好的配色方案")
        results["recommendations"].append("推荐使用: #0072B2 (蓝), #E69F00 (橙), #009E73 (绿)")

    return results


def print_palette_report(results: dict):
    """打印配色分析报告"""
    print("\n" + "=" * 60)
    print("配色分析报告")
    print("=" * 60)

    print(f"\n颜色数量: {len(results['colors'])}")
    print("颜色列表:")
    for i, color in enumerate(results['colors'], 1):
        print(f"  {i}. {color}")

    if results['pairs']:
        print(f"\n对比度检查 ({len(results['pairs'])} 对):")
        for pair in results['pairs']:
            status = "✓" if pair['passes_AA'] else "✗"
            print(f"  {status} {pair['color1']} vs {pair['color2']}: {pair['contrast_ratio']}:1")

    if results['issues']:
        print("\n问题:")
        for issue in results['issues']:
            print(f"  ✗ {issue}")

    if results['warnings']:
        print("\n警告:")
        for warning in results['warnings']:
            print(f"  ! {warning}")

    if results['recommendations']:
        print("\n建议:")
        for rec in results['recommendations']:
            print(f"  → {rec}")

    if not results['issues'] and not results['warnings']:
        print("\n✓ 配色方案良好")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 默认配色方案示例
    default_palette = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7', '#56B4E9']

    if len(sys.argv) > 1:
        colors = sys.argv[1:]
    else:
        colors = default_palette
        print("使用默认配色方案 (Okabe-Ito)")

    results = analyze_palette(colors)
    print_palette_report(results)
