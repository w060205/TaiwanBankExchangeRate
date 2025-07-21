# Django 匯率報表系統（Exchange Rate Dashboard）

一個使用 Django 製作的匯率查詢與分析平台，提供每日匯率自動更新、報表查詢、圖表分析與 CSV/Excel 匯出功能。

## 💡 專案特色
- 從台灣銀行每日自動擷取匯率資料（中英文幣別）
- 可查詢不同時間區間與幣別匯率趨勢（支援日/月/年分組）
- 多幣別折線圖分析（Chart.js）
- 報表匯出為 CSV、Excel
- 後台排程任務每日自動抓資料

## 🔧 使用技術
- Django 5.x
- BeautifulSoup (抓台灣銀行匯率)
- Chart.js（前端圖表）
- Pandas（匯出 Excel）
- Django 管理命令 + Windows Task Scheduler（定時排程）

## 📸 系統畫面截圖
<img width="1771" height="419" alt="登入畫面" src="https://github.com/user-attachments/assets/bfe23c63-4028-476f-aadb-07390356d421" />
<img width="1728" height="1178" alt="幣別查詢" src="https://github.com/user-attachments/assets/1bfa8669-4520-4188-b5fe-c2abc0c412f4" />
<img width="1672" height="1075" alt="幣別圖表" src="https://github.com/user-attachments/assets/55adb079-0cf2-4157-820a-f558bc1495c6" />


## 📁 專案架構
（如上方目錄結構）

## 🚀 安裝與執行
```bash
git clone ...
pip install -r requirements.txt
python manage.py migrate
python manage.py fetch_rates   # 用windows自動排程抓匯率
python manage.py runserver
