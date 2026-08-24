# -*- coding: utf-8 -*-
"""
agne-ai API 集成模块
OpenAI 兼容接口，支持 chat completions 和 image generations
SSL 需要在 Windows 上使用 CERT_NONE（apihub.agnes-ai.com 证书问题）
"""
from __future__ import annotations

import json
import ssl
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional

# Agnes AI 配置
AGNES_BASE_URL = "https://apihub.agnes-ai.com/v1"
AGNES_API_KEY = "sk-uR79z5ie2SDrQvTq49p5bH0Bp3Fmes9PlYhy9f42lMxhI4tZ"

# SSL 上下文（禁用验证以解决 Windows SSL 握手问题）
_SSL_CTX = None

def _get_ssl_context() -> ssl.SSLContext:
    global _SSL_CTX
    if _SSL_CTX is None:
        _SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        _SSL_CTX.check_hostname = False
        _SSL_CTX.verify_mode = ssl.CERT_NONE
    return _SSL_CTX

# 代理绕过：agnes-ai 通过本地代理会 502（TLS 握手失败），直接直连
_PROXIES_BYPASS = {
    "http": None,
    "https": None,
}

# 全局只初始化一次 opener（禁用代理 + 自定义 SSL）
_OPENER_INSTALLED = False

def _ensure_opener():
    """安装全局 opener：禁用代理 + 自定义 SSL context（Windows 兼容）"""
    global _OPENER_INSTALLED
    if _OPENER_INSTALLED:
        return
    ctx = _get_ssl_context()
    # 覆盖全局默认 HTTPS context（Windows urllib 的 HTTPSHandler 不接受 context 参数，
    # 但 ssl._create_default_https_context 会被 urllib 内部调用）
    ssl._create_default_https_context = lambda *a, **kw: ctx
    # 禁用代理：用空 ProxyHandler 覆盖环境 HTTPS_PROXY
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    _OPENER_INSTALLED = True

def _api_call(endpoint: str, method: str = "GET", data: dict = None, timeout: int = 120) -> dict:
    """通用 API 调用，处理 SSL 和错误"""
    _ensure_opener()
    url = f"{AGNES_BASE_URL}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {AGNES_API_KEY}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    resp = urllib.request.urlopen(req, timeout=timeout)
    return json.loads(resp.read().decode())

def list_models() -> List[Dict]:
    """列出可用模型"""
    result = _api_call("models")
    return result.get("data", [])

def chat_completion(
    messages: List[Dict],
    model: str = "agnes-2.5-flash",  # 默认使用 2.5-flash（reasoning 与 content 平衡更好）
    max_tokens: int = 1000,           # reasoning 模型需要足够 token
    temperature: float = 0.7,
    stream: bool = False,
    reasoning_effort: str = "low"
) -> Dict:
    """聊天补全（支持 reasoning 模型，content + reasoning_content 双字段）"""
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
        "reasoning": {"effort": reasoning_effort}
    }
    start = time.time()
    result = _api_call("chat/completions", "POST", payload, timeout=120)
    elapsed = time.time() - start
    choice = result.get("choices", [{}])[0]
    msg = choice.get("message", {})
    # reasoning 模型：content 可能为空，fallback 到 reasoning_content
    content = msg.get("content", "") or msg.get("reasoning_content", "")
    reasoning = msg.get("reasoning_content", "")
    usage = result.get("usage", {})
    return {
        "content": content,
        "reasoning": reasoning,
        "model": model,
        "usage": usage,
        "elapsed_s": round(elapsed, 1),
        "finish_reason": choice.get("finish_reason", "")
    }

def generate_image(
    prompt: str,
    model: str = "agnes-image-2.0-flash",
    size: str = "1024x1024",
    n: int = 1
) -> Dict:
    """生成图片（可能 503 服务繁忙）"""
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": n
    }
    start = time.time()
    try:
        result = _api_call("images/generations", "POST", payload, timeout=180)
        elapsed = time.time() - start
        return {
            "status": "success",
            "elapsed_s": round(elapsed, 1),
            "data": result.get("data", [])
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "status": "error",
            "error": str(e),
            "elapsed_s": round(elapsed, 1)
        }

def generate_mechanism_prompt(
    axis_nodes: List[Dict],
    style: str = "nature-journal"
) -> str:
    """为机制轴生成 AI 绘图提示词"""
    entity_lines = []
    for node in axis_nodes:
        eid = node.get("id", "")
        title = node.get("title", "")
        evid = node.get("evi", "")
        geom = node.get("geom", "")
        entity_lines.append(f"- {title} [{eid}] (recovery: {geom})")

    relations = []
    for i in range(len(axis_nodes) - 1):
        relations.append(f"{axis_nodes[i].get('id', '')} -> {axis_nodes[i+1].get('id', '')}")

    prompt = f"""Scientific mechanism diagram for Nature/Science journal:

AXIS: Gut microbiome remodelling → serum purine/indole metabolism → microglia TGFβ-purinergic → OPC purinergic → sleep recovery

Entities (6 nodes, horizontal flow):
{chr(10).join(entity_lines)}

Relations (causal arrows):
{chr(10).join(relations)}

Style requirements:
- {style} style, clean vector illustration
- Flat design, white background
- Color-coded: microbiome (red), serum metabolites (blue), faeces (green), microglia (orange), OPC (purple), sleep (gold)
- Evidence badges (E1/E2) on each node
- Arrows: activation (filled head) / inhibition (flat head)
- Minimal text, high information density
- Suitable for Nature Methods/Cell Systems figure panel

Generate a professional scientific mechanism diagram."""
    return prompt

# 便捷函数
def ask_agnes(messages, **kwargs):
    """简化的聊天调用"""
    return chat_completion(messages, **kwargs)

def draw_mechanism(axis_data: List[Dict], output_dir: str = None) -> Dict:
    """完整机制图生成流程：提示词生成 → 图片生成"""
    prompt = generate_mechanism_prompt(axis_data)
    # 先让 AI 优化提示词
    response = chat_completion([
        {"role": "user", "content": f"优化以下科学机制图提示词，使其符合 Nature/Science 投稿标准（简洁、精确、专业）：\n\n{prompt}"}
    ], max_tokens=300)
    optimized_prompt = response["content"]
    print(f"Optimized prompt:\n{optimized_prompt}")
    # 生成图片
    img_result = generate_image(optimized_prompt)
    return {
        "original_prompt": prompt,
        "optimized_prompt": optimized_prompt,
        "image": img_result
    }

if __name__ == "__main__":
    # 测试
    print("=== agnes-ai API 测试 ===")
    models = list_models()
    print(f"可用模型: {[m['id'] for m in models]}")

    print("\n--- Chat 测试 ---")
    result = chat_completion([
        {"role": "user", "content": "简述肠脑轴在睡眠障碍中的潜在机制，3句话"}
    ], max_tokens=200)
    print(f"响应 ({result['elapsed_s']}s): {result['content'][:100]}...")

    print("\n--- 图片生成测试 ---")
    img = generate_image("scientific gut-brain axis mechanism diagram, Nature style")
    print(f"状态: {img['status']}, 耗时: {img.get('elapsed_s', '?')}s")
    if img['status'] == 'success':
        for d in img.get('data', []):
            print(f"  URL: {d.get('url', 'N/A')}")
    else:
        print(f"  错误: {img.get('error', 'unknown')}")
