import os
import sys

# 1. 路径配置（跨周调用大法，防止报错）
# 找到上一级目录（也就是你整个 ai-portfolio 的根目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import weekpath
weekpath.load_env() # 加载 .env 里的密钥

# 2. 导入你前两周写好的积木
from llm import LLM 
# 注意：如果你之前的 rag_qa.py 里没有 retrieve 和 build_prompt 函数，
# 我们用这里的极简版代替。如果你有，请把下面两行改成 from rag_qa import retrieve, build_prompt
from openai import OpenAI

# 极简版检索函数（模拟你 W7 的功能）
def retrieve(question):
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "week07_RAG", "我的资料.txt"), "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "暂无资料"

def build_prompt(question, ctx):
    return f"【参考资料】：\n{ctx}\n\n【用户问题】：\n{question}"

# 3. 组装核心：粘合层
llm = LLM()
SYSTEM_HINT = "你是国际中文教学助手，面向 HSK3-4 学习者，回答需给出依据。"

def answer(question, use_rag=True, prefer="local"):
    if use_rag:
        ctx = retrieve(question)
        prompt = SYSTEM_HINT + "\n" + build_prompt(question, ctx)
    else:
        prompt = SYSTEM_HINT + "\n" + question
    
    return llm.ask(prompt, prefer=prefer)

# 4. 运行测试：三问三答
if __name__ == "__main__":
    questions = [
        "把字句的教学难点有哪些？",
        "HSK4词汇量要求是多少？",
        "《愚公移山》可以设计什么课堂活动？"
    ]
    
    print("=== 开始测试学科智能助手 v1.0 ===")
    for q in questions:
        print(f"\n提问: {q}")
        try:
            # 走 RAG 模式，使用本地引擎 (prefer="local")
            ans = answer(q, use_rag=True, prefer="local")
            print(f"回答: {ans}")
        except Exception as e:
            print(f"[运行失败] {e}")
        print("-" * 40)
