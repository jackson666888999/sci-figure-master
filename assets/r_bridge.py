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
mat <- matrix(c({data_str}), nrow={len(data)}, ncol={len(data[0]) if data else 0}, byrow=TRUE)
rownames(mat) <- c({", ".join(f'"{n}"' for n in (row_names or [f"Gene{i}" for i in range(len(data))]))})
colnames(mat) <- c({", ".join(f'"{n}"' for n in (col_names or [f"Sample{i}" for i in range(len(data[0]) if data else 0)]))})

# 颜色映射
col_fun <- colorRamp2(c(-2, 0, 2), c("blue", "white", "red"))

# 输出设备（依据后缀）
out_ext <- tolower(substr("{output_path}", nchar("{output_path}") - 3, nchar("{output_path}")))
if (out_ext == ".png") {{
  png("{output_path}", width = 1200, height = 800, res = 150)
}} else if (out_ext == ".svg") {{
  svg("{output_path}", width = 10, height = 8)
}} else {{
  pdf("{output_path}", width = 10, height = 8)
}}
ht <- Heatmap(mat,
    name = "{title}",
    col = col_fun,
    show_row_names = TRUE,
    show_column_names = TRUE,
    row_names_gp = gpar(fontsize = 8),
    column_names_gp = gpar(fontsize = 8)
)
draw(ht, heatmap_legend_side = "right")
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

    r_script = f"""
library(EnhancedVolcano)

# 数据
df <- data.frame(
  gene = c({", ".join(f'"{g}"' for g in genes)}),
  log2FC = c({", ".join(str(v) for v in log2fcs)}),
  P.Value = c({", ".join(str(v) for v in pvals)})
)

# 绘图
out_file <- "{output_path}"
pdf(out_file, width=10, height=8)
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
"""
    return RBridge.run_script(r_script, output_path, packages=["EnhancedVolcano"])


def plot_ma_plot(
    data: list,
    output_path: str,
    title: str = "MA Plot",
    log2fc_col: str = "log2FC",
    base_mean_col: str = "AveExpr",
    **kwargs
) -> Dict:
    """
    生成 MA 图（R ggplot2）

    Args:
        data: 差异表达数据列表（需含 log2FC 和 AveExpr 列）
        output_path: 输出路径
        title: 图表标题
    """
    log2fcs = [d.get(log2fc_col, 0) for d in data]
    base_means = [d.get(base_mean_col, 0) for d in data]
    genes = [str(d.get("feature_id", d.get("gene", f"feat{i}"))) for i, d in enumerate(data)]

    # 取前 5000 个点避免过大
    if len(log2fcs) > 5000:
        idx = list(range(5000))
        import random; random.seed(42)
        idx = random.sample(range(len(log2fcs)), 5000)
        log2fcs = [log2fcs[i] for i in idx]
        base_means = [base_means[i] for i in idx]
        genes = [genes[i] for i in idx]

    r_script = f"""
library(ggplot2)
library(ggrepel)

# 数据
df <- data.frame(
  baseMean = c({", ".join(str(v) for v in base_means)}),
  log2FC = c({", ".join(str(v) for v in log2fcs)}),
  gene = c({", ".join(f'"{g}"' for g in genes)})
)
df$baseMean <- as.numeric(df$baseMean)
df$log2FC <- as.numeric(df$log2FC)

# 过滤极端值
df <- df[is.finite(df$baseMean) & is.finite(df$log2FC), ]

# 绘图
out_file <- "{output_path}"
pdf(out_file, width=10, height=8)
ggplot(df, aes(x=baseMean, y=log2FC)) +
  geom_point(alpha=0.4, size=0.8, color="#666666") +
  geom_hline(yintercept=0, linetype="solid", color="black", linewidth=0.5) +
  geom_hline(yintercept=c(-1, 1), linetype="dashed", color="gray", linewidth=0.5) +
  scale_x_log10(labels=scales::label_number()) +
  labs(title="{title}", x="Base Mean (log10)", y="log2 Fold Change") +
  theme_minimal() +
  theme(plot.title=element_text(hjust=0.5, face="bold"),
        axis.text=element_text(size=8),
        axis.title=element_text(size=10))
dev.off()
"""
    return RBridge.run_script(r_script, output_path, packages=["ggplot2", "ggrepel"])


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
# 扩展 R 图型：ggtree / phyloseq / clusterProfiler
# ─────────────────────────────────────────────────────────────

def plot_ggtree(
    data: str,
    output_path: str,
    title: str = "Phylogenetic Tree",
    tree_format: str = "newick",
    **kwargs
) -> Dict:
    """
    ggtree 系统发育树（R）
    data: Newick 字符串 或 树文件路径；若为路径则直接读取
    """
    import os as _os
    if _os.path.exists(str(data)):
        tree_src = f'read.tree("{data}")'
    else:
        # 写入临时 newick
        import tempfile as _tmp
        fd, tp = _tmp.mkstemp(suffix=".nwk")
        with _open(fd, "w") as _f:
            _f.write(str(data))
        tree_src = f'read.tree("{tp}")'

    r_script = f'''
library(ggtree)
library(ggplot2)

tree <- {tree_src}
p <- ggtree(tree) + geom_tiplab(size = 3) + ggtitle("{title}")
ggsave("{output_path}", p, width = 10, height = 8, dpi = 300)
cat("DONE:", "{output_path}", "\\n")
'''
    return RBridge.run_script(r_script, output_path, packages=["ggtree", "ggplot2"])


