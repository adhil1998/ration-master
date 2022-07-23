from rest_framework import serializers
from rest_framework.serializers import CharField, IntegerField, SerializerMethodField
from django.db.models import Sum, F
from django.contrib.auth import authenticate

from accounts.constants import UserType
from accounts.models import User, Admin, RationShop, Card
from common.exceptions import UnauthorizedAccess
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
