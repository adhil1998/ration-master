from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView, UpdateAPIView

from common.permissions import IsAuthenticated, IsAdmin, MultiPermissionView, IsShop, IsCard
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from supply.filter import StockFilter
from supply.models import Product, Stock, MonthlyQuota
from supply.serializer import ProductSerializer, StockSerializer, MonthlyQuotaSerializer


class ProductView(ListCreateAPIView):
    """View for product list and create"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class StockView(ListCreateAPIView, MultiPermissionView):
    """View for product list and create"""
    permissions = {
        'GET': (IsAuthenticated, ),
        'POST': (IsAuthenticated, IsAdmin)
    }
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filterset_class = StockFilter


class MonthlyQuotaView(ListCreateAPIView, UpdateAPIView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsAdmin)
    }
    serializer_class = MonthlyQuotaSerializer
    queryset = MonthlyQuota.objects.all()
