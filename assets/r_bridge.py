#!/usr/bin/env python3
"""
R Bridge — 通过 Rscript 调用 R 包生成高质量图表
集成: ComplexHeatmap, EnhancedVolcano, ggtree, circlize, phyloseq 等
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List


class RBridge:
    """R 脚本执行桥接"""

    RSCRIPT = "Rscript"  # Windows 下通常在 PATH 中
    R_LIBS_USER = os.path.expanduser("~/.Rlibrary")

    @classmethod
    def is_available(cls) -> bool:
        """检查 R 是否可用"""
        try:
            result = subprocess.run(
                [cls.RSCRIPT, "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @classmethod
    def run_script(
        cls,
        r_code: str,
        output_path: str,
        packages: List[str] = None,
        timeout: int = 120
    ) -> Dict:
        """
        执行 R 代码并生成图表

        Args:
            r_code: R 代码字符串
            output_path: 输出文件路径
            packages: 需要安装的 R 包列表
            timeout: 超时时间（秒）

        Returns:
            {"status": "success" | "error", "output": str, "error": str}
        """
        # 生成临时 R 脚本
        with tempfile.NamedTemporaryFile(
            suffix=".R", mode="w", encoding="utf-8", delete=False
        ) as f:
            r_script = f.name

            # 写入 R 代码
            if packages:
                # 自动安装缺失的包
                f.write("pkgs <- c(" + ", ".join(f'"{p}"' for p in packages) + ")\n")
                f.write("for (pkg in pkgs) {\n")
                f.write("  if (!requireNamespace(pkg, quietly = TRUE)) {\n")
                f.write(f'    install.packages(pkg, repos="https://mirrors.tuna.tsinghua.edu.cn/CRAN/")\n')
                f.write("  }\n")
                f.write("}\n\n")

            f.write(r_code)
            f.write(f'\n\ncat("DONE:", output_path, "\\n")\n')

        try:
            result = subprocess.run(
                [cls.RSCRIPT, r_script],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, "R_LIBS_USER": cls.R_LIBS_USER}
            )

            output = result.stdout.strip()
            error = result.stderr.strip() if result.stderr else ""

            # 检查是否成功（返回码为 0 或输出包含 DONE）
            # 注意：包加载消息会写入 stderr，不是错误
            if result.returncode == 0 or "DONE:" in output or "null device" in output:
                return {"status": "success", "output": output, "error": error}
            else:
                return {"status": "error", "output": output, "error": error}

        except subprocess.TimeoutExpired:
            return {"status": "error", "output": "", "error": f"Timeout after {timeout}s"}
        except Exception as e:
            return {"status": "error", "output": "", "error": str(e)}
        finally:
            # 清理临时文件
            try:
                os.unlink(r_script)
            except:
                pass


# ─────────────────────────────────────────────────────────────
# R 图表生成函数
# ─────────────────────────────────────────────────────────────

def plot_complex_heatmap(
    data: list,
    output_path: str,
    title: str = "Complex Heatmap",
    row_names: list = None,
    col_names: list = None,
    **kwargs
) -> Dict:
    """
    生成 ComplexHeatmap 复合热图（R）

    Args:
        data: 二维数据矩阵（list of lists）
        output_path: 输出路径
        title: 图表标题
        row_names: 行名列表
        col_names: 列名列表
    """
    # 将 Python 数据转换为 R 数据框
    data_str = _python_to_r_matrix(data)
    r_script = f'''
library(ComplexHeatmap)
library(circlize)

# 数据矩阵
mat <- matrix({data_str}, nrow={len(data)}, ncol={len(data[0]) if data else 0})
rownames(mat) <- c({", ".join(f'"{n}"' for n in (row_names or [f"Gene{i}" for i in range(len(data))]))})
colnames(mat) <- c({", ".join(f'"{n}"' for n in (col_names or [f"Sample{i}" for i in range(len(data[0]) if data else 0)]))})

# 颜色映射
col_fun <- colorRamp2(c(-2, 0, 2), c("blue", "white", "red"))

# 绘图
png("{output_path.replace('.pdf', '.png')}", width=1200, height=800, res=150)
ht <- Heatmap(mat,
    name="{title}",
    col=col_fun,
    show_row_names=TRUE,
    show_column_names=TRUE,
    row_names_gp=gpar(fontsize=8),
    column_names_gp=gpar(fontsize=8)
)
draw(ht, heatmap_legend_side="right")
dev.off()
'''
    return RBridge.run_script(r_script, output_path, packages=["ComplexHeatmap", "circlize"])


def plot_enhanced_volcano(
    data: list,
    output_path: str,
    title: str = "Enhanced Volcano",
    gene_col: str = "gene",
    log2fc_col: str = "log2FC",
    pval_col: str = "pvalue",
    **kwargs
) -> Dict:
    """
    生成 EnhancedVolcano 火山图（R）

    Args:
        data: 差异表达数据列表
        output_path: 输出路径
        title: 图表标题
    """
    # 转换为 R data.frame
    if data and isinstance(data, list) and isinstance(data[0], dict):
        genes = [d.get(gene_col, d.get("gene", "")) for d in data]
        log2fcs = [d.get(log2fc_col, d.get("log2FC", 0)) for d in data]
        pvals = [d.get(pval_col, d.get("pvalue", 1)) for d in data]
    else:
        genes = log2fcs = pvals = []

    r_script = f'''
library(EnhancedVolcano)

# 数据
df <- data.frame(
  gene = c({", ".join(f'"{g}"' for g in genes)}),
  log2FC = c({", ".join(str(v) for v in log2fcs)}),
  P.Value = c({", ".join(str(v) for v in pvals)})
)

# 绘图
pdf("{output_path}", width=10, height=8)
EnhancedVolcano(df,
  lab = "gene",
  x = "log2FC",
  y = "P.Value",
  title = "{title}",
  pCutoff = 0.05,
  FCcutoff = 1,
  pointSize = 3,
  labSize = 3
)
dev.off()
'''
    return RBridge.run_script(r_script, output_path, packages=["EnhancedVolcano"])


def plot_circos_diagram(
    data: list,
    output_path: str,
    title: str = "Circos Diagram",
    **kwargs
) -> Dict:
    """
    生成 Circos 圈图（R）

    Args:
        data: 连接数据列表 [{"from": "...", "to": "...", "value": ...}]
        output_path: 输出路径
    """
    links_str = ", ".join(
        f'c("{d["from"]}", "{d["to"]}")'
        for d in (data or [])
    )
    r_script = f'''
library(circlize)

# 绘图区域
circos.initialize(factor.labels = c("A", "B", "C", "D", "E", "F"))

# 添加连线
if (length({data or []}) > 0) {{
  for (link in list({links_str})) {{
    circos.link(link[1], link[2])
  }}
}}

# 标题
title("{title}")
'''
    return RBridge.run_script(r_script, output_path, packages=["circlize"])


# ─────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────

def _python_to_r_matrix(data: list) -> str:
    """将 Python 二维列表转换为 R matrix 字符串"""
    rows = []
    for row in data:
        values = ", ".join(str(v) for v in row)
        rows.append(f"c({values})")
    return f"\n    {',\n    '.join(rows)}"


def plot_r(
    plot_type: str,
    data,
    output_path: str,
    **kwargs
) -> Dict:
    """
    统一 R 绘图入口

    Args:
        plot_type: 图型（"complex_heatmap" | "enhanced_volcano" | "circos" 等）
        data: 数据
        output_path: 输出路径
    """
    plot_funcs = {
        "complex_heatmap": plot_complex_heatmap,
        "enhanced_volcano": plot_enhanced_volcano,
        "circos": plot_circos_diagram,
    }
    func = plot_funcs.get(plot_type)
    if not func:
        return {"status": "error", "error": f"未知的 R 图型: {plot_type}"}
    return func(data, output_path, **kwargs)


# ─────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────

def check_r_available() -> bool:
    """检查 R 是否可用"""
    return RBridge.is_available()


def get_r_version() -> str:
    """获取 R 版本"""
    try:
        result = subprocess.run(
            [RBridge.RSCRIPT, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().split("\n")[0]
    except:
        return "Unknown"


if __name__ == "__main__":
    print("=== R Bridge 测试 ===")
    print(f"R 可用: {RBridge.is_available()}")
    print(f"R 版本: {get_r_version()}")
    print()

    # 测试复杂热图
    test_data = [
        [1.2, -0.5, 2.1],
        [-0.8, 1.5, 0.3],
        [0.9, -1.2, 1.8]
    ]
    result = plot_complex_heatmap(
        test_data,
        "test_heatmap.pdf",
        title="Test Complex Heatmap",
        row_names=["Gene1", "Gene2", "Gene3"],
        col_names=["Sample1", "Sample2", "Sample3"]
    )
    print(f"Complex Heatmap: {result['status']}")
