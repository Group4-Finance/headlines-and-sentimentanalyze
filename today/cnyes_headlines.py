import requests
import csv
import time
from datetime import datetime, timedelta

# 取今天的日期
today = datetime.today()
target_date_str = today.strftime("%Y-%m-%d")
start_ts = int(datetime(today.year, today.month, today.day, 0, 0, 0).timestamp())
end_ts = int(datetime(today.year, today.month, today.day, 23, 59, 59).timestamp())

# headers 設定
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://news.cnyes.com/news/cat/headline"
}

# 初始化
results = []
page = 1
while True:
    url = (
        f"https://api.cnyes.com/media/api/v1/newslist/category/headline"
        f"?startAt={start_ts}&endAt={end_ts}&limit=100&page={page}"
    )

    time.sleep(5)
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"

    try:
        data = res.json()
        items = data["items"]["data"]
    except Exception:
        break

    if not items:
        break

    for item in items:
        timestamp = item["publishAt"]
        pub_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        title = item["title"]
        news_id = item["newsId"]
        link = f"https://news.cnyes.com/news/id/{news_id}"
        results.append([pub_time, title, link])

    page += 1

# 儲存成 CSV
filename = f"cnyes_headlines_{target_date_str.replace('-', '')}.csv"
with open(filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["時間", "標題", "連結"])
    writer.writerows(results)

print(f"已儲存 {len(results)} 筆新聞到 {filename}")
