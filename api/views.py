from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters

from api.Filters import ProductFilter
from api.models import Product
from api.serializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['date', 'cash_buy', 'cash_sell']
    ordering = ['-date']  # 預設排序為日期由新到舊
    search_fields = ['currency']