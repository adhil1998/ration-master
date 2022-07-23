from rest_framework import serializers
from django.db.models import Sum, F
from django.contrib.auth import authenticate

from accounts.constants import UserType
from accounts.models import User, Admin
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
        user.save()
        user.user.type = UserType.ADMIN
        return user
