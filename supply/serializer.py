from datetime import datetime
from itertools import product

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField, \
    DateField, PrimaryKeyRelatedField
from django.db.models import Sum, F

from accounts.constants import AgeGroupType
from accounts.models import RationShop
from accounts.serializers import ShopSerializer
from common.exceptions import BadRequest
from common.fields import IdencodeField
from supply.models import Product, Stock, MonthlyQuota, Holidays, PublicHolidays


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'idencode']


class StockSerializer(serializers.ModelSerializer):
    """"""
    product = IdencodeField(related_model=Product, serializer=ProductSerializer)
    shop = IdencodeField(related_model=RationShop, serializer=ShopSerializer)

    class Meta:
        model = Stock
        fields = ['product', 'shop', 'idencode', 'quantity', ]


class MonthlyQuotaSerializer(serializers.ModelSerializer):
    """"""
    product = IdencodeField(related_model=Product, serializer=ProductSerializer)
    date = DateField()

    class Meta:
        model = MonthlyQuota
        fields = ['product', 'quantity', 'card_type', 'age_group', 'date',
                  'idencode']

    def create(self, validated_data):
        """Override create"""
        try:
            quota, create = MonthlyQuota.objects.get_or_create(**validated_data)
        except Exception as e:
            raise BadRequest("Already added quota for this month ...try to edit" + str(e))
        return quota

    def update(self, instance, validated_data):
        """Override update"""
        super(MonthlyQuotaSerializer, self).update(instance, validated_data)
        return instance


class HolidaysSerializer(serializers.ModelSerializer):
    """"""
    shop = IdencodeField(related_model=RationShop, serializer=ShopSerializer)
    date = DateField()

    class Meta:
        model = Holidays
        fields = ['shop', 'holidays', 'date']

    def create(self, validated_data):
        """Override create"""
        try:
            holiday, create = Holidays.objects.get_or_create(
                current_year=validated_data['date'].year,
                current_month=validated_data['date'].month,
                shop=validated_data['shop'])
            holiday.holidays = validated_data['holidays']
            holiday.save()
        except Exception as e:
            raise BadRequest("update" + str(e))
        return holiday


class PublicHolidaysSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = PublicHolidays
        fields = ['holidays', 'date']

    def create(self, validated_data):
        """Override create"""
        try:
            holiday, create = Holidays.objects.get_or_create(
                current_year=validated_data['date'].year,
                current_month=validated_data['date'].month)
            holiday.holidays = validated_data['holidays']
            holiday.save()
        except Exception as e:
            raise BadRequest("update" + str(e))
        return holiday
