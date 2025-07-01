1) Arrange CSV files by year 2020-2025
2) Latest forum page = previous page + 1
3) 2020 starting page index 945 = https://www.ptt.cc/bbs/Stock/index945.html
4) Result_V1 --> sentiment_result.py(by Winnie) modified to cope with PTT CSV format (old version using News keywoards to identify scores)
5) Result_V2 --> Scores are caculated according to more informal key words and negation words (More accurate in terms of scores) uses 情緒加權分數 to combine with other factor (formula of Score * 0.1)
