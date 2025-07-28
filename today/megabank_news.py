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
    "User-Agent": "Mozilla/5.0"
}

today = datetime.today().date()
today_str = today.strftime("%Y%m%d")
formatted_date = today.strftime("%Y/%m/%d")

for page in range(1, 6):
    url = f"https://fund.megabank.com.tw/w/wp/wu01megaNews.djhtm?A=NA&B={today.year}-{today.month}-{today.day}&C=NA&Page={page}"
    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, features="html.parser")

    for tr in html.find_all('tr'):
        en_date = tr.find('td', class_=['wfb2c', 'wfb5c'])
        en_title = tr.find('a')

        if en_date and en_title and en_date.text.strip() == formatted_date:
            title_final = en_title.text.strip()
            url_final = "https://fund.megabank.com.tw" + en_title['href']
            table.append([formatted_date, title_final, url_final])

df = pd.DataFrame(table, columns=["時間", "標題", "連結"])
filename = f"megabank_news_{today_str}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"✅ 共儲存 {len(table)} 筆今日兆豐金新聞 → {filename}")
