from django.urls import path

from supply.views import ProductView, StockView, MonthlyQuotaView, HolidaysView, \
    PublicHolidaysView, TokenView, PurchaseView, StockUpdateView, TokenDetailView, TokenDetailIdView, \
    NotificationListCreateView

urlpatterns = [
    path(r'products/', ProductView .as_view()),
    path(r'stock/', StockView .as_view()),
    path(r'stock/<idencode:pk>/', StockUpdateView .as_view()),
    path(r'quota/', MonthlyQuotaView .as_view()),
    path(r'quota/<idencode:pk>/', MonthlyQuotaView .as_view()),
    path(r'shop/holiday/', HolidaysView .as_view()),
    path(r'public/holiday/', PublicHolidaysView .as_view()),
    path(r'token/create/', TokenView .as_view()),
    path(r'token/', TokenView .as_view()),
    path(r'token/active/', TokenDetailView .as_view()),
    path(r'token/get/<idencode:pk>/', TokenDetailIdView.as_view()),
    path(r'token/update/<idencode:pk>/', TokenView.as_view()),
    path(r'purchase/', PurchaseView.as_view()),
    path(r'notification/', NotificationListCreateView.as_view()),
]
