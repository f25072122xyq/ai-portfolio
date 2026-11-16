import os
import json
import ast
import operator
import datetime
import re
import csv
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# ================= 1. 定义三个工具 =================
def get_time():
    return str(datetime.datetime.now())

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("只允许数字与 + - * / ** % 运算")

def calc(expr):
    try:
        return str(_eval_node(ast.parse(str(expr), mode="eval")))
    except ZeroDivisionError:
        return "错误：除数为0"
    except Exception as e:
        return "拒绝计算：%s" % e

def hsk_level(word):
    # 简单模拟生词表查询
    vocab_dict = {"把": "3", "坚持": "4", "商量": "4"}
    if str(word).strip() in vocab_dict:
        return "%s 是 %s 级" % (word, vocab_dict[str(word).strip()])
    return "未找到 %s" % word

TOOLS = {"get_time": get_time, "calc": calc, "hsk_level": hsk_level}

# ================= 2. 提示词与解析 =================
SYS = (
    "你是国际中文助教。可用工具只有这3个：get_time（查当前时间，无参数）、"
    "calc（四则运算，如 calc('35*24')）、hsk_level（查生词 HSK 等级，如 hsk_level('把'))。"
    "如需调用，只输出一行 JSON，格式：{\"tool\": \"工具名\", \"args\": [参数]}；"
    "一次只调用一个工具，绝不编造不存在的工具名；无需工具时直接回答。"
)

def parse_calls(txt):
    s = (txt or "").strip().replace("```json", "").replace("```", "").strip()
    try:
        obj = json.loads(s)
        return [obj] if isinstance(obj, dict) else []
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                obj = json.loads(m.group())
                if isinstance(obj, dict):
                    return [obj]
            except Exception:
                pass
    return []

# ================= 3. 核心运行循环 =================
def run(user_msg, max_calls=2):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg}]
    print(f"\n[用户] {user_msg}")
    
    for _ in range(max_calls):
        response = client.chat.completions.create(model="deepseek-chat", messages=msgs)
        txt = response.choices[0].message.content
        calls = [c for c in parse_calls(txt) if isinstance(c.get("tool"), str) and c.get("tool") in TOOLS]
        
        if not calls:
            print(f"[AI直接回答] {txt}")
            return txt
            
        # 执行工具
        results = []
        for call in calls:
            args = call.get("args") or []
            print(f"[模型决定调用工具] {call['tool']}，参数：{args}")
            try:
                res = TOOLS[call["tool"]](*args)
                results.append(res)
                print(f"[工具返回] {res}")
            except Exception as e:
                results.append(f"工具执行失败：{e}")
                print(f"[工具报错] {e}")
                
        # 回喂给模型
        msgs += [
            {"role": "assistant", "content": txt},
            {"role": "user", "content": f"工具返回：{results}。请据此作答。"}
        ]
        
    # 强制收口
    final = client.chat.completions.create(model="deepseek-chat", messages=msgs).choices[0].message.content
    print(f"[AI最终回答] {final}")
    return final

if __name__ == "__main__":
    print("=== 开始工具调用测试 ===")
    # 测试 1：复合问句
    run("请依次查询两件事：1. '把'字的HSK等级是多少？2. 现在的时间是多少？")
    # 测试 2：安全计算
    run("请帮我算一下 35*24 等于多少？")
    # 测试 3：越权拦截
    run("算一下 __import__('os').system('ls') 等于多少")
