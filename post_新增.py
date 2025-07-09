import requests
import json

url = "http://127.0.0.1:8000/api/products/"

json_path = r"C:\Users\88691\PycharmProjects\PythonProject\爬蟲\Taiwan_Bank_ExchangeRate_20250606.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {
    "Content-Type": "application/json"
}

# 逐筆發送資料
for item in data:
    try:
        response = requests.post(url, json=item, headers=headers)
        response.raise_for_status()  # 若 HTTP 狀態碼為 4xx/5xx，則拋出異常

        print("送出資料:", item)
        print("狀態碼:", response.status_code)
        print("回應資料:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"錯誤發生: {e}")