import pandas as pd
import re

# 👇 CHANGE THIS TO YOUR FILE NAME (e.g., '2020.csv')
file_name = "2025.csv"

# Load file
df = pd.read_csv(file_name)

# --- Basic sentiment words ---
positive_words = ['賺', '獲利', '上漲', '大漲', '看好', '漲停', '創新高', '買進', '反彈', '強勢']
negative_words = ['虧', '虧損', '賠錢', '暴跌', '下跌', '崩盤', '跌停', '看壞', '停損', '賣壓']
negation_words = ['不', '沒', '未', '無']

# --- Function to score sentiment ---
def get_score(text):
    text = str(text)
    score = 0
    for word in positive_words:
        if any(n + word in text for n in negation_words):
            score -= 1
        elif word in text:
            score += 1
    for word in negative_words:
        if any(n + word in text for n in negation_words):
            score += 1
        elif word in text:
            score -= 1
    return score

# --- Apply scoring ---
df["情緒分數"] = df["標題"].apply(get_score)
df["情緒加權分數"] = df["情緒分數"] * 0.1

# --- Save result ---
out_name = file_name.replace(".csv", "_scored.csv")
df.to_csv(out_name, index=False)
print("✅ Done! Output saved as:", out_name)
