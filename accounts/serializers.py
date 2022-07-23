from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField
from django.db.models import Sum, F
from django.contrib.auth import authenticate

from accounts.constants import UserType
from accounts.models import User, Admin, RationShop, Card, OtpToken
from common.exceptions import UnauthorizedAccess, BadRequest
from common.fields import KWArgsObjectField


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

    class Meta:
        """meta info"""
        model = RationShop
        fields = ['username', 'idencode', 'email', 'mobile', 'password',
                  'first_name', 'last_name', 'employee_name', 'employee_id',
                  'location']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Override user creation"""
        password = validated_data.pop('password')
        user = super(ShopSerializer, self).create(validated_data)
        user.set_password(password)
        user.type = UserType.SHOP
        user.save()
        return user


class CardSerializer(serializers.ModelSerializer):
    """Serializer for lis and create User(s)"""
    holder_name = CharField(required=True)
    card_number = IntegerField(required=True)
    card_type = IntegerField(required=True)

    class Meta:
        """meta info"""
        model = Card
        fields = ['idencode', 'email', 'mobile', 'card_number', 'holder_name',
                  'card_type']

    def create(self, validated_data):
        """Override user creation"""
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
