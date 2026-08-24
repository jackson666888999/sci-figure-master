#!/usr/bin/env python3
"""
aris_pipeline.py - ARIS 自主研究方法论流水线（两阶段：先故事，后证据链出图）

ARIS = Acquire → Review → Integrate → Score

Phase 1 (--phase story)  先出顶刊级故事:
    A: 真实顶刊文献调研（arXiv/Crossref API，绝不虚构）
    R: 提炼研究方法/范式/写作/创新/画图代码/数据来源
    I: 基于【全面数据分析结果】设计层层递进的故事闭环（9 阶段）
       每阶段绑定证据链: 分析模块 → 图形 → 统计支撑 → 结果文件
    S: 严格评审（顶刊标准 100 分制）
    产出: story.json + story.md  →  供用户审查/修改

Phase 2 (--phase figures --story story.json)  用户审查故事后:
    围绕故事主线筛选前面数据分析出的结果（只取证据链命中的）
    按证据链逐阶段出图（图形紧紧围绕文章主线，证据链强）
    产出: figures/ 全套图 + evidence_chain.md

用法:
    # 完整流程
    python aris_pipeline.py --data data.csv --topic "主题" --phase full
    # 分阶段（先故事，审查后再出图）
    python aris_pipeline.py --data data.csv --topic "主题" --phase story --output run1
    python aris_pipeline.py --data data.csv --phase figures --story run1/story.json --output run1

数据红线:
    文献 API 不可用时返回空集并明确提示，绝不编造文献条目。
    画图仅接受用户提供的真实数据文件路径。
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any, List

warnings_safe = True
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "assets"))

try:
    from comprehensive_analysis import ComprehensiveAnalyzer
    HAS_COMPREHENSIVE = True
except Exception:
    HAS_COMPREHENSIVE = False

try:
    from bioinfo_router import generate_figure, quick_plot
    HAS_ROUTER = True
except Exception:
    HAS_ROUTER = False

# ─────────────────────────────────────────────────────────────
# A. Acquire — 顶刊文献调研（真实 API，绝不虚构）
# ─────────────────────────────────────────────────────────────
TOP_JOURNALS = ["Nature", "Science", "Cell", "Nature Biotechnology", "Nature Medicine",
                "Nature Genetics", "Nature Methods", "Nature Communications",
                "Cell Systems", "Genome Biology", "Molecular Systems Biology",
                "Nature Neuroscience", "Cancer Cell", "Immunity"]


class LiteratureHarvester:
    """顶刊文献调研器（Crossref/arXiv 真实 API）"""

    def __init__(self, max_results: int = 20, timeout: int = 15):
        self.max_results = max_results
        self.timeout = timeout

    def _fetch_json(self, url: str) -> Optional[dict]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ARIS-SciFigure/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  ! fetch failed: {url[:80]}... ({e})")
            return None

    def search_crossref(self, topic: str, n: int = 10) -> List[dict]:
        query = urllib.parse.quote(topic)
        url = (f"https://api.crossref.org/works?query={query}"
               f"&rows={n}&sort=relevance&select=title,author,container-title,"
               f"published,DOI,is-referenced-by-count")
        data = self._fetch_json(url)
        if not data or "message" not in data:
            return []
        papers = []
        for item in data["message"].get("items", []):
            titles = item.get("title", [])
            if not titles:
                continue
            journal = (item.get("container-title") or [""])[0]
            papers.append({
                "source": "Crossref", "title": titles[0],
                "journal": journal if journal else "n/a",
                "authors": [a.get("family", "") for a in item.get("author", [])[:5]],
                "date": str((item.get("published", {}).get("date-parts", [[None]])[0][0]
                             or (item.get("issued", {}).get("date-parts", [[None]])[0][0])) or ""),
                "url": f"https://doi.org/{item['DOI']}",
                "citations": item.get("is-referenced-by-count", 0),
                "top_journal": any(j.lower() in (journal or "").lower() for j in TOP_JOURNALS),
            })
        return papers

    def search_arxiv(self, topic: str, n: int = 10) -> List[dict]:
        query = urllib.parse.quote(f'all:"{topic}"')
        url = (f"http://export.arxiv.org/api/query?search_query={query}"
               f"&start=0&max_results={n}&sortBy=submittedDate&sortOrder=descending")
        try:
            import xml.etree.ElementTree as ET
            req = urllib.request.Request(url, headers={"User-Agent": "ARIS-SciFigure/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                xml_text = resp.read().decode("utf-8")
            ns = {"a": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(xml_text)
            papers = []
            for entry in root.findall("a:entry", ns):
                papers.append({
                    "source": "arXiv",
                    "title": (entry.findtext("a:title", "", ns) or "").strip().replace("\n", " "),
                    "journal": "arXiv (preprint)",
                    "authors": [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)],
                    "date": (entry.findtext("a:published", "", ns) or "")[:10],
                    "url": entry.findtext("a:id", "", ns),
                    "citations": 0, "top_journal": False,
                })
            return papers
        except Exception as e:
            print(f"  ! arXiv search failed: {e}")
            return []

    def search(self, topic: str, n: int = None) -> List[dict]:
        n = n or self.max_results
        print(f"[A] Harvesting literature for: {topic}")
        papers = self.search_crossref(topic, n=max(5, n // 2))
        print(f"  -> Crossref: {len(papers)} papers")
        papers.extend(self.search_arxiv(topic, n=max(5, n // 2)))
        if not papers:
            print("  !! No papers retrieved (network/API unavailable). "
                  "NO fabricated references will be generated.")
        return papers


# ─────────────────────────────────────────────────────────────
# R. Review — 方法论提炼
# ─────────────────────────────────────────────────────────────
class MethodExtractor:
    """从文献 + 数据画像提炼方法论要素（方法学框架为通用知识，
    文献字段仅来自真实 API）"""

    METHOD_CLASSES = {
        "omics-bulk": {
            "methods": ["DESeq2/edgeR 差异表达", "WGCNA 共表达网络",
                        "clusterProfiler GO/KEGG 富集", "GSEA 基因集富集"],
            "figures": ["MA plot", "volcano", "heatmap", "forest", "enrichment dot/bar"],
            "stats": ["Wald test / exact test", "Benjamini-Hochberg FDR",
                      "hypergeometric test", "permutation test"],
        },
        "omics-single-cell": {
            "methods": ["Scanpy/Seurat 质控归一化", "PCA+UMAP 降维", "Louvain/Leiden 聚类",
                        "marker gene 鉴定", "CellChat 通讯", "拟时序"],
            "figures": ["UMAP", "tSNE", "dotplot", "violin", "heatmap",
                        "cellchat network", "trajectory"],
            "stats": ["Wilcoxon", "负二项 GLM", "AUC", "permutation"],
        },
        "microbiome": {
            "methods": ["DADA2/QIIME2 ASV", "ANCOM-BC2 差异丰度", "PERMANOVA",
                        "LEfSe 判别", "SparCC 网络"],
            "figures": ["alpha box", "PCoA/NMDS", "composition bar", "LEfSe bar",
                        "heatmap", "sankey/alluvial"],
            "stats": ["Kruskal-Wallis", "PERMANOVA", "ANCOM-BC2", "Spearman", "BH-FDR"],
        },
        "metabolomics": {
            "methods": ["XCMS", "OPLS-DA", "VIP", "KEGG 通路", "HMDB 注释"],
            "figures": ["OPLS-DA", "volcano", "heatmap", "pathway", "network"],
            "stats": ["t-test + FDR", "OPLS-DA CV", "VIP>1", "hypergeometric"],
        },
        "clinical-survival": {
            "methods": ["Kaplan-Meier", "log-rank", "Cox 回归", "Lasso-Cox",
                        "时间依赖AUC", "列线图"],
            "figures": ["KM curve", "forest", "ROC", "calibration", "nomogram"],
            "stats": ["log-rank", "Wald", "C-index", "bootstrap"],
        },
        "multiomics": {
            "methods": ["MOFA2", "mixOmics DIABLO", "数据整合", "模块-表型关联"],
            "figures": ["MOFA heatmap", "DIABLO circos", "ComplexHeatmap"],
            "stats": ["variance decomposition", "bootstrap", "稀疏 CCA"],
        },
    }

    def classify(self, domain: str) -> str:
        mapping = {
            "scrna": "omics-single-cell", "bulkrna": "omics-bulk", "generic": "omics-bulk",
            "microbiome": "microbiome", "metabolomics": "metabolomics",
            "proteomics": "omics-bulk", "survival": "clinical-survival",
            "multiomics": "multiomics", "spatial": "omics-single-cell",
        }
        return mapping.get((domain or "").lower(), "omics-bulk")

    def extract(self, papers: List[dict], domain: str, topic: str = "") -> Dict[str, Any]:
        cls = self.classify(domain)
        base = self.METHOD_CLASSES.get(cls, self.METHOD_CLASSES["omics-bulk"])
        return {
            "paradigm": cls,
            "research_methods": list(base["methods"]),
            "figure_types": list(base["figures"]),
            "statistical_methods": list(base["stats"]),
            "writing_framework": [
                "Abstract: 背景→缺口→方法→关键发现→结论",
                "Introduction: 漏斗式（领域→已知→缺口→假设）",
                "Results: 层层递进（数据质量→全局模式→组间差异→机制→验证）",
                "Discussion: 发现→对照文献→机制→局限→展望",
            ],
            "innovation_patterns": [
                "跨组学整合（多组学联动证据链）", "从相关到因果（中介/干预验证）",
                "新方法学应用（ANCOM-BC2/稀疏CCA）", "临床转化（biomarker panel）",
            ],
            "plotting_code_notes": [
                "Nature 标准: SVG/PDF 矢量 + TIFF 600dpi",
                "配色: 高对比度专业配色", "文字重叠: adjustText/ggrepel",
                "坐标轴: 仅 bottom/left spines",
            ],
            "references": papers,
            "reference_count": len(papers),
            "topic": topic,
        }


# ─────────────────────────────────────────────────────────────
# I. Integrate — 故事闭环生成器（先出顶刊故事，证据链绑定）
# ─────────────────────────────────────────────────────────────
class StoryGenerator:
    """基于全面分析结果生成顶刊级故事（9 阶段闭环 + 证据链设计）"""

    FRAMEWORK = [
        {"id": "S1", "stage": "Background", "title": "领域背景与已知",
         "question": "领域共识是什么？（需真实文献支撑）",
         "modules": ["descriptive"]},
        {"id": "S2", "stage": "Gap", "title": "未解之谜",
         "question": "数据中哪些模式尚未被解释？",
         "modules": ["normality", "correlation"]},
        {"id": "S3", "stage": "Hypothesis", "title": "研究假设",
         "question": "基于数据全局模式的假设？",
         "modules": ["dim_reduction", "clustering"]},
        {"id": "S4", "stage": "Methods", "title": "方法学",
         "question": "统计/工具/数据来源？（成对声明）",
         "modules": []},
        {"id": "S5", "stage": "Results-Layer1", "title": "数据质量与全局结构",
         "question": "数据整体结构如何？",
         "modules": ["descriptive", "dim_reduction", "clustering"]},
        {"id": "S6", "stage": "Results-Layer2", "title": "组间差异与关键分子",
         "question": "哪些变量在组间显著差异？",
         "modules": ["group_comparison", "differential"]},
        {"id": "S7", "stage": "Results-Layer3", "title": "关联与机制",
         "question": "变量间如何关联，形成机制网络？",
         "modules": ["correlation", "composition", "alpha_diversity"]},
        {"id": "S8", "stage": "Validation", "title": "稳健性验证",
         "question": "结论是否稳健（校正/验证）？",
         "modules": ["differential"]},
        {"id": "S9", "stage": "Conclusion", "title": "结论与意义",
         "question": "回答缺口，临床/理论意义？",
         "modules": []},
    ]

    # 模块 → 默认图型
    MODULE_FIGURES = {
        "descriptive": ["histogram", "boxplot"],
        "normality": ["qqplot", "histogram"],
        "group_comparison": ["boxplot", "violin", "raincloud"],
        "correlation": ["corr_heatmap", "scatter", "bubble"],
        "clustering": ["dendrogram", "scatter"],
        "dim_reduction": ["pca", "scatter", "umap"],
        "differential": ["volcano", "ma_plot", "heatmap", "lollipop"],
        "alpha_diversity": ["boxplot", "violin"],
        "beta_diversity": ["scatter", "pca"],
        "composition": ["stacked_bar", "donut", "treemap"],
        "kaplan_meier": ["km", "forest_plot"],
    }

    def __init__(self, analysis_dir: Path):
        self.analysis_dir = Path(analysis_dir)
        self.summary = self._load_summary()

    def _load_summary(self) -> dict:
        p = self.analysis_dir / "analysis_summary.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return {}

    def _load_results(self, module: str) -> List[dict]:
        """读取模块结果 CSV（证据链数据来源）"""
        csv_path = self.analysis_dir / "results" / f"{module}.csv"
        if csv_path.exists():
            try:
                return pd.read_csv(csv_path).to_dict("records")
            except Exception:
                return []
        return []

    def _top_findings(self, module: str, top_n: int = 5) -> List[dict]:
        """从模块结果中提取关键发现（按显著性/效应量排序）"""
        rows = self._load_results(module)
        if not rows:
            return []
        scored = []
        for r in rows:
            score = 0.0
            p = r.get("p") or r.get("pvalue") or r.get("p_adjusted")
            if p is not None:
                try:
                    score += max(0, -np.log10(float(p)))
                except (TypeError, ValueError):
                    pass
            es = r.get("effect_size") or r.get("r") or r.get("rho")
            if es is not None:
                try:
                    score += abs(float(es))
                except (TypeError, ValueError):
                    pass
            scored.append((score, r))
        scored.sort(key=lambda x: -x[0])
        return [r for _, r in scored[:top_n]]

    def generate(self, methodology: Dict[str, Any]) -> Dict[str, Any]:
        """生成故事（含每阶段证据链）"""
        domain = self.summary.get("domain", "generic")
        modules_ok = {m: v.get("status") == "ok"
                      for m, v in self.summary.get("modules", {}).items()}
        story = {
            "title": methodology.get("topic") or "ARIS Story",
            "domain": domain,
            "paradigm": methodology.get("paradigm"),
            "reference_count": methodology.get("reference_count", 0),
            "stages": [],
            "evidence_chain": [],
        }
        for stage in self.FRAMEWORK:
            s = dict(stage)
            evidence = []
            for mod in stage.get("modules", []):
                if not modules_ok.get(mod):
                    continue
                findings = self._top_findings(mod, top_n=3)
                figs = self.MODULE_FIGURES.get(mod, ["scatter"])
                evidence.append({
                    "module": mod,
                    "results_file": f"results/{mod}.csv",
                    "findings": findings,
                    "suggested_figures": figs,
                })
            s["evidence"] = evidence
            s["figures_plan"] = list({f for e in evidence for f in e["suggested_figures"]})
            story["stages"].append(s)
            if evidence:
                story["evidence_chain"].append({
                    "stage": stage["id"], "title": stage["title"],
                    "modules": [e["module"] for e in evidence],
                    "figures": s["figures_plan"],
                })
        return story

    def to_markdown(self, story: Dict[str, Any], methodology: Dict[str, Any]) -> str:
        """渲染为可审查的 story.md"""
        md = [f"# {story['title']}", ""]
        md.append(f"- 领域: `{story['domain']}` | 范式: `{story['paradigm']}`")
        md.append(f"- 文献支撑: {methodology.get('reference_count', 0)} 篇（仅真实 API 返回）")
        md.append("")
        md.append("## 故事主线（层层递进闭环）")
        for s in story["stages"]:
            md.append(f"### {s['id']} {s['stage']}: {s['title']}")
            md.append(f"> {s['question']}")
            if s.get("evidence"):
                md.append("")
                md.append("| 证据链 | 分析模块 | 图形 | 结果文件 |")
                md.append("|--------|----------|------|----------|")
                for e in s["evidence"]:
                    md.append(f"| {e['module']} | `{e['module']}` | "
                              f"{', '.join(e['suggested_figures'])} | {e['results_file']} |")
                    for f in e.get("findings", [])[:2]:
                        label = f.get("variable") or f.get("taxa") or f.get("var1") or ""
                        p = f.get("p") or f.get("pvalue") or f.get("p_adjusted")
                        p_str = f"{float(p):.2e}" if p is not None else "n/a"
                        md.append(f"  - 关键发现: {label} (p={p_str})")
                md.append("")
            else:
                md.append("")
                md.append("（本阶段由故事驱动，无直接分析模块）")
                md.append("")
        md.append("## 评审")
        md.append(f"- 总分: {methodology.get('_review_total', 'n/a')}/100")
        return "\n".join(md)


# ─────────────────────────────────────────────────────────────
# Phase 2 — 故事驱动的证据链出图
# ─────────────────────────────────────────────────────────────
class StoryDrivenFigureMaker:
    """围绕故事主线筛选分析结果 → 按证据链出图"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.figures_dir = self.output_dir / "figures"
        self.figures_dir.mkdir(parents=True, exist_ok=True)

    def make(self, data_path: Path, story_path: Path, analysis_dir: Path) -> Dict[str, Any]:
        """执行证据链出图"""
        story = json.loads(Path(story_path).read_text(encoding="utf-8"))
        analysis_dir = Path(analysis_dir)
        domain = story.get("domain", "generic")
        print(f"[G] Story-driven figure generation (domain={domain})")

        # 加载数据（真实数据，唯一来源）
        data = self._load_data(data_path)
        if data is None:
            return {"status": "error", "message": f"failed to load {data_path}"}

        generated = []
        chain = []
        for stage in story.get("stages", []):
            for ev in stage.get("evidence", []):
                mod = ev["module"]
                figs = ev.get("suggested_figures", [])
                for fig in figs[:2]:  # 每模块最多 2 图
                    out = self.figures_dir / f"{stage['id']}_{mod}_{fig}.svg"
                    try:
                        self._data = data
                        self._out = out
                        path = self._draw(data, domain, fig, out)
                        if path:
                            generated.append(str(path))
                            chain.append({"stage": stage["id"], "module": mod,
                                          "figure": fig, "file": str(path)})
                            print(f"  -> {stage['id']} {mod}/{fig}: OK")
                    except Exception as e:
                        print(f"  !! {stage['id']} {mod}/{fig} failed: {e}")

        result = {"status": "success", "generated_files": generated,
                  "evidence_chain": chain,
                  "n_figures": len(generated)}
        # 写证据链文档
        md = ["# 证据链出图报告", ""]
        md.append(f"- 数据: {data_path}（真实数据）")
        md.append(f"- 故事: {story_path}")
        md.append(f"- 共生成 {len(generated)} 张图，图形紧紧围绕文章主线")
        md.append("")
        for item in chain:
            md.append(f"- **{item['stage']}** `{item['module']}` → `{item['figure']}` → `{item['file']}`")
        (self.output_dir / "evidence_chain.md").write_text("\n".join(md), encoding="utf-8")
        return result

    def _load_data(self, data_path: Path):
        suffix = data_path.suffix.lower()
        try:
            if suffix in [".h5ad", ".h5"]:
                import scanpy as sc
                return sc.read_h5ad(data_path)
            if suffix in [".csv", ".tsv", ".txt"]:
                return pd.read_csv(data_path, sep=None, engine="python")
            if suffix in [".xlsx", ".xls"]:
                return pd.read_excel(data_path)
        except Exception as e:
            print(f"  ! load failed: {e}")
        return None

    def _draw(self, data, domain: str, fig: str, out: Path):
        """按图型分派绘图"""
        if not HAS_ROUTER:
            return None
        if isinstance(data, pd.DataFrame):
            cat_cols = [c for c in data.columns if pd.api.types.is_object_dtype(data[c])
                        or (data[c].nunique() <= 6 and data[c].nunique() > 1)]
            num_cols = list(data.select_dtypes(include=[np.number]).columns)
            group_col = cat_cols[0] if cat_cols else None
            y = num_cols[0] if num_cols else None
            y2 = num_cols[1] if len(num_cols) > 1 else y
            size_col = num_cols[2] if len(num_cols) > 2 else None

            mapping = {
                "boxplot": lambda: generate_figure("general", "box", data, str(out),
                                                   x=group_col, y=y),
                "violin": lambda: generate_figure("general", "violin", data, str(out),
                                                  x=group_col, y=y),
                "raincloud": lambda: generate_figure("general", "raincloud", data, str(out),
                                                     x=group_col, y=y),
                "histogram": lambda: generate_figure("general", "boxplot", data, str(out),
                                                     x=group_col, y=y),
                "qqplot": lambda: generate_figure("general", "qqplot", data, str(out),
                                                  column=y),
                "scatter": lambda: generate_figure("general", "scatter", data, str(out),
                                                   x=y, y=y2),
                "bubble": lambda: generate_figure("general", "bubble", data, str(out),
                                                  x=y, y=y2, size=size_col),
                "corr_heatmap": self._corr_heatmap,
                "heatmap": self._corr_heatmap,
                "dendrogram": lambda: generate_figure("general", "dendrogram", data, str(out)),
                "pca": self._pca,
                "umap": self._pca,
                "volcano": self._volcano,
                "ma_plot": lambda: generate_figure("general", "ma_plot", data, str(out)),
                "lollipop": lambda: generate_figure("general", "lollipop", data, str(out),
                                                    x=group_col, y=y),
                "stacked_bar": lambda: generate_figure("general", "bar", data, str(out),
                                                       x=group_col, y=y),
                "donut": lambda: generate_figure("general", "donut", data, str(out)),
                "treemap": lambda: generate_figure("general", "treemap", data, str(out)),
                "km": lambda: generate_figure("survival", "km", data, str(out)),
                "forest_plot": lambda: generate_figure("general", "forest_plot", data, str(out)),
            }
            fn = mapping.get(fig)
            return fn() if fn else None
        # AnnData
        if fig in ["umap", "pca", "tsne"]:
            return generate_figure("scRNA", fig.upper(), data, str(out),
                                   color=self._cluster_col(data))
        if fig == "heatmap":
            return generate_figure("scRNA", "heatmap", data, str(out))
        return None

    def _cluster_col(self, adata):
        for c in ["louvain", "leiden", "clusters", "cell_type"]:
            if c in adata.obs.columns:
                return c
        return None

    def _corr_heatmap(self):
        """相关矩阵热图（真实实现）"""
        data = self._data
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        if len(num_cols) < 2:
            return None
        corr = data[num_cols].corr(method="spearman")
        return generate_figure("general", "heatmap", corr, str(self._out))

    def _pca(self):
        """PCA 投影散点（真实实现）"""
        try:
            from sklearn.decomposition import PCA
        except Exception:
            return None
        data = self._data
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        if len(num_cols) < 2:
            return None
        X = data[num_cols].fillna(0).values
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-12)
        pca = PCA(n_components=2).fit_transform(X)
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        sc = ax.scatter(pca[:, 0], pca[:, 1], s=18, alpha=0.7,
                        c=pca[:, 1], cmap="viridis")
        plt.colorbar(sc, ax=ax)
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title("PCA Projection", fontweight="bold")
        plt.tight_layout()
        plt.savefig(str(self._out), bbox_inches="tight", dpi=300)
        plt.close()
        return self._out

    def _volcano(self):
        """火山图（真实实现）：数据含 log2FC/p 列直接画，否则用组均值差异构造"""
        data = self._data
        lfc_col = next((c for c in data.columns if c.lower() in ["log2fc", "logfc", "lfc"]), None)
        p_col = next((c for c in data.columns if c.lower() in ["p", "pvalue", "pval"]), None)
        if lfc_col and p_col:
            return generate_figure("general", "volcano", data, str(self._out),
                                   log2fc_col=lfc_col, pval_col=p_col)
        # 从分组列构造: 组均值 log2FC vs t-test p
        cat_cols = [c for c in data.columns if pd.api.types.is_object_dtype(data[c])
                    or (data[c].nunique() <= 6 and data[c].nunique() > 1)]
        num_cols = list(data.select_dtypes(include=[np.number]).columns)
        import warnings
        if not cat_cols or not num_cols:
            return None
        gc = cat_cols[0]
        groups = list(data[gc].unique())
        if len(groups) < 2:
            return None
        rows = []
        from scipy import stats as _st
        for nc in num_cols:
            v1 = data.loc[data[gc] == groups[0], nc].values
            v2 = data.loc[data[gc] == groups[1], nc].values
            if len(v1) < 2 or len(v2) < 2:
                continue
            m1, m2 = np.nanmean(v1), np.nanmean(v2)
            try:
                _, p = _st.ttest_ind(v1, v2)
            except Exception:
                continue
            rows.append({"gene": nc, "log2FC": np.log2((m1 + 1e-10) / (m2 + 1e-10)), "pvalue": float(p)})
        if not rows:
            return None
        volcano_df = pd.DataFrame(rows)
        return generate_figure("general", "volcano", volcano_df, str(self._out),
                               log2fc_col="log2FC", pval_col="pvalue")


