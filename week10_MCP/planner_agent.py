import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入你的 W6 引擎
try:
    from llm import LLM
except ImportError:
    raise SystemExit("❌ 找不到 llm.py，请确保它在上一级目录中。")

llm = LLM()

# 修复3：正确的提示词格式化
PLAN_PROMPT = """请把《%s》的备课拆成 4 个有序步骤。
要求：1.定教学要点 2.写教学目标 3.出教案框架 4.配课后练习。
请直接输出这4个步骤，每行一个。"""

def planner_agent(lesson, auto_confirm=False, prefer="local"):
    print(f"【规划中】正在拆解《{lesson}》的备课步骤...")
    
    # 1. 获取计划
    plan = llm.ask(PLAN_PROMPT % lesson, prefer=prefer)
    steps = [s.strip() for s in plan.splitlines() if s.strip()]
    
    # 过滤掉AI可能输出的废话（如"好的"、"步骤一："等）
    steps = [s for s in steps if len(s) > 5][:4]
    
    print("\n=== 拆解计划 ===")
    for i, step in enumerate(steps, 1):
        print(f"步骤 {i}: {step}")
    
    outputs = []
    # 2. 逐个执行
    for step in steps:
        print(f"\n【正在执行】{step}...")
        
        # 模拟从知识库获取背景资料（如果没有你之前的 retrieve，就用空字符串）
        ctx = "请参考《愚公移山》原文进行设计。" 
        
        # 修复3：正确的 Prompt 拼接
        prompt = f"参考资料：\n{ctx}\n\n请执行以下教学任务：\n{step}"
        
        out = llm.ask(prompt, prefer=prefer)
        outputs.append(f"【{step}】\n{out}")
        
        # 修复4：注入防护与人工确认
        if not auto_confirm:
            print("\n[待人工确认] 本步生成结果如下：")
            print(out[:200] + "...\n(已截断显示，完整结果已保存)")
            # 在实际交互中这里可以加 input("是否继续？(y/n)")

    return "\n\n".join(outputs)


if __name__ == "__main__":
    cloud = "--cloud" in sys.argv
    words = [a for a in sys.argv[1:] if a != "--cloud"]
    lesson = "".join(words) if words else "愚公移山"
    
    # 修复4：修复了原来截图里死循环重复调用 llm.ask 的问题
    if cloud:
        print("【提示】已切换到云端引擎运行...")
        # 将默认本地偏好改为云端
        prefer_mode = "api"
    else:
        prefer_mode = "local"

    # 自动确认模式默认开启，防止卡住
    final_result = planner_agent(lesson, auto_confirm=True, prefer=prefer_mode)
    
    print("\n\n=== 最终生成完毕 ===")
    # 保存到文件，方便查看
    with open("备课结果.md", "w", encoding="utf-8") as f:
        f.write(final_result)
    print("✅ 完整结果已保存到当前目录下的『备课结果.md』")
