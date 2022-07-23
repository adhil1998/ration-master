from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from django.db.models import IntegerField, CharField, \
    ForeignKey, BooleanField, DateTimeField
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from random import randint

from common.functions import encode
from common.models import AbstractBaseModel
from accounts.constants import UserType, OTPType, GenderType, AgeGroupType, CardType


# Create your models here.


class User(AbstractUser):
    """User model"""
    type = IntegerField(default=UserType.CARD,
                        choices=UserType.choices())
    mobile = CharField(max_length=15, default='', unique=True)

    def issue_access_token(self):
        """Function to get or create user access token."""
        token, created = AccessToken.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()
        return token.key

    def issue_otp_token(self):
        """Function to get or create user access token."""
        token, created = OtpToken.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()
        return token.key

    def __str__(self):
        return self.username

    @property
    def idencode(self):
        """Return converted id"""
        return encode(self.id)


class Admin(User):
    """To store admin details"""
    district = CharField(max_length=50, default='')
    dob = DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Admins'


class RationShop(User):
    """To store shop details"""
    employee_name = CharField(max_length=100, default='')
    employee_id = CharField(max_length=15, default='')
    location = CharField(max_length=100, default='')
    verified = BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'RationShops'

    def __str__(self):
        return self.username + self.employee_name + self.employee_id


class Card(User):
    """To store card owner details"""
    card_number = CharField(max_length=15, default='', unique=True)
    holder_name = CharField(max_length=100, default='')
    card_type = IntegerField(default=CardType.WHITE,
                             choices=CardType.choices())
    verified = BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Cards'

    def __str__(self):
        return self.username + self.holder_name


class Member(AbstractBaseModel):
    """To store member detail"""
    card = ForeignKey(Card, on_delete=models.CASCADE)
    name = CharField(max_length=100, default='')
    age = IntegerField(default=None)
    age_group = IntegerField(default=None, choices=AgeGroupType.choices())
    gender = IntegerField(default=None, choices=GenderType.choices())
    occupation = CharField(max_length=100, default=None)

    def __str__(self):
        return self.name + self.card.card_number


class AccessToken(models.Model):
    """To create and store bearer token"""
    user = ForeignKey('User', on_delete=models.CASCADE)
    key = CharField(max_length=200, unique=True)
    active = BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.key:
            self.key = get_random_string(90)
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = get_random_string(90)
        if AccessToken.objects.filter(key=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.key = self.generate_unique_key()
        self.save()


class OtpToken(AbstractBaseModel):
    """To store OTP information"""
    user = ForeignKey(User, on_delete=models.CASCADE)
    otp = IntegerField(null=True)
    is_active = BooleanField(default=False)
    type = IntegerField(default=None, choices=OTPType.choices())
    expired_in = DateTimeField(default=None)

    def __str__(self):
        return self.user.card.holder_name + str(self.otp)

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.otp:
            self.key = randint(100000, 999999)
        self.expired_in = datetime.now() + timedelta(minutes=10)
        return super(OtpToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = randint(100000, 999999)
        if OtpToken.objects.filter(otp=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.otp = self.generate_unique_key()
        self.save()

