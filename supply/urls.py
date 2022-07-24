from django.urls import path

from supply.views import ProductView, StockView, MonthlyQuotaView

urlpatterns = [
    path(r'products/', ProductView .as_view()),
    path(r'stock/', StockView .as_view()),
    path(r'quota/', MonthlyQuotaView .as_view()),
    path(r'quota/<idencode:pk>/', MonthlyQuotaView .as_view()),
]