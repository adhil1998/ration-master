from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField, \
    DateField, PrimaryKeyRelatedField, DateTimeField
from django.db.models import Sum, F

from accounts.constants import AgeGroupType
from accounts.models import RationShop, Card
from accounts.serializers import ShopSerializer, CardSerializer
from common.exceptions import BadRequest
from common.fields import IdencodeField, KWArgsObjectField
from common.services import send_otp
from supply.constants import TokenStatus
from supply.models import Product, Stock, MonthlyQuota, Holidays, PublicHolidays, \
    Token, Purchase
from supply.utilities import create_token_time


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
    date = DateField()

    class Meta:
        model = PublicHolidays
        fields = ['holidays', 'date']

    def create(self, validated_data):
        """Override create"""
        try:
            holiday, create = PublicHolidays.objects.get_or_create(
                current_year=validated_data['date'].year,
                current_month=validated_data['date'].month)
            holiday.holidays = validated_data['holidays']
            holiday.save()
        except Exception as e:
            raise BadRequest("update" + str(e))
        return holiday


class PurchaseSerializer(serializers.ModelSerializer):
    """serializer for purchase"""
    token = IdencodeField(related_model=Token, write_only=True)
    product = IdencodeField(related_model=Product, serializer=ProductSerializer)

    class Meta:
        model = Purchase
        fields = ['token', 'product', 'quantity']

    def validate(self, data):
        """"""
        if not data['token'].status == TokenStatus.INITIATED:
            raise BadRequest("NOT VALID TOKEN")
        return data


class TokenSerializer(serializers.ModelSerializer):
    """"""
    shop = IdencodeField(related_model=RationShop, serializer=ShopSerializer)
    card = KWArgsObjectField(serializer=CardSerializer)

    class Meta:
        model = Token
        fields = ['idencode', 'card', 'shop', 'number', 'time', 'status', ]
        extra_kwargs = {
            'time': {'read_only': True},
            'number': {'read_only': True}
        }

    def create(self, validated_data):
        """"""
        validated_data['time'], validated_data['number'] = create_token_time(validated_data['shop'])
        validated_data['status'] = TokenStatus.INITIATED
        token = Token.objects.filter(
            card=validated_data['card'],
            time__year=validated_data['time'].year,
            time__month=validated_data['time'].month,
            status__in=[TokenStatus.COMPLETED, TokenStatus.INITIATED]).exists()
        if token:
            raise BadRequest('Token already created')
        token = Token.objects.create(**validated_data)
        send_otp(token.card.mobile, f'Your token for VQ Ration successfully booked. '
                                    f'Number:{token.number}\n'
                                    f'Time&Date:{token.time.strftime("%H:%M %d-%m-%y")}')
        return token

    def to_representation(self, instance):
        data = {"idencode": instance.idencode,
                "shop": ShopSerializer(instance.shop).data,
                "time": datetime.strftime(instance.time, "%H:%M %d-%m-%y"),
                "card": CardSerializer(instance.card).data,
                "number": instance.number,
                "status": instance.status,
                "purchase": PurchaseSerializer(instance.purchase.all(), many=True).data}
        return data