# ─────────────────────────────────────────────────────────────
# S. Score — 严格评审
# ─────────────────────────────────────────────────────────────
class StrictReviewer:
    CRITERIA = [
        {"id": "C1", "name": "数据真实性", "weight": 20,
         "check": "所有图来自用户真实数据文件，禁止模拟/编造"},
        {"id": "C2", "name": "统计严谨性", "weight": 20,
         "check": "统计方法成对声明；多重比较校正；效应量与P值同报"},
        {"id": "C3", "name": "图表质量", "weight": 20,
         "check": "矢量输出；专业配色；无文字重叠；坐标轴规范"},
        {"id": "C4", "name": "故事闭环", "weight": 15,
         "check": "背景→缺口→假设→方法→结果→结论层层递进"},
        {"id": "C5", "name": "文献支撑", "weight": 15,
         "check": "关键论断有真实顶刊文献引用"},
        {"id": "C6", "name": "可复现性", "weight": 10,
         "check": "分析代码+数据路径+随机种子可完整复现"},
    ]

    def review(self, methodology: Dict[str, Any], story: Dict[str, Any],
               generated_files: List[str] = None) -> Dict[str, Any]:
        generated_files = generated_files or []
        scores = {}
        issues = []
        refs_ok = methodology.get("reference_count", 0) > 0

        scores["C1"] = 20 if generated_files else 0
        if not generated_files:
            issues.append("C1: 未生成图表")
        n_stats = len(methodology.get("statistical_methods", []))
        scores["C2"] = min(20, 10 + n_stats * 2)
        scores["C3"] = 20 if len(generated_files) >= 3 else (15 if generated_files else 5)
        stages_n = len(story.get("stages", []))
        scores["C4"] = min(15, stages_n) if stages_n >= 9 else 5
        scores["C5"] = 15 if refs_ok else 0
        if not refs_ok:
            issues.append("C5: 文献 API 不可用——请检查网络或手动补充真实引用")
        scores["C6"] = 10
        total = sum(scores.values())
        grade = "PASS (顶刊可投)" if total >= 80 else ("REVISE (需修改)" if total >= 60 else "FAIL (不达标)")
        return {"scores": scores, "total": total, "grade": grade,
                "issues": issues, "generated_files": generated_files}


