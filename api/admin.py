from django.contrib import admin
from api.models import Product
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'date', 'cash_buy', 'cash_sell', 'colored_rate')
    readonly_fields = ('cash_buy', 'cash_sell') #無法更改匯率
    list_filter = ('currency', 'date')
    search_fields = ('currency',)
    ordering = ['-date']
    fieldsets = (
        ('基本資料', {
            'fields': ('currency', 'date')
        }),
        ('匯率資訊', {
            'fields': ('cash_buy', 'cash_sell'),
            'classes': ['collapse'],
        }),
    )

    @admin.display(description="買入/賣出比")
    def colored_rate(self, obj):
        if obj.cash_buy and obj.cash_sell:
            rate = round(float(obj.cash_sell) / float(obj.cash_buy), 3)
            color = 'green' if rate > 1 else 'red'
            return format_html(f'<b style="color:{color}">{rate}</b>')
        return "-"
