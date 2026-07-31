"""
shared/llm_call.py
统一的 LLM 调用封装，支持 DeepSeek / OpenAI 兼容接口。
"""
import os
import time
import json
from typing import Optional

import requests


DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 2  # seconds


def llm_call(
    prompt: str,
    system: str = "You are a helpful assistant.",
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL,
    temperature: float = 0.7,
    max_tokens: int = 8192,
    max_retries: int = DEFAULT_MAX_RETRIES,
    response_format: Optional[dict] = None,
) -> str:
    """
    调用 OpenAI 兼容接口，返回模型回复文本。

    Parameters
    ----------
    prompt : str
        用户消息。
    system : str
        系统提示词。
    model : str
        模型名称。
    api_key : str, optional
        API key，默认从环境变量 DEEPSEEK_API_KEY 读取。
    base_url : str
        API base URL。
    temperature : float
        采样温度。
    max_tokens : int
        最大输出 token 数。
    max_retries : int
        失败重试次数。
    response_format : dict, optional
        响应格式，如 {"type": "json_object"}。

    Returns
    -------
    str
        模型回复文本。
    """
    if api_key is None:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量或传入 api_key 参数")

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format:
        payload["response_format"] = response_format

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code != 200:
                print(f"[DEBUG] API error {resp.status_code}: {resp.text[:500]}")
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError) as e:
            if attempt == max_retries:
                raise RuntimeError(f"LLM 调用失败，已重试 {max_retries} 次: {e}")
            time.sleep(DEFAULT_RETRY_DELAY * attempt)

    return ""


def llm_call_json(
    prompt: str,
    system: str = "You are a helpful assistant. Respond in valid JSON only.",
    **kwargs,
) -> dict:
    """
    调用 LLM 并解析 JSON 响应。
    """
    raw = llm_call(
        prompt,
        system=system,
        response_format={"type": "json_object"},
        **kwargs,
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM 返回的内容不是合法 JSON: {e}\n\n原始内容:\n{raw[:500]}")


if __name__ == "__main__":
    # 快速测试
    result = llm_call("用一句话介绍材料科学")
    print(result)
