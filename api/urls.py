from django.urls import path, include
from rest_framework import routers
from api import views

# 建立路由器
router = routers.DefaultRouter()

# 註冊 網址 對應視圖
router.register(r'products', views.ProductViewSet)


# 建立列表 網址對應路由
urlpatterns = [
    path('', include(router.urls)),
]