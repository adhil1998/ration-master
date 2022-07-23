from django.db import models
from django.db.models import IntegerField, CharField, \
    ForeignKey, BooleanField, DateTimeField, TextField

from common.functions import encode
from common.models import AbstractBaseModel
from supply.constants import UnitType
from accounts.models import RationShop, User, Card
from accounts.constants import CardType, AgeGroupType


# Create your models here.


class Product(AbstractBaseModel):
    """Store product details"""
    name = CharField(max_length=100, default='')


class Stock(AbstractBaseModel):
    """To store information about product stock"""
    product = ForeignKey(Product, on_delete=models.CASCADE)
    shop = ForeignKey(RationShop, on_delete=models.CASCADE)
    quantity = IntegerField()
    unit = IntegerField(default=UnitType.KG, choices=UnitType.choices())


class Token(AbstractBaseModel):
    """To store Token data"""
    card = ForeignKey(Card, on_delete=models.CASCADE)
    RationShop = ForeignKey(RationShop, on_delete=models.CASCADE)
    number = IntegerField()
    time = DateTimeField(default=None)


class Purchase(AbstractBaseModel):
    """To store purchase details"""
    token = ForeignKey(Token, on_delete=models.CASCADE)
    product = ForeignKey(Product, on_delete=models.CASCADE)
    quantity = IntegerField()


class MonthlyQuota(AbstractBaseModel):
    """To store product quantity availabale for each card owner"""
    product = ForeignKey(Product, on_delete=models.CASCADE)
    quantity = IntegerField()
    card_type = IntegerField(default=CardType, choices=CardType.choices())
    age_group = IntegerField(default=None, choices=AgeGroupType.choices())


class Holidays(AbstractBaseModel):
    """To store holy days"""
    shop = ForeignKey(RationShop, on_delete=models.CASCADE)
    holidays = TextField()



