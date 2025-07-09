import os
import glob
import json
import requests

# 1️⃣ 設定 JSON 檔案資料夾
json_dir = r"C:\Users\88691\PycharmProjects\PythonProject\爬蟲"

# 2️⃣ 自動尋找最新的 JSON 檔案
file_pattern = os.path.join(json_dir, "Taiwan_Bank_ExchangeRate_*.json")
json_files = glob.glob(file_pattern)

if not json_files:
    print("❌ 找不到 JSON 檔案")
    exit()

latest_file = sorted(json_files)[-1]
print(f"📄 使用最新 JSON 檔案：{os.path.basename(latest_file)}")

# 3️⃣ 讀取 JSON 檔案
with open(latest_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 4️⃣ API 設定
API_URL = "http://127.0.0.1:8000/api/rate/"
HEADERS = {
    "Content-Type": "application/json"
}

# 5️⃣ 檢查資料是否存在，再決定是否 POST
for item in data:
    currency = item.get('currency')
    date = item.get('date')

    if not currency or not date:
        print(f"⚠️ 資料缺少 currency 或 date，略過: {item}")
        continue

    # 發 GET 請求查是否已有相同資料
    params = {
        'currency': currency,
        'from_date': date,
        'to_date': date
    }

    try:
        check_response = requests.get(API_URL, params=params, headers=HEADERS)
        check_response.raise_for_status()
        existing = check_response.json()

        if existing:
            print(f"🔁 資料已存在（{currency}, {date}），跳過。")
            continue

        # 資料不存在，送出 POST
        post_response = requests.post(API_URL, json=item, headers=HEADERS)
        post_response.raise_for_status()

        print(f"✅ 已新增：{currency} - {date}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 錯誤：{e}")
        print("🧨 錯誤資料內容：", json.dumps(item, ensure_ascii=False, indent=2))

        # 若有 POST response 也印出錯誤內容（避免變數未定義先判斷）
        if 'post_response' in locals():
            print("🧨 回傳錯誤訊息：", post_response.text)