def plot_phyloseq(
    data: dict,
    output_path: str,
    plot_kind: str = "ord_nmds",   # ord_nmds | ord_pcoa | bar | alpha
    group_col: str = "Group",
    **kwargs
) -> Dict:
    """
    phyloseq 微生物组可视化（R）
    data: {"otu_table": [[...]], "tax_table": [...], "sample_names": [...], "groups": [...]}
    """
    otu = data.get("otu_table", [])
    sample_names = data.get("sample_names", [f"S{i+1}" for i in range(len(otu[0]) if otu else 0)])
    groups = data.get("groups", ["G1"] * len(sample_names))
    # 构造 phyloseq 对象的最小 R 代码（从矩阵 + 样本数据）
    otu_str = _python_to_r_matrix(otu)
    sample_df = ", ".join(f'"{g}"' for g in groups)
    r_script = f'''
library(phyloseq)
library(ggplot2)

otu.mat <- matrix(c({otu_str}), nrow = {len(otu)}, byrow = TRUE,
                  dimnames = list(NULL, c({", ".join(chr(34)+s+chr(34) for s in sample_names)})))
sample.df <- data.frame(Sample = c({", ".join(chr(34)+s+chr(34) for s in sample_names)}),
                        {group_col} = factor(c({sample_df})),
                        row.names = c({", ".join(chr(34)+s+chr(34) for s in sample_names)}))
sam <- sample_data(sample.df)
otu <- otu_table(otu.mat, taxa_are_rows = TRUE)
ps <- phyloseq(otu, sam)

p <- plot_{plot_kind}(ps, color = "{group_col}")
ggsave("{output_path}", p, width = 8, height = 6, dpi = 300)
cat("DONE:", "{output_path}", "\\n")
'''
    return RBridge.run_script(r_script, output_path, packages=["phyloseq", "ggplot2"])


def plot_clusterprofiler(
    data: list,
    output_path: str,
    plot_kind: str = "dotplot",   # dotplot | enrichment_map | cnetplot | barplot
    title: str = "Enrichment",
    **kwargs
) -> Dict:
    """
    clusterProfiler 富集分析可视化（R）
    data: [{"term":..., "pvalue":..., "gene":[...], "count":...}, ...]
    """
    terms = [d.get("term", f"T{i}") for i, d in enumerate(data)]
    pvals = [d.get("pvalue", 0.05) for d in data]
    genes = [d.get("gene", []) for d in data]
    counts = [d.get("count", len(g)) for g in genes]

    term_str = ", ".join(f'"{t}"' for t in terms)
    pval_str = ", ".join(str(p) for p in pvals)
    count_str = ", ".join(str(c) for c in counts)
    gene_str = ", ".join(
        'c(' + ", ".join(f'"{g}"' for g in gl) + ')' for gl in genes
    )

    r_script = f'''
library(clusterProfiler)
library(ggplot2)
library(enrichplot)

# 构造富集结果对象（简化）
yy <- data.frame(
  Description = c({term_str}),
  pvalue = c({pval_str}),
  Count = c({count_str}),
  geneID = c({gene_str})
)
# 模拟 enrichResult 结构（绘图接口兼容）
rownames(yy) <- yy$Description
yy$geneID <- sapply(yy$geneID, function(x) paste(unlist(x), collapse = "/"))

p <- {plot_kind}(yy, showCategory = {min(20, len(data))})
ggsave("{output_path}", p, width = 9, height = 7, dpi = 300)
cat("DONE:", "{output_path}", "\\n")
'''
    return RBridge.run_script(r_script, output_path, packages=["clusterProfiler", "enrichplot", "ggplot2"])


# ─────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────

def _python_to_r_matrix(data: list) -> str:
    """将 Python 二维列表转换为 R matrix 的扁平 data 向量字符串"""
    flat = []
    for row in data:
        for v in row:
            flat.append(str(v))
    return ", ".join(flat)


def plot_r(
    plot_type: str,
    data,
    output_path: str,
    **kwargs
) -> Dict:
    """
    统一 R 绘图入口

    Args:
        plot_type: 图型（"complex_heatmap" | "enhanced_volcano" | "circos" |
                          "ggtree" | "phyloseq" | "clusterprofiler"）
        data: 数据
        output_path: 输出路径
    """
    plot_funcs = {
        "complex_heatmap": plot_complex_heatmap,
        "enhanced_volcano": plot_enhanced_volcano,
        "ma_plot": plot_ma_plot,
        "circos": plot_circos_diagram,
        "ggtree": plot_ggtree,
        "phyloseq": plot_phyloseq,
        "clusterprofiler": plot_clusterprofiler,
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
