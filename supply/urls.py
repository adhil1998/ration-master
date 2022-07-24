from django.urls import path

from supply.views import ProductView, StockView

urlpatterns = [
    path(r'products/', ProductView .as_view()),
    path(r'stock/', StockView .as_view()),
]