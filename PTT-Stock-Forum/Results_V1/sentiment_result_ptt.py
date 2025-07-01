import pandas as pd

# 讀取 CSV（含正確標題列）
df = pd.read_csv('2021.csv')  # 用你的實際檔案名稱

# 清理與重新命名欄位
df.columns = df.columns.str.strip()
df = df.rename(columns={'標題': 'title', '人氣': 'score', '日期': 'date'})  # 注意：你是「日期」不是「時間」
df['title'] = df['title'].str.strip()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date  # 指定日期格式

# 設定情緒關鍵字
positive_keywords = [
    '創高', '創新高', '成長', '營收創高', '強勁', '回升', '擴張',
    '超預期', '買盤強勁', '收紅', '創新紀錄', '業績亮眼'
]
negative_keywords = [
    '下跌', '崩跌', '重挫', '利空', '疲弱', '萎縮', '下修',
    '衰退', '賣壓沉重', '收黑', '虧損擴大', '低迷'
]

# 計算情緒分數
def get_sentiment(title):
    if pd.isna(title):
        return 0
    for word in positive_keywords:
        if word in title:
            return 1
    for word in negative_keywords:
        if word in title:
            return -1
    return 0

df['sentiment'] = df['title'].apply(get_sentiment)

# 每日情緒總分
daily_sentiment = df.groupby('date')['sentiment'].sum().reset_index()
daily_sentiment = daily_sentiment.rename(columns={'date': '日期', 'sentiment': '每日原始總分'})

# 左側情緒分類邏輯
def left_side_label(score):
    if score > 0:
        return -1
    elif score < 0:
        return 1
    else:
        return 0

daily_sentiment['左側情緒分類'] = daily_sentiment['每日原始總分'].apply(left_side_label)

# 輸出結果
daily_sentiment.to_csv('sentiment_result.csv', index=False, encoding='utf-8-sig')
print("✅ 已輸出含每日原始總分與左側情緒分類的結果為 sentiment_result.csv")
