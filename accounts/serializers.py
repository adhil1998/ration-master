from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField
from django.db.models import Sum, F, Count, Q, Case, When
from django.contrib.auth import authenticate

from accounts.constants import UserType, AgeGroupType
from accounts.models import User, Admin, RationShop, Card, OtpToken, Member
from common.exceptions import UnauthorizedAccess, BadRequest
from common.fields import KWArgsObjectField
from supply.constants import TokenStatus
from supply.models import Product, MonthlyQuota, Stock, Purchase


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""

    class Meta:
        """meta info"""
        model = Admin
        fields = ['username', 'idencode', 'email', 'dob', 'mobile',
                  'password', 'first_name', 'last_name', 'district']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Override user creation"""
        password = validated_data.pop('password')
        user = super(AdminSerializer, self).create(validated_data)
        user.set_password(password)
        user.type = UserType.ADMIN
        user.save()
        return user


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""
    employee_name = CharField(required=True)
    employee_id = IntegerField(required=True)
    location = CharField(required=True)
    stock = SerializerMethodField()
    current_stock = SerializerMethodField()

    class Meta:
        """meta info"""
        model = RationShop
        fields = ['username', 'idencode', 'email', 'mobile', 'password',
                  'first_name', 'last_name', 'employee_name', 'employee_id',
                  'location', 'verified', 'stock', 'current_stock']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_stock(self, obj):
        """Get stock details of shop"""
        stocks = Stock.objects.filter(shop=obj).exclude(quantity=0)
        stock_list = []
        for stock in stocks:
            data = {
                "product_idencode": stock.product.idencode,
                "name": stock.product.name,
                "quantity": stock.quantity,
                "unit": stock.product.unit
            }
            stock_list.append(data)
        return stock_list

    def get_current_stock(self, obj):
        """Get current stock details ( After exclude quantity booked by token )"""
        stocks = Stock.objects.filter(shop=obj).exclude(quantity=0)
        stock_list = []
        for stock in stocks:
            purchased_quantity = Purchase.objects.filter(
                token__status=TokenStatus.INITIATED).aggregate(Sum(
                'quantity', default=0))['quantity__sum']
            data = {
                "name": stock.product.name,
                "quantity": stock.quantity - purchased_quantity,
                "unit": stock.product.unit
            }
            stock_list.append(data)
        return stock_list

    def create(self, validated_data):
        """Override user creation"""
        password = validated_data.pop('password')
        user = super(ShopSerializer, self).create(validated_data)
        user.set_password(password)
        user.type = UserType.SHOP
        user.save()
        return user


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for contacts"""
    card = KWArgsObjectField(write_only=True)

    class Meta:
        model = Member
        fields = ['name', 'age', 'age_group', 'idencode',
                  'gender', 'card', 'occupation']

    def create(self, validated_data):
        """Override create"""
        contact = super(MemberSerializer, self).create(validated_data)
        return contact


class CardSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""
    holder_name = CharField(required=True)
    card_number = IntegerField(required=True)
    card_type = IntegerField(required=True)
    available_quota = SerializerMethodField()
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        """meta info"""
        model = Card
        fields = ['idencode', 'email', 'mobile', 'card_number', 'holder_name',
                  'card_type', 'verified', 'available_quota', 'members']

    def get_available_quota(self, obj):
        """get availble amound of prodects per card in month"""
        query = Q(
            quota__current_month=datetime.now().month,
            quota__current_year=datetime.now().year,
            quota__card_type=obj.card_type)
        products = Product.objects.annotate(ration=Count('quota', filter=query)).exclude(ration=0)
        child = obj.members.filter(age_group=AgeGroupType.CHILD).count()
        adults = obj.members.filter(age_group=AgeGroupType.ADULT).count()
        product_list = []
        for product in products:
            try:
                adults_quantity = MonthlyQuota.objects.get(
                    current_month=datetime.now().month, current_year=datetime.now().year,
                    card_type=obj.card_type, product=product,
                    age_group=AgeGroupType.ADULT).quantity * adults
            except:
                adults_quantity = 0
            try:
                child_quantity = MonthlyQuota.objects.get(
                    current_month=datetime.now().month, current_year=datetime.now().year,
                    card_type=obj.card_type, product=product,
                    age_group=AgeGroupType.CHILD).quantity * child
            except:
                child_quantity = 0
            data = {
                "idencode": product.idencode,
                "name": product.name,
                "quantity": adults_quantity + child_quantity,
                "unit": product.unit
            }
            product_list.append(data)
        return product_list

    def create(self, validated_data):
        """Override user creation"""
        validated_data['username'] = validated_data['card_number']
        user = super(CardSerializer, self).create(validated_data)
        user.type = UserType.CARD
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        """Overide login"""
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise UnauthorizedAccess('Not valid credentials')
        if user.type == UserType.SHOP.value:
            if not user.rationshop.verified:
                raise BadRequest("NOT VERIFIED")
        return user

    def to_representation(self, instance):
        """Override instance output"""
        data = {
            "idencode": instance.idencode,
            "name": instance.username,
            "type": instance.type,
            "bearer": instance.issue_access_token(),
        }
        return data


class LoginOTPSerializer(serializers.Serializer):
    card_number = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

    def create(self, validated_data):
        """Overide login"""
        card_number = validated_data['card_number']
        otp = validated_data['otp']
        card = Card.objects.get(card_number=card_number)
        try:
            otp = OtpToken.objects.get(user=card, otp=otp)
        except:
            raise BadRequest("INVALID CREDENTIALS")
        if datetime.now() > otp.expired_in.replace(tzinfo=None):
            raise BadRequest("OTP EXPIRED")
        otp.refresh()
        if not card.verified:
            raise BadRequest("Card not verified")
        return card

    def to_representation(self, instance):
        """Override instance output"""
        data = {
            "idencode": instance.idencode,
            "name": instance.username if instance.username else instance.holder_name,
            "type": instance.type,
            "bearer": instance.issue_access_token(),
        }
        return data


class ShopLiteSerializer(serializers.ModelSerializer):

    class Meta:
        """meta info"""
        model = RationShop
        fields = ['first_name', 'idencode', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

