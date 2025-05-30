import jieba
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from matplotlib.font_manager import FontProperties

# 设置中文字体
font_path = "NotoSansSC-VariableFont_wght.ttf"  # 改为你的实际路径
my_font = FontProperties(fname=font_path, size=14)

# 1. 读取文本
with open("梦溪笔谈_维基文库.txt", "r", encoding="utf-8") as f:
    text = f.read()

labels = ['天文', '水利', '机械', '火药', '指南针', '冶金', '医学', '造纸', '印刷', '农学']
values = [9, 8, 2, 2, 2, 1, 1, 1, 1, 1]

plt.figure(figsize=(12,6))
plt.bar(labels, values, color='skyblue')

# 2. 科技关键词
science_keywords = [
    '天文', '星', '历法', '地理', '水利', '堤坝', '冶金', '铁', '铜', '机械', '器械', '数学', '算术', '物理', '化学',
    '地震', '火药', '指南针', '磨镜', '造纸', '印刷', '医药', '医学', '农学', '工程', '发明', '观测', '仪器',
    '测量', '测绘', '建筑', '水钟', '漏刻', '车', '船', '桥', '水轮', '蒸馏', '炼丹', '秤', '度量衡', '舟', '灯', '风筝'
]

# 3. 分词与统计
words = jieba.lcut(text)
counter = Counter(words)
result = {kw: counter[kw] for kw in science_keywords if counter[kw] > 0}

# ------ 柱状图 -------
plt.xlabel('科技关键词', fontproperties=my_font)
plt.ylabel('出现次数', fontproperties=my_font)
plt.title('《梦溪笔谈》科技关键词出现次数柱状图', fontproperties=my_font)
plt.xticks(rotation=45, ha='right', fontproperties=my_font)
plt.yticks(fontproperties=my_font)
plt.tight_layout()
plt.savefig('梦溪笔谈_科技关键词柱状图.png', dpi=200)
plt.show()

# ------ 词云图 -------
wc = WordCloud(
    font_path='NotoSansSC-VariableFont_wght.ttf',    # 微软雅黑字体，确保有这个文件，否则用其他支持中文的字体
    background_color='white',
    width=800,
    height=400,
    max_words=50
)
wc.generate_from_frequencies(result)
wc.to_file('梦溪笔谈_科技关键词词云.png')

plt.figure(figsize=(10,5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("《梦溪笔谈》科技关键词词云")
plt.show()