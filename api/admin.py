from django.contrib import admin

from api.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'cash_buy', 'cash_sell')
    list_filter = ('currency', 'date')
    search_fields = ('currency',)