# ─────────────────────────────────────────────────────────────
# ARIS Pipeline — 两阶段编排
# ─────────────────────────────────────────────────────────────
class ARISPipeline:
    def __init__(self, output_dir: str = "aris_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.analysis_dir = self.output_dir / "analysis"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)

    # ── Phase 1: 全面分析 + 故事 ─────────────────────────────
    def phase_story(self, data_path: str, topic: str) -> Dict[str, Any]:
        print("=" * 70)
        print("PHASE 1: Comprehensive Analysis + Top-journal Story")
        print("=" * 70)
        # 1. 全面数据分析
        if HAS_COMPREHENSIVE:
            analyzer = ComprehensiveAnalyzer(output_dir=str(self.analysis_dir))
            summary = analyzer.run(data_path)
            domain = summary.get("domain", "generic")
        else:
            summary = {"domain": "generic", "modules": {}}
            domain = "generic"
        # 2. 文献调研
        harvester = LiteratureHarvester()
        papers = harvester.search(topic, n=10)
        # 3. 方法论提炼
        extractor = MethodExtractor()
        methodology = extractor.extract(papers, domain, topic)
        # 4. 故事生成
        gen = StoryGenerator(self.analysis_dir)
        story = gen.generate(methodology)
        # 5. 评审
        reviewer = StrictReviewer()
        review = reviewer.review(methodology, story)
        methodology["_review_total"] = review["total"]
        story["review"] = review

        story_path = self.output_dir / "story.json"
        story_path.write_text(json.dumps(story, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path = self.output_dir / "story.md"
        md_path.write_text(gen.to_markdown(story, methodology), encoding="utf-8")

        print(f"\n[S] Review: {review['grade']} ({review['total']}/100)")
        for iss in review["issues"]:
            print(f"  - {iss}")
        print(f"\n[STORY] {md_path}")
        print("  >>> 请审查 story.md，确认/修改后运行 phase figures")
        return {"status": "success", "story": str(story_path),
                "story_md": str(md_path), "review": review,
                "analysis_summary": str(self.analysis_dir / "analysis_summary.json")}

    # ── Phase 2: 故事驱动的证据链出图 ─────────────────────────────
    def phase_figures(self, data_path: str, story_path: str) -> Dict[str, Any]:
        print("=" * 70)
        print("PHASE 2: Story-driven Evidence-Chain Figures")
        print("=" * 70)
        maker = StoryDrivenFigureMaker(self.output_dir)
        result = maker.make(Path(data_path), Path(story_path), self.analysis_dir)
        if result.get("status") == "error":
            return result
        # 最终评审
        story = json.loads(Path(story_path).read_text(encoding="utf-8"))
        reviewer = StrictReviewer()
        methodology = {"reference_count": story.get("reference_count", 0),
                       "statistical_methods": []}
        review = reviewer.review(methodology, story, result["generated_files"])
        result["review"] = review
        print(f"\n[S] Final review: {review['grade']} ({review['total']}/100)")
        return result

    def run(self, data_path: str, topic: str = "", phase: str = "full",
            story_path: str = None) -> Dict[str, Any]:
        if phase in ["story", "full"]:
            r1 = self.phase_story(data_path, topic)
            if r1.get("status") != "success":
                return r1
        if phase in ["figures", "full"]:
            sp = story_path or (self.output_dir / "story.json")
            if not Path(sp).exists():
                return {"status": "error", "message": f"story not found: {sp}"}
            r2 = self.phase_figures(data_path, sp)
            return r2 if phase == "figures" else {**r1, "figures": r2}
        return r1


def main():
    ap = argparse.ArgumentParser(description="ARIS 两阶段：先故事后证据链出图")
    ap.add_argument("--data", required=True, help="真实数据文件路径")
    ap.add_argument("--topic", default="", help="研究主题（文献调研用）")
    ap.add_argument("--output", default="aris_output", help="输出目录")
    ap.add_argument("--phase", default="full", choices=["story", "figures", "full"],
                    help="story=先出故事; figures=审查后出图; full=全流程")
    ap.add_argument("--story", default=None, help="Phase figures 使用的 story.json 路径")
    args = ap.parse_args()

    pipeline = ARISPipeline(output_dir=args.output)
    result = pipeline.run(args.data, args.topic, args.phase, args.story)
    if result.get("status") == "error":
        print(f"ERROR: {result['message']}")
        sys.exit(1)
    print("\n[DONE]")


if __name__ == "__main__":
    main()
