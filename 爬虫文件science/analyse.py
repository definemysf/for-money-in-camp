import jieba
from collections import Counter

# 1. 读取文本
with open("梦溪笔谈_维基文库.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. 定义科技相关关键词（可根据需要自行扩展）
science_keywords = [
    '天文', '星', '历法', '地理', '水利', '堤坝', '冶金', '铁', '铜', '机械', '器械', '数学', '算术', '物理', '化学',
    '地震', '火药', '指南针', '磨镜', '造纸', '印刷', '医药', '医学', '农学', '工程', '发明', '观测', '仪器',
    '测量', '测绘', '建筑', '水钟', '漏刻', '车', '船', '桥', '水轮', '蒸馏', '炼丹', '秤', '度量衡', '舟', '灯', '风筝'
]

# 3. 分词
words = jieba.lcut(text)

# 4. 统计关键词出现次数
counter = Counter(words)
result = {kw: counter[kw] for kw in science_keywords if counter[kw] > 0}

# 5. 输出统计总结
print("《梦溪笔谈》科技相关关键词出现次数统计：\n")
for k, v in sorted(result.items(), key=lambda x: -x[1]):
    print(f"{k}: {v}次")

# 6. 可选：保存统计结果到文件
with open("梦溪笔谈_关键词统计总结.txt", "w", encoding="utf-8") as f:
    f.write("《梦溪笔谈》科技相关关键词出现次数统计：\n\n")
    for k, v in sorted(result.items(), key=lambda x: -x[1]):
        f.write(f"{k}: {v}次\n")