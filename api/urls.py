from django.urls import path, include
from rest_framework import routers
from api import views
from api.views import product_list_view,export_csv,export_excel

# 建立路由器
router = routers.DefaultRouter()


# 註冊 網址 對應視圖
router.register(r'products', views.ProductViewSet)


# 建立列表 網址對應路由
urlpatterns = [
    path('', include(router.urls)),
    path('report/', product_list_view,name='product_list'),
    path('report/csv/', export_csv, name='report_csv'),
    path('report/excel/', export_excel, name='report_excel'),

]