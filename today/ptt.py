import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://www.ptt.cc"
BOARD_URL = f"{BASE_URL}/bbs/Stock/index.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}
COOKIES = {"over18": "1"}

def get_page_soup(url):
    res = requests.get(url, headers=HEADERS, cookies=COOKIES)
    return BeautifulSoup(res.text, "html.parser")

def get_last_page_number():
    soup = get_page_soup(BOARD_URL)
    btns = soup.find_all("a", class_="btn wide")
    for btn in btns:
        if "上頁" in btn.text:
            href = btn["href"]
            page_num = int(href.split("index")[1].split(".html")[0])
            return page_num + 1
    return None

def get_post_date(post_url):
    try:
        soup = get_page_soup(post_url)
        meta_tags = soup.find_all("span", class_="article-meta-value")
        if len(meta_tags) >= 4:
            date_str = meta_tags[3].text.strip()
            date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
            return date_obj.date()
    except Exception as e:
        print(f"Error parsing date from {post_url}: {e}")
    return None

def crawl_today_posts():
    today = datetime.now().date()
    print(f"Today's date: {today}")
    latest_page = get_last_page_number()
    print(f"Latest page number: {latest_page}")
    all_posts = []
    page = latest_page
    no_today_count = 0

    while page > 0:
        url = f"{BASE_URL}/bbs/Stock/index{page}.html"
        print(f"📄 Crawling {url}")
        soup = get_page_soup(url)
        articles = soup.find_all("div", class_="r-ent")

        today_posts_this_page = 0

        for a in articles:
            title_div = a.find("div", class_="title")
            if not title_div or not title_div.a:
                continue

            title = title_div.a.text.strip()
            href = BASE_URL + title_div.a["href"]
            post_date = get_post_date(href)

            if post_date == today:
                pop_div = a.find("div", class_="nrec")
                pop = pop_div.span.text.strip() if pop_div and pop_div.span else "None"
                all_posts.append({"標題": title, "人氣": pop, "日期": post_date})
                today_posts_this_page += 1

            time.sleep(0.5)

        if today_posts_this_page == 0:
            no_today_count += 1
            if no_today_count >= 2:
                print("No posts from today found in two consecutive pages. Stopping crawl.")
                break
        else:
            no_today_count = 0

        page -= 1
        time.sleep(1)

    return all_posts

# 執行主程式
if __name__ == "__main__":
    posts = crawl_today_posts()

    if posts:
        df = pd.DataFrame(posts)
        today_str = datetime.now().strftime("%Y%m%d")
        filename = f"ptt_stock_{today_str}.csv"  # ✅ 依照日期命名

        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"✅ 共取得 {len(posts)} 筆今日文章")
        print(f"📄 已儲存至：{filename}")
    else:
        print("⚠️ 今日未找到任何文章")
