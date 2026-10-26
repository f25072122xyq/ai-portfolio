import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件里的密钥
load_dotenv() 

# ================= 引擎 1：本地引擎 (Ollama) =================
class LocalEngine:
    def __init__(self, model=None):
        self.model = model or os.getenv("LOCAL_MODEL", "qwen2.5:1.5b")

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        r = requests.post("http://localhost:11434/api/chat", json={
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "options": {"temperature": temperature, "num_predict": max_tokens},
            "stream": False
        }, timeout=60)
        r.raise_for_status() 
        return r.json()["message"]["content"]


# ================= 引擎 2：云端引擎 (DeepSeek) =================
class APIEngine:
    def __init__(self):
        self.client = None 

    def ensure_client(self):
        if self.client is None:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("缺少 DEEPSEEK_API_KEY 密钥，请检查 .env 文件！")
            self.client = OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=api_key
            )

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        self.ensure_client() 
        r = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return r.choices[0].message.content


# ================= 统一入口：双引擎封装 =================
class LLM:
    def __init__(self):
        self.local = LocalEngine()
        self.api = APIEngine()

    def ask(self, prompt, prefer="local", **kwargs):
        first, second = (self.local, self.api) if prefer == "local" else (self.api, self.local)
        try:
            return first.ask(prompt, **kwargs)
        except Exception as e:
            print(f"\n[引擎切换警告] 首选引擎失败，原因: {e}")
            print(f"[引擎切换警告] 正在自动切换到备用引擎...\n")
            return second.ask(prompt, **kwargs)
