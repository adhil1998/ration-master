from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveAPIView, UpdateAPIView

from common.exceptions import BadRequest
from common.permissions import IsAuthenticated, IsAdmin, MultiPermissionView, IsShop, IsCard
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from supply.constants import TokenStatus
from supply.filter import StockFilter, TokenFilter
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


class TokenView(ListCreateAPIView, RetrieveAPIView, UpdateAPIView,
                MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsCard),
        'PATCH': (IsAuthenticated, IsShop)
    }
    serializer_class = TokenSerializer
    queryset = Token.objects.all().order_by('number')
    filterset_class = TokenFilter

    def patch(self, request, pk, **kwargs):
        """Override update method"""
        instance = self.get_object()
        validated_data = self.request.data
        if not 'status' in validated_data:
            raise BadRequest('Status missing in body')
        elif validated_data['status'] == TokenStatus.CANCELED:
            instance.status = TokenStatus.CANCELED
        else:
            instance.status = TokenStatus.COMPLETED
            for purchase in instance.purchase.all():
                stock = Stock.objects.get(
                    product=purchase.product, shop=purchase.token.shop)
                stock.quantity = stock.quantity - purchase.quantity
                stock.save()
        instance.save()
        return success_response(TokenSerializer(instance).data, 'Updated')


class TokenDetailView(RetrieveAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated, IsCard),
    }
    serializer_class = TokenSerializer

    def get_object(self):
        """"""
        try:
            token = Token.objects.get(card=self.kwargs['card'])
        except:
            raise BadRequest('NO ACTIVE TOKENS')
        return token


class PurchaseView(ListCreateAPIView, RetrieveAPIView, MultiPermissionView):
    """"""
    permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsCard)
    }
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
