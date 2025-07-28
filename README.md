# Django 匯率報表系統（Exchange Rate Dashboard）

一個使用 Django 製作的匯率查詢與分析平台，提供每日匯率自動更新、報表查詢、圖表分析與 CSV/Excel 匯出功能。

## 專案特色
- 從台灣銀行每日自動擷取匯率資料（中英文幣別）
- 可查詢不同時間區間與幣別匯率趨勢（支援日/月/年分組）
- 多幣別折線圖分析（Chart.js）
- 報表匯出為 CSV、Excel
- 後台排程任務每日自動抓資料
- 分頁功能

## 使用技術
- Django 5.x
- BeautifulSoup (抓台灣銀行匯率)
- Chart.js（前端圖表）
- Pandas（匯出 Excel）
- Django 管理命令 + Windows Task Scheduler（定時排程）

## 系統畫面截圖
<img width="1300" height="924" alt="django後台管理" src="https://github.com/user-attachments/assets/6de0f9f5-5a1e-4db1-90da-729c2b562ed1" />
<img width="1272" height="906" alt="django幣別資料" src="https://github.com/user-attachments/assets/a87e764b-ab38-4ee7-888f-90203d149c6b" />
<img width="1771" height="419" alt="登入畫面" src="https://github.com/user-attachments/assets/bfe23c63-4028-476f-aadb-07390356d421" />
<img width="1728" height="1178" alt="幣別查詢" src="https://github.com/user-attachments/assets/1bfa8669-4520-4188-b5fe-c2abc0c412f4" />
<img width="1672" height="1075" alt="幣別圖表" src="https://github.com/user-attachments/assets/55adb079-0cf2-4157-820a-f558bc1495c6" />

資料來源
台灣銀行匯率資料：https://rate.bot.com.tw/xrt?Lang=zh-TW

## 專案架構
<pre lang="markdown">```text
├── api/
│   ├── management/commands/
│   │   └── fetch_rates.py           ← 自訂匯率抓取指令
│   ├── migrations/                  ← 資料庫遷移記錄
│   ├── models.py                    ← 幣別與匯率模型定義
│   ├── views.py                     ← 報表邏輯與圖表 JSON 輸出
│   ├── urls.py                      ← app 路由（註冊在 bank/urls.py）
│   └── serializers.py               ← 資料序列化（若有提供 API）
│
├── bank/
│   ├── settings.py                  ← 專案設定（資料庫、app 註冊等）
│   ├── urls.py                      ← 專案主路由（include api/urls.py）
│
├── templates/
│   ├── base.html                    ← 頁面共用 layout 樣板
│   ├── registration/login.html      ← 登入頁面（Django auth）
│   └── report/product_list.html     ← 報表查詢與圖表頁面
│
├── db.sqlite3                       ← 預設 SQLite 資料庫
├── manage.py                        ← Django 指令入口
├── requirements.txt                 ← 套件安裝清單
.gitignore ```</pre>




