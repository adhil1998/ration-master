from django.urls import path

from supply.views import ProductView

urlpatterns = [
    path(r'products/', ProductView .as_view()),
]