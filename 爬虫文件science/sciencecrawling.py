import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
})

base_url = "https://zh.wikisource.org/wiki/梦溪笔谈/卷{:0>2d}"  # 卷号两位填充
all_text = ""

for i in range(1, 27):
    url = base_url.format(i)
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        # 维基文库主要内容在 <div id="mw-content-text"> 下的 <div class="mw-parser-output">
        content_div = soup.find("div", {"id": "mw-content-text"})
        parser_output = content_div.find("div", class_="mw-parser-output")
        # 合并所有段落文本
        juan_text = ""
        for elem in parser_output.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6']):
            juan_text += elem.get_text(strip=True) + "\n"
        all_text += f"\n【卷{i:0>2d}】\n" + juan_text
        print(f"已抓取 卷{i:0>2d}")
        time.sleep(1)
    except Exception as e:
        print(f"抓取 卷{i:0>2d} 失败: {e}")

with open("梦溪笔谈_维基文库.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("全部卷抓取完毕，已保存到 梦溪笔谈_维基文库.txt")