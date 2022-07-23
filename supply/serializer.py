from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField
from django.db.models import Sum, F

from supply.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'unit', 'idencode']
