from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView, UpdateAPIView

from common.permissions import IsAuthenticated, IsAdmin, MultiPermissionView, IsShop, IsCard
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from supply.models import Product
from supply.serializer import ProductSerializer


class ProductView(ListCreateAPIView):
    """View for product list and create"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

