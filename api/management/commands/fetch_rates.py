# api/management/commands/fetch_rates.py

from django.core.management.base import BaseCommand
from api.models import Product
from bs4 import BeautifulSoup
import requests
from datetime import date
import re

class Command(BaseCommand):
    help = '從台灣銀行匯率頁面抓中英文幣別一起儲存'

    def handle(self, *args, **kwargs):
        url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('❌ 無法取得匯率資料'))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('table.table tbody tr')
        today = date.today()

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue

            full_name = cols[0].find('div').text.strip()
            match = re.search(r'(.+?)\s+\((\w+)\)', full_name)

            if not match:
                continue

            currency_name = match.group(1).strip()  # 中文名稱
            currency_code = match.group(2).strip()  # 英文代碼

            # 把中英文合併為一個字串存入 currency 欄位
            currency_label = f'{currency_name} ({currency_code})'

            cash_buy = cols[1].text.strip()
            cash_sell = cols[2].text.strip()

            if cash_buy == '-' or cash_sell == '-':
                continue

            obj, created = Product.objects.get_or_create(
                currency=currency_label,
                date=today,
                defaults={
                    'cash_buy': cash_buy,
                    'cash_sell': cash_sell
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f' 匯入 {currency_label} 匯率成功'))
            else:
                self.stdout.write(f' 已存在 {currency_label} 匯率，略過')
