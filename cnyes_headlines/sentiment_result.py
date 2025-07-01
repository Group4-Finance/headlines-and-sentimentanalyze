import pandas as pd
import glob
import os

# 關鍵詞設定
positive_keywords = [
    '創新高', '成長', '強勁', '回升', '創新紀錄', '資金湧入', '熱絡', '升溫',
    '超預期', '大漲', '報喜', '買盤進駐', '股價反彈','需求增加', '動能強勁',
    '利多', '高檔震盪'
]
# 負向關鍵詞擴充版
negative_keywords = [
    '崩跌', '重挫', '疲弱', '下修', '衰退', '低迷', '拋售', '空頭壓力', '賣壓湧現',
    '走跌', '走弱', '下滑', '挫逾', '需求疲軟', '跌破', '齊挫', '暴跌', '下跌', '下挫',
    '跌幅擴大', '續跌', '月減', '股匯齊挫', '殖利率下滑', '跌破整數關卡'
]

# 改良後：計算所有正負關鍵詞出現次數 → 傳回總體情緒分數（可正可負）
def get_sentiment(title):
    if pd.isna(title):
        return 0
    pos_score = sum(word in title for word in positive_keywords)
    neg_score = sum(word in title for word in negative_keywords)
    return pos_score - neg_score

# 左側分類：情緒越負 → 越可能進場（+1）
def left_side_label(score):
    if score > 0:
        return -1
    elif score < 0:
        return 1
    else:
        return 0

# 搜尋所有月份新聞檔案
all_files = glob.glob("cnyes_headlines_*.csv")

# 儲存所有資料
all_data = []

for file in all_files:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={'時間': 'date', '標題': 'title'})
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['sentiment'] = df['title'].apply(get_sentiment)
    all_data.append(df)

# 合併所有月份資料
combined_df = pd.concat(all_data, ignore_index=True)

# 每日匯總
daily_sentiment = combined_df.groupby('date')['sentiment'].sum().reset_index()
daily_sentiment = daily_sentiment.rename(columns={'date': '日期', 'sentiment': '每日原始總分'})
daily_sentiment['左側情緒分類'] = daily_sentiment['每日原始總分'].apply(left_side_label)

# 輸出結果
daily_sentiment.to_csv('sentiment_result.csv', index=False, encoding='utf-8-sig')
print("已輸出跨月份分析結果為 sentiment_result.csv")
