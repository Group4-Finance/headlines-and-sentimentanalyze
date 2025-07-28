import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import jieba.analyse
import jieba
import logging
jieba.setLogLevel(logging.WARNING)

table = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 只抓今天
today = datetime.today().date()
today_str = today.strftime("%Y%m%d")
date_str = f"{today.year}-{today.month}-{today.day}"
formatted_date = today.strftime("%Y/%m/%d")

for page in range(1, 6):  # 每日最多5頁
    url = f"https://fund.megabank.com.tw/w/wp/wu01megaNews.djhtm?A=NA&B={date_str}&C=NA&Page={page}"
    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, features="html.parser")

    for tr in html.find_all('tr'):
        en_date = tr.find('td', class_=['wfb2c', 'wfb5c'])
        en_title = tr.find('a')

        if en_date and en_title and en_date.text.strip() == formatted_date:
            title_final = en_title.text.strip()
            url_final = "https://fund.megabank.com.tw" + en_title['href']
            tags = jieba.analyse.extract_tags(title_final)

            data = {
                "日期": en_date.text.strip(),
                "標題": title_final,
                "連結": url_final,
                "標籤": tags
            }

            if data not in table:
                table.append(data)

# 存成 CSV
df = pd.json_normalize(table)
df.to_csv(f"megabank_news_{today_str}.csv", index=False, encoding="utf-8-sig")
