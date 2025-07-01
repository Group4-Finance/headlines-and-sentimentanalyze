import pandas as pd

# 👉 設定檔案名稱
file_name = "PTT_stock.csv"

# 讀取資料
df = pd.read_csv(file_name)
df.columns = df.columns.str.strip()

# --- 基本情緒關鍵詞設定 ---
positive_words = ['賺', '獲利', '上漲', '大漲', '看好', '漲停', '創新高', '買進', '反彈', '強勢']
negative_words = ['虧', '虧損', '賠錢', '暴跌', '下跌', '崩盤', '跌停', '看壞', '停損', '賣壓']
negation_words = ['不', '沒', '未', '無']

# --- 離散化情緒分數（僅 ±1 / 0） ---
def get_discrete_score(text):
    text = str(text)
    pos_hit = any(
        word in text and not any(n + word in text for n in negation_words)
        for word in positive_words
    )
    neg_hit = any(
        word in text and not any(n + word in text for n in negation_words)
        for word in negative_words
    )

    if pos_hit and not neg_hit:
        return 1
    elif neg_hit and not pos_hit:
        return -1
    else:
        return 0

# --- 左側情緒分類：原始總分越低 → 越可能進場
def left_side_label(score):
    if score > 0:
        return -1
    elif score < 0:
        return 1
    else:
        return 0

# --- 套用情緒分數 ---
df["情緒分數"] = df["標題"].apply(get_discrete_score)
# 嘗試轉換日期欄位，錯誤值設為 NaT（缺失）
df["日期"] = pd.to_datetime(df["日期"], errors="coerce").dt.date
df = df.dropna(subset=["日期"])    # 移除無法轉為日期的列

daily_summary = (
    df.groupby("日期")["情緒分數"]
    .sum()
    .reset_index()
    .rename(columns={"情緒分數": "每日原始總分"})
)
daily_summary["左側情緒分類"] = daily_summary["每日原始總分"].apply(left_side_label)

# --- 輸出每日結果 ---
daily_summary.to_csv("PTT_sentiment.csv", index=False, encoding="utf-8-sig")
print("✅ 已輸出每日原始總分與左側分類至 PTT_sentiment.csv")
