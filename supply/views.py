from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveAPIView, UpdateAPIView

from common.permissions import IsAuthenticated, IsAdmin, MultiPermissionView, IsShop, IsCard
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from supply.filter import StockFilter
from supply.models import Product, Stock, MonthlyQuota, Holidays, PublicHolidays, Token, Purchase
from supply.serializer import ProductSerializer, StockSerializer, MonthlyQuotaSerializer, HolidaysSerializer, \
    PublicHolidaysSerializer, TokenSerializer, PurchaseSerializer


class ProductView(ListCreateAPIView):
    """View for product list and create"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class StockView(ListCreateAPIView, MultiPermissionView):
    """View for product list and create"""
    permissions = {
        'GET': (IsAuthenticated,),
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


class HolidaysView(ListCreateAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsAdmin or IsShop)
    }
    serializer_class = HolidaysSerializer
    queryset = Holidays.objects.all()


class PublicHolidaysView(ListCreateAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsAdmin)
    }
    serializer_class = PublicHolidaysSerializer
    queryset = PublicHolidays.objects.all()


class TokenView(ListCreateAPIView, RetrieveAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsCard)
    }
    serializer_class = TokenSerializer
    queryset = Token.objects.all()


class PurchaseView(ListCreateAPIView, RetrieveAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsCard)
    }
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
