import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量（也就是你上周配置的密钥）
load_dotenv()

# ================= 1. 配置区 =================
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

# ================= 2. 读取资料 =================
def load_docs(file_path):
    """读取你的学科资料"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ================= 3. 核心 RAG 流程 =================
def ask_rag(question, docs_text):
    client = OpenAI(base_url=BASE_URL, api_key=os.getenv("DEEPSEEK_API_KEY"))
    
    # 这里修正了！必须强制 AI 附上出处！
    prompt = f"""你是一个专业的学科问答助手。请严格根据以下【参考资料】回答用户的问题。
如果参考资料中没有提到，请直接回答“根据提供的资料，我无法回答这个问题”，绝对不要自己瞎编。
在回答的最后，必须加上【来源：我的资料.txt】。

【参考资料】：
{docs_text}

【用户问题】：
{question}
"""
    # 发送请求
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1 # 温度调低，让它更严谨，不要发散
    )
    return response.choices[0].message.content


# ================= 4. 测试运行 =================
if __name__ == "__main__":
    print("正在加载资料...")
    try:
        docs = load_docs("我的资料.txt")
    except FileNotFoundError:
        print("【错误】找不到 '我的资料.txt'，请检查文件是否在同一个文件夹里！")
        exit()

    question = "HSK4级需要掌握多少个词汇？"
    
    print(f"\n用户提问：{question}")
    print("AI 正在思考并查阅资料...\n")
    
    answer = ask_rag(question, docs)
    
    print("=== AI 回答 ===")
    print(answer)
    print("===============")
