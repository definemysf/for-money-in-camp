import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import re
from snownlp import SnowNLP
from matplotlib.font_manager import FontProperties

# 全局字体设置，保证所有matplotlib绘制的中文都能正常显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 字体文件路径，给wordcloud和fontproperties用
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font = FontProperties(fname=FONT_PATH)

def fetch_text_from_kanunu(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, "html.parser")
    tds = soup.find_all('td')
    main_td = max(tds, key=lambda td: len(td.get_text(strip=True)), default=None)
    if not main_td or len(main_td.get_text(strip=True)) < 200:
        raise ValueError('未找到正文内容，请检查页面结构！')
    text = main_td.get_text(separator='\n').replace('\u3000', '').replace('\r', '')
    text = re.sub(r'www\.kanunu8\.com.*', '', text)
    text = re.sub(r'看书好.*', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def load_stopwords():
    stopwords = set('，。、：“”‘’！？（）…—\n\t  了 的 和 是 在 与 也 不 有 我 他 她 你 我们 他们 她们 这 那'.split())
    try:
        with open('yangzhiqiu_stopwords.txt', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith('//'):
                    stopwords.add(word)
    except Exception as e:
        print("加载停用词表失败：", e)
    return stopwords

def word_frequency(text):
    words = jieba.lcut(text)
    stopwords = load_stopwords()
    words = [w for w in words if w not in stopwords and len(w) > 1]
    counter = Counter(words)
    return counter.most_common(20)

def sentiment_analysis(text):
    s = SnowNLP(text)
    return s.sentiments

def plot_wordcloud(text, filename='wordcloud.png', remove_stopwords=True):
    words = jieba.lcut(text)
    if remove_stopwords:
        stopwords = load_stopwords()
        words = [w for w in words if w not in stopwords and len(w) > 1]
    else:
        words = [w for w in words if len(w) > 1]
    wc = WordCloud(font_path=FONT_PATH, background_color='white', width=800, height=400)
    wc.generate(' '.join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('《羊脂球》词云', fontproperties=font)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def character_network(text, characters, filename='character_network.png'):
    edges = Counter()
    sentences = re.split('[。！？\n]', text)
    for sent in sentences:
        present = [c for c in characters if c in sent]
        for i in range(len(present)):
            for j in range(i+1, len(present)):
                edges[(present[i], present[j])] += 1
    G = nx.Graph()
    for (a, b), w in edges.items():
        G.add_edge(a, b, weight=w)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color='lightblue',
        node_size=2000,
        edge_color='gray',
        width=[G[u][v]['weight'] for u,v in G.edges()],
        font_family='sans-serif',
        font_size=15,
        font_weight='bold'
    )
    # networkx的draw会用rcParams字体，但保险起见再手动写一遍节点标签
    for label in pos:
        plt.text(pos[label][0], pos[label][1], label,
                 fontproperties=font,
                 horizontalalignment='center', verticalalignment='center')
    plt.title('人物关系网络', fontproperties=font)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_sentiment_trend(text, filename='sentiment_trend.png'):
    paras = [p for p in text.split('\n') if p.strip()]
    sentiments = [SnowNLP(p).sentiments for p in paras]
    plt.figure(figsize=(12,4))
    plt.plot(sentiments, marker='o')
    plt.title('情感趋势（按段落）', fontproperties=font)
    plt.xlabel('段落', fontproperties=font)
    plt.ylabel('情感分数 (0消极-1积极)', fontproperties=font)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_frequency_bar(freq, filename='freq_bar.png'):
    plt.figure(figsize=(10,5))
    words, counts = zip(*freq)
    plt.bar(words, counts)
    plt.title('高频词柱状图', fontproperties=font)
    plt.xlabel('词语', fontproperties=font)
    plt.ylabel('出现次数', fontproperties=font)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    url = "https://www.kanunu8.com/book4/10266/227953.html"
    text = fetch_text_from_kanunu(url)
    print("文本片段：", text[:100])
    freq = word_frequency(text)
    print("高频词：", freq)
    sentiment = sentiment_analysis(text)
    print("全文情感分数（0-1）：", sentiment)
    # 生成去除停用词的词云
    plot_wordcloud(text, filename='wordcloud_no_stopwords.png', remove_stopwords=True)
    # 生成包含全部词的词云
    plot_wordcloud(text, filename='wordcloud_all_words.png', remove_stopwords=False)
    characters = ['羊脂球', '卡雷马黛', '布里萨尔', '康特', '鲁阿索', '商人', '主教', '修女', '士兵']
    character_network(text, characters, filename='character_network.png')
    plot_sentiment_trend(text, filename='sentiment_trend.png')
    plot_frequency_bar(freq, filename='freq_bar.png')