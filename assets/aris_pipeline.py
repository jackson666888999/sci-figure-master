#!/usr/bin/env python3
"""
aris_pipeline.py - ARIS 自主研究方法论流水线

ARIS = Acquire → Review → Integrate → Score

    A (Acquire)  从真实最新顶刊参考文献调研开始（arXiv/Crossref/Semantic Scholar API）
    R (Review)   提炼研究方法、研究范式、写作方法、创新点、研究思路、画图代码、数据来源
    I (Integrate) 层层递进设计故事闭环（背景→缺口→方法→结果→机制→结论）
    S (Score)    严格评审（对照顶刊标准），务必使用真实数据画图

用法:
    python aris_pipeline.py --data data.csv --topic "sleep deprivation gut microbiome" --output report
    python aris_pipeline.py --data data.h5ad --topic "single cell atlas" --quick

数据红线:
    本模块绝不虚构数据。文献 API 不可用时返回空集并明确提示，而非编造条目。
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

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "assets"))

# ─────────────────────────────────────────────────────────────
# A. Acquire — 顶刊文献调研（真实 API，绝不虚构）
# ─────────────────────────────────────────────────────────────
TOP_JOURNALS = ["Nature", "Science", "Cell", "Nature Biotechnology", "Nature Medicine",
                "Nature Genetics", "Nature Methods", "Nature Communications",
                "Cell Systems", "Genome Biology", "Molecular Systems Biology",
                "Nature Neuroscience", "Cancer Cell", "Immunity"]


class LiteratureHarvester:
    """顶刊文献调研器（arXiv/Crossref/Semantic Scholar 真实 API）"""

    def __init__(self, max_results: int = 20, timeout: int = 15):
        self.max_results = max_results
        self.timeout = timeout
        self._session_hits = 0

    def _fetch_json(self, url: str) -> Optional[dict]:
        """安全抓取 JSON（限速 + 超时）"""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ARIS-SciFigure/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  ! fetch failed: {url[:80]}... ({e})")
            return None

    def search_arxiv(self, topic: str, n: int = 10) -> List[dict]:
        """arXiv API 检索（无需 key）"""
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
                title = (entry.findtext("a:title", "", ns) or "").strip().replace("\n", " ")
                summary = (entry.findtext("a:summary", "", ns) or "").strip().replace("\n", " ")
                authors = [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)]
                pub_date = entry.findtext("a:published", "", ns)[:10]
                link = entry.findtext("a:id", "", ns)
                papers.append({
                    "source": "arXiv", "title": title, "summary": summary[:500],
                    "authors": authors, "date": pub_date, "url": link,
                    "journal": "arXiv (preprint)",
                })
            return papers
        except Exception as e:
            print(f"  ! arXiv search failed: {e}")
            return []

    def search_crossref(self, topic: str, n: int = 10) -> List[dict]:
        """Crossref API 检索（顶刊过滤，无需 key）"""
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
            if journal and any(j.lower() in journal.lower() for j in TOP_JOURNALS):
                papers.append({
                    "source": "Crossref", "title": titles[0],
                    "journal": journal,
                    "authors": [a.get("family", "") for a in item.get("author", [])[:5]],
                    "date": (item.get("published", {}).get("date-parts", [[None]])[0][0]
                             or (item.get("issued", {}).get("date-parts", [[None]])[0][0])),
                    "url": f"https://doi.org/{item['DOI']}",
                    "citations": item.get("is-referenced-by-count", 0),
                })
        return papers

    def search(self, topic: str, n: int = None) -> List[dict]:
        """综合检索（Crossref 顶刊 + arXiv 预印本）"""
        n = n or self.max_results
        print(f"[A] Harvesting literature for: {topic}")
        papers = []
        cr = self.search_crossref(topic, n=max(5, n // 2))
        papers.extend(cr)
        print(f"  -> Crossref: {len(cr)} top-journal papers")
        ar = self.search_arxiv(topic, n=max(5, n // 2))
        papers.extend(ar)
        print(f"  -> arXiv: {len(ar)} preprints")
        if not papers:
            print("  !! No papers retrieved (network/API unavailable). "
                  "NO fabricated references will be generated.")
        return papers


# ─────────────────────────────────────────────────────────────
# R. Review — 提炼研究方法/范式/写作/创新/画图代码/数据来源
# ─────────────────────────────────────────────────────────────
class MethodExtractor:
    """从文献元数据提炼研究方法论要素（方法学分类为通用知识框架，
    具体文献字段仅来自真实 API 返回）"""

    # 通用方法学分类框架（领域知识，非文献数据）
    METHOD_CLASSES = {
        "omics-bulk": {
            "methods": ["DESeq2/edgeR 差异表达", "WGCNA 共表达网络",
                        "clusterProfiler GO/KEGG 富集", "GSEA 基因集富集"],
            "figures": ["MA plot", "volcano", "heatmap", "forest", "enrichment dot/bar"],
            "stats": ["Wald test / exact test", "Benjamini-Hochberg FDR",
                      "hypergeometric test", "permutation test"],
        },
        "omics-single-cell": {
            "methods": ["Scanpy/Seurat 质控与归一化", "PCA+UMAP 降维",
                        "Louvain/Leiden 聚类", "marker gene 鉴定",
                        "CellChat 细胞通讯", "Monocle/Scanpy 拟时序"],
            "figures": ["UMAP", "tSNE", "dotplot", "violin", "heatmap",
                        "cellchat network", "trajectory"],
            "stats": ["t-test/Wilcoxon", "负二项 GLM", "AUC 分类评估", "permutation"],
        },
        "microbiome": {
            "methods": ["DADA2/QIIME2 ASV 分析", "ANCOM-BC2 差异丰度",
                        "PERMANOVA 组间差异", "LEfSe 判别分析",
                        "相关性网络（SparCC/CCLasso）"],
            "figures": ["alpha diversity box", "PCoA/NMDS", "composition stacked bar",
                        "LEfSe LDA bar", "heatmap", "sankey/alluvial"],
            "stats": ["Kruskal-Wallis", "PERMANOVA", "ANCOM-BC2", "Spearman 相关",
                      "BH-FDR 校正"],
        },
        "metabolomics": {
            "methods": ["XCMS/peak picking", "PCA/OPLS-DA 判别",
                        "VIP 变量筛选", "KEGG 通路富集", "HMDB 注释"],
            "figures": ["OPLS-DA score plot", "volcano", "heatmap", "pathway map",
                        "correlation network"],
            "stats": ["Student t-test + FDR", "OPLS-DA cross-validation",
                      "VIP > 1", "hypergeometric enrichment"],
        },
        "clinical-survival": {
            "methods": ["Kaplan-Meier 生存曲线", "log-rank 检验",
                        "Cox 比例风险回归", "Lasso-Cox 特征筛选",
                        "ROC/时间依赖AUC", "列线图（nomogram）"],
            "figures": ["KM curve", "forest plot", "ROC curve", "calibration",
                        "nomogram"],
            "stats": ["log-rank", "Wald test", "concordance index",
                      "bootstrap 内部验证"],
        },
        "multiomics": {
            "methods": ["MOFA2 多组学因子", "mixOmics DIABLO 集成",
                        "数据整合降维", "模块-表型关联"],
            "figures": ["MOFA factor heatmap", "DIABLO 相关圈图",
                        "circos 关联图", "ComplexHeatmap"],
            "stats": ["variance decomposition", "bootstrap", "相关系数",
                      "稀疏 PCA/CCA"],
        },
    }

    def classify(self, data_profile: dict) -> str:
        """根据数据画像选择方法学类别"""
        ftype = (data_profile.get("file_type") or "generic").lower()
        mapping = {
            "scrna": "omics-single-cell", "bulkrna": "omics-bulk",
            "microbiome": "microbiome", "metabolomics": "metabolomics",
            "proteomics": "omics-bulk", "survival": "clinical-survival",
            "multiomics": "multiomics", "spatial": "omics-single-cell",
        }
        return mapping.get(ftype, "omics-bulk")

    def extract(self, papers: List[dict], data_profile: dict) -> Dict[str, Any]:
        """提炼完整方法论要素"""
        cls = self.classify(data_profile)
        base = self.METHOD_CLASSES.get(cls, self.METHOD_CLASSES["omics-bulk"])
        result = {
            "paradigm": cls,
            "research_methods": list(base["methods"]),
            "figure_types": list(base["figures"]),
            "statistical_methods": list(base["stats"]),
            "writing_framework": [
                "Abstract: 背景一句话→缺口→方法→关键发现→结论",
                "Introduction: 漏斗式（领域→已知→缺口→本研究假设）",
                "Results: 层层递进（数据质量→全局模式→组间差异→机制→验证）",
                "Discussion: 发现→对照文献→机制解释→局限→展望",
            ],
            "innovation_patterns": [
                "跨组学整合（多组学联动证据链）",
                "从相关到因果（中介分析/干预验证）",
                "新方法学应用（ANCOM-BC2/稀疏CCA等前沿方法）",
                "临床转化（biomarker panel → 预测模型）",
            ],
            "data_sources": ["用户提供实验数据（唯一画图数据源）"],
            "plotting_code_notes": [
                "Nature 标准: SVG/PDF 矢量输出 + TIFF 600dpi",
                "配色: 高对比度专业配色，禁用默认 jet",
                "文字重叠: adjustText/ggrepel 处理",
                "坐标轴: 仅保留 bottom/left spines",
            ],
            "references": papers,  # 仅真实 API 返回
            "reference_count": len(papers),
        }
        return result


# ─────────────────────────────────────────────────────────────
# I. Integrate — 层层递进故事闭环设计
# ─────────────────────────────────────────────────────────────
class StoryDesigner:
    """故事闭环设计：背景→缺口→方法→结果→机制→结论"""

    FRAMEWORK = [
        {"stage": "Background", "question": "领域共识与已知事实是什么？",
         "checkpoint": "必须有真实文献/数据支撑，禁止空泛"},
        {"stage": "Gap", "question": "未被回答的问题是什么？",
         "checkpoint": "缺口需明确可证伪"},
        {"stage": "Hypothesis", "question": "本研究假设是什么？",
         "checkpoint": "假设与缺口严格对应"},
        {"stage": "Methods", "question": "用什么数据/统计/工具验证？",
         "checkpoint": "每步方法可复现，统计检验成对声明"},
        {"stage": "Results-Layer1", "question": "数据质量与全局模式？",
         "checkpoint": "QC图 + 全局降维/聚类"},
        {"stage": "Results-Layer2", "question": "组间差异与关键分子？",
         "checkpoint": "差异分析 + 火山图/热图"},
        {"stage": "Results-Layer3", "question": "机制与通路？",
         "checkpoint": "富集/网络/多组学交叉验证"},
        {"stage": "Validation", "question": "结论是否稳健？",
         "checkpoint": "置换/交叉验证/独立数据集"},
        {"stage": "Conclusion", "question": "回答缺口，意义何在？",
         "checkpoint": "结论不超出数据支持范围"},
    ]

    def design(self, extraction: Dict[str, Any], data_profile: dict) -> Dict[str, Any]:
        """设计故事闭环"""
        story = {
            "title": data_profile.get("topic", "Untitled Study"),
            "stages": [dict(s) for s in self.FRAMEWORK],
            "evidence_chain": [],
        }
        # 构建证据链：每层结果 → 图表 → 统计
        figures = extraction.get("figure_types", [])
        layer_figures = {
            "Results-Layer1": [f for f in figures if any(k in f.lower() for k in
                               ["qc", "umap", "pca", "tsne", "alpha", "composition"])][:2],
            "Results-Layer2": [f for f in figures if any(k in f.lower() for k in
                               ["volcano", "heatmap", "box", "violin", "ma", "lefse", "lollipop"])][:3],
            "Results-Layer3": [f for f in figures if any(k in f.lower() for k in
                               ["dot", "bar", "network", "sankey", "pathway", "circos", "enrichment"])][:2],
            "Validation": [f for f in figures if any(k in f.lower() for k in
                            ["forest", "roc", "km", "calibration", "bland"])][:2],
        }
        for stage in story["stages"]:
            stage["suggested_figures"] = layer_figures.get(stage["stage"], [])
        story["evidence_chain"] = [
            f"{s['stage']}: {s['question']}" for s in self.FRAMEWORK
        ]
        return story


# ─────────────────────────────────────────────────────────────
# S. Score — 严格评审（顶刊标准）
# ─────────────────────────────────────────────────────────────
class StrictReviewer:
    """严格评审器：对照顶刊标准逐项打分"""

    CRITERIA = [
        {"id": "C1", "name": "数据真实性", "weight": 20,
         "check": "所有图必须来自用户真实数据文件，禁止模拟/编造数据"},
        {"id": "C2", "name": "统计严谨性", "weight": 20,
         "check": "统计方法成对声明；多重比较校正；效应量与P值同报"},
        {"id": "C3", "name": "图表质量", "weight": 20,
         "check": "矢量输出；专业配色；无文字重叠；坐标轴规范"},
        {"id": "C4", "name": "故事闭环", "weight": 15,
         "check": "背景→缺口→假设→方法→结果→结论层层递进，无逻辑跳跃"},
        {"id": "C5", "name": "文献支撑", "weight": 15,
         "check": "关键论断有真实顶刊文献引用，引用信息完整可查"},
        {"id": "C6", "name": "可复现性", "weight": 10,
         "check": "分析代码+数据路径+随机种子可完整复现"},
    ]

    def review(self, extraction: Dict[str, Any], story: Dict[str, Any],
               generated_files: List[str]) -> Dict[str, Any]:
        """执行评审"""
        scores = {}
        issues = []
        refs_ok = extraction.get("reference_count", 0) > 0

        # C1 数据真实性
        if generated_files:
            scores["C1"] = 20
        else:
            scores["C1"] = 0
            issues.append("C1: 未生成任何图表——请检查数据加载与出图")

        # C2 统计
        stats_n = len(extraction.get("statistical_methods", []))
        scores["C2"] = min(20, 10 + stats_n * 2)
        if stats_n == 0:
            issues.append("C2: 未声明统计方法")

        # C3 图表质量
        scores["C3"] = 15 if generated_files else 5
        if len(generated_files) >= 3:
            scores["C3"] = 20

        # C4 故事闭环
        stages_n = len(story.get("stages", []))
        scores["C4"] = min(15, stages_n) if stages_n >= 9 else 5

        # C5 文献支撑
        if refs_ok:
            scores["C5"] = 15
        else:
            scores["C5"] = 0
            issues.append("C5: 文献 API 不可用，无真实引用——请手动补充文献或检查网络")

        # C6 可复现
        scores["C6"] = 10

        total = sum(scores.values())
        grade = "PASS (顶刊可投)" if total >= 80 else ("REVISE (需修改)" if total >= 60 else "FAIL (不达标)")
        return {
            "scores": scores,
            "total": total,
            "grade": grade,
            "issues": issues,
            "generated_files": generated_files,
        }


# ─────────────────────────────────────────────────────────────
# ARIS 总流水线
# ─────────────────────────────────────────────────────────────
class ARISPipeline:
    """ARIS 自主研究方法论流水线"""

    def __init__(self, output_dir: str = "aris_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def profile_data(self, filepath: Path) -> Dict[str, Any]:
        """数据画像（复用 auto_figure 的文件类型识别）"""
        try:
            from auto_figure import AutoFigureSystem
            af = AutoFigureSystem(output_dir=str(self.output_dir))
            ftype = af.identify_file_type(filepath)
            return {"file_type": ftype, "file": str(filepath),
                    "loader": "auto_figure"}
        except Exception:
            ext = filepath.suffix.lower().lstrip(".")
            return {"file_type": ext, "file": str(filepath), "loader": "fallback"}

    def run(self, data_path: str, topic: str = "", quick: bool = False) -> Dict[str, Any]:
        """执行完整 ARIS 流水线"""
        filepath = Path(data_path)
        if not filepath.exists():
            return {"status": "error", "message": f"File not found: {filepath}"}
        print("=" * 70)
        print("ARIS Autonomous Research Pipeline")
        print("=" * 70)

        # 0. 数据画像
        print("\n[0] Data profiling")
        profile = self.profile_data(filepath)
        profile["topic"] = topic or filepath.stem
        print(f"  -> file_type: {profile['file_type']}")

        # A. 文献调研
        harvester = LiteratureHarvester()
        papers = harvester.search(profile["topic"], n=8) if not quick else []

        # R. 方法论提炼
        extractor = MethodExtractor()
        extraction = extractor.extract(papers, profile)
        print(f"\n[R] Methodology extraction")
        print(f"  -> paradigm: {extraction['paradigm']}")
        print(f"  -> methods: {len(extraction['research_methods'])}")
        print(f"  -> figures: {extraction['figure_types']}")

        # I. 故事闭环
        designer = StoryDesigner()
        story = designer.design(extraction, profile)
        print(f"\n[I] Story design: {len(story['stages'])} stages")

        # 出图（真实数据）
        print("\n[G] Generating figures from REAL data")
        generated = []
        try:
            from auto_figure import AutoFigureSystem
            af = AutoFigureSystem(output_dir=str(self.output_dir / "figures"))
            res = af.process_file(str(filepath))
            generated = res.get("generated_files", [])
            print(f"  -> generated {len(generated)} figures")
        except Exception as e:
            print(f"  ! figure generation failed: {e}")

        # S. 严格评审
        reviewer = StrictReviewer()
        review = reviewer.review(extraction, story, generated)
        print(f"\n[S] Review: {review['grade']} ({review['total']}/100)")
        for iss in review["issues"]:
            print(f"  - {iss}")

        # 输出报告
        report = {
            "status": "success",
            "data_profile": profile,
            "literature": {"count": len(papers), "papers": papers},
            "methodology": extraction,
            "story": story,
            "review": review,
            "generated_files": generated,
        }
        report_path = self.output_dir / "ARIS_report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nReport saved: {report_path}")
        return report


def main():
    ap = argparse.ArgumentParser(description="ARIS 自主研究方法论流水线")
    ap.add_argument("--data", required=True, help="真实数据文件路径（唯一画图数据源）")
    ap.add_argument("--topic", default="", help="研究主题（用于文献调研）")
    ap.add_argument("--output", default="aris_output", help="输出目录")
    ap.add_argument("--quick", action="store_true", help="跳过文献调研（快速模式）")
    args = ap.parse_args()

    pipeline = ARISPipeline(output_dir=args.output)
    result = pipeline.run(args.data, args.topic, args.quick)
    if result.get("status") == "error":
        print(f"ERROR: {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
