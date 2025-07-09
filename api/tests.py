from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Product
from django.urls import reverse
from datetime import date

class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # 建立初始匯率資料
        self.product1 = Product.objects.create(
            currency='USD',
            cash_buy=31.23,
            cash_sell=31.45,
            date=date(2024, 7, 1)
        )

        self.product2 = Product.objects.create(
            currency='JPY',
            cash_buy=0.219,
            cash_sell=0.223,
            date=date(2024, 7, 2)
        )

        self.valid_payload = {
            'currency': 'EUR',
            'cash_buy': '34.56',
            'cash_sell': '35.12',
            'date': '2024-07-08'
        }

    def test_create_product(self):
        """測試新增匯率資料"""
        response = self.client.post('/api/products/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_list_products(self):
        """測試取得匯率列表"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 預設開啟分頁時用 data['results']

    def test_filter_by_currency(self):
        """測試依幣別篩選"""
        response = self.client.get('/api/products/?currency=usd')  # 不區分大小寫
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['currency'], 'USD')

    def test_ordering_by_cash_buy(self):
        """測試依買入價排序（遞減）"""
        response = self.client.get('/api/products/?ordering=-cash_buy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        values = [item['cash_buy'] for item in response.data['results']]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_update_product(self):
        """測試 PUT 更新匯率資料"""
        update_data = {
            'currency': 'USD',
            'cash_buy': '32.00',
            'cash_sell': '32.50',
            'date': '2024-07-01'
        }
        url = f'/api/products/{self.product1.id}/'
        response = self.client.put(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(float(self.product1.cash_buy), 32.00)

    def test_delete_product(self):
        """測試刪除匯率資料"""
        url = f'/api/products/{self.product2.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)  # 原本 2 筆，刪掉 1 筆

    def test_invalid_create(self):
        """測試錯誤資料，缺少 currency"""
        invalid_payload = {
            'cash_buy': '30.00',
            'cash_sell': '31.00',
            'date': '2024-07-08'
        }

        response = self.client.post('/api/products/', invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('currency', response.data)  # 確認錯誤回傳中有 currency 欄位錯誤
