import csv
import json
import openpyxl
from django.core.paginator import Paginator

from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay, TruncYear
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters

from api.Filters import ProductFilter
from api.models import Product
from api.serializers import ProductSerializer
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['date', 'cash_buy', 'cash_sell']
    ordering = ['-date']  # 預設排序為日期由新到舊
    search_fields = ['currency']


@login_required
def product_list_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    currency = request.GET.get('currency')
    group_by = request.GET.get('group_by', 'month')  # 預設按月

    # 選擇日期截斷函數與格式
    if group_by == 'day':
        trunc_func = TruncDay('date')
        date_format = '%Y-%m-%d'
    elif group_by == 'year':
        trunc_func = TruncYear('date')
        date_format = '%Y'
    else:
        trunc_func = TruncMonth('date')
        date_format = '%Y-%m'

    # 基本 queryset（不切片）
    base_qs = Product.objects.all()

    if start_date and end_date:
        base_qs = base_qs.filter(date__range=(start_date, end_date))

    if currency:
        base_qs = base_qs.filter(currency=currency)

    base_qs = base_qs.order_by('-date')

    # 分頁設定：每頁顯示 10 筆
    paginator = Paginator(base_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 幣別選項
    currency_options = Product.objects.values_list('currency', flat=True).distinct()

    # 建立所有日期標籤（取所有資料中日期的最大集合）
    # 先取得該期間、該幣別資料，做一次完整的period標籤集合
    all_periods_qs = base_qs.annotate(period=trunc_func).values('period').distinct().order_by('period')
    all_labels = [item['period'].strftime(date_format) for item in all_periods_qs]

    # ⭐ 圖表邏輯修正：只查詢所選幣別，否則查全部
    chart_dict = {}

    if currency:  # 有指定幣別，只查這個
        filtered = base_qs.filter(currency=currency)
        period_data = filtered.annotate(period=trunc_func) \
            .values('period') \
            .annotate(total=Sum('cash_buy')) \
            .order_by('period')
        data_map = {item['period'].strftime(date_format): float(item['total'] or 0) for item in period_data}
        data = [data_map.get(label, 0) for label in all_labels]
        chart_dict[currency] = {
            'labels': all_labels,
            'data': data
        }

    else:  # 沒指定幣別，全部幣別分別顯示，labels統一
        for curr in currency_options:
            filtered = base_qs.filter(currency=curr)
            monthly_data = filtered.annotate(period=trunc_func) \
                .values('period') \
                .annotate(total=Sum('cash_buy')) \
                .order_by('period')
            data_map = {item['period'].strftime(date_format): float(item['total'] or 0) for item in monthly_data}
            data = [data_map.get(label, 0) for label in all_labels]

            chart_dict[curr] = {
                'labels': all_labels,
                'data': data,
            }

    return render(request, 'report/product_list.html', {
        'products': page_obj,
        'chart_dict': json.dumps(chart_dict),
        'chart_dict_raw': chart_dict,
        'currency_options': currency_options,
        'group_by': group_by,
        'now': now(),
        'request': request,
    })


def export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    products = Product.objects.all()
    if start_date and end_date:
        products = products.filter(date__range=(start_date, end_date))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(['幣別', '現金買入', '現金賣出', '日期'])
    for product in products:
        writer.writerow([product.currency, product.cash_buy, product.cash_sell, product.date])
    return response

def export_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    products = Product.objects.all()
    if start_date and end_date:
        products = products.filter(date__range=(start_date, end_date))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "報表"
    ws.append(['幣別', '現金買入', '現金賣出', '日期'])

    for product in products:
        ws.append([product.currency, product.cash_buy, product.cash_sell, product.date])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    wb.save(response)
    return response