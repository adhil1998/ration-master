from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField
from django.db.models import Sum, F

from accounts.models import RationShop
from accounts.serializers import ShopSerializer
from common.fields import IdencodeField
from supply.models import Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'idencode']


class StockSerializer(serializers.ModelSerializer):
    """"""
    product = IdencodeField(related_model=Product, write_only=True)
    shop = IdencodeField(related_model=RationShop, write_only=True)
    product_details = ProductSerializer(source='product')
    shop_details = ShopSerializer(source='shop')

    class Meta:
        model = Stock
        fields = ['product', 'shop', 'idencode', 'quantity', 'product_details',
                  'shop_details']
