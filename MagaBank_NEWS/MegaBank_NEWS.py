import requests
import bs4 as bs
import pandas as pd
from datetime import datetime, timedelta
import tabulate
import jieba.analyse
import jieba
import logging
jieba.setLogLevel(logging.WARNING)

table = []
h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

start_date = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
end_date = datetime.today().date()
current_date = start_date

while current_date <= end_date:
    date_str = f"{current_date.year}-{current_date.month}-{current_date.day}"

    for page in range(1, 6):
        url = f"https://fund.megabank.com.tw/w/wp/wu01megaNews.djhtm?A=NA&B={date_str}&C=NA&Page={page}"
        response = requests.get(url, headers=h)
        html = bs.BeautifulSoup(response.text, features="html.parser")

        for tr in html.find_all('tr'):
            en_date = tr.find('td', class_=['wfb2c', 'wfb5c'])
            en_title = tr.find('a')

            if en_date and en_title:

                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%Y/%m/%d")

                if en_date.text.strip() == formatted_date:
                    date_final = en_date.text.strip()
                    title_final = en_title.text.strip()
                    en_url = en_title['href']
                    url_final = "https://fund.megabank.com.tw" + en_url
                    tags = jieba.analyse.extract_tags(title_final)

                    data = {
                        "日期": date_final,
                        "標題": title_final,
                        "連結": url_final,
                        "標籤": tags
                    }
                    if data not in table:  # 加這行就能避免重複
                        table.append(data)

    current_date += timedelta(days=1)  # 換下一天

df = pd.json_normalize(table)
# print(tabulate.tabulate(df, headers='keys', tablefmt='grid'))

df.to_csv("megabank_news.csv",index=False, encoding="utf-8-sig")