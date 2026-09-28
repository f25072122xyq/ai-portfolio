import csv

# 1. 读取生词表
with open("生词表.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    words = list(reader)

# 2. 生成带完整句子的填空题
with open("填空练习.txt", "w", encoding="utf-8") as f_out:
    
    # 只取前 5 个词
    selected_words = words[:5] 
    
    for w in selected_words:
        word = w.get('词汇', '')
        pos = w.get('词性', '')

        # === 跳过“把字句” ===
        if word == '把字句':
            continue

        # 针对不同词汇，逐一设计精准句子
        if word == '把':
            # 介词：典型的“把”字句结构
            sentence = "他 ____ 那本新买的书放在了书架上。"
        elif word == '商量':
            # 动词：做谓语，表示交换意见
            sentence = "明天去哪里吃饭，我们需要好好 ____ 一下。"
        elif word == '决定':
            # 动词：做谓语，表示做出主张
            sentence = "经过深思熟虑，他最终 ____ 放弃这次机会。"
        elif word == '感动':
            # 动词：做谓语，表示受到触动
            sentence = "听到他无私奉献的事迹，在场的所有人都深受 ____。"
        else:
            # 其他词性兜底
            sentence = f"老师在课堂上提到了 ____ 这个概念。"

        # 写入文件
        f_out.write(f"请用“____”改写句子：{sentence} （目标词：{word}，词性：{pos}）\n")

print(f"运行成功！已跳过“把字句”，生成《填空练习.txt》")