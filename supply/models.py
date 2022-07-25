from django.db import models
from django.db.models import IntegerField, CharField, \
    ForeignKey, BooleanField, DateTimeField, TextField, DateField

from common.functions import encode
from common.models import AbstractBaseModel
from supply.constants import UnitType, TokenStatus
from accounts.models import RationShop, User, Card
from accounts.constants import CardType, AgeGroupType


# Create your models here.


class Product(AbstractBaseModel):
    """Store product details"""
    name = CharField(max_length=100, default='')
    unit = IntegerField(default=UnitType.KG, choices=UnitType.choices())

    def __str__(self):
        return self.name + ' ' + UnitType(value=self.unit).name


class Stock(AbstractBaseModel):
    """To store information about product stock"""
    product = ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    shop = ForeignKey(RationShop, on_delete=models.CASCADE, related_name='stock')
    quantity = IntegerField()

    def __str__(self):
        return f"{self.product.name} {self.shop.location} {self.quantity}"


class Token(AbstractBaseModel):
    """To store Token data"""
    card = ForeignKey(Card, on_delete=models.CASCADE, related_name='toke',
                      null=True, blank=True)
    shop = ForeignKey(RationShop, on_delete=models.CASCADE, related_name='toke',
                      null=True, blank=True)
    number = IntegerField(null=True, blank=True)
    time = DateTimeField(default=None, null=True, blank=True)
    status = IntegerField(default=TokenStatus.INITIATED,
                          choices=TokenStatus.choices())


class Purchase(AbstractBaseModel):
    """To store purchase details"""
    token = ForeignKey(Token, on_delete=models.CASCADE, related_name='purchase')
    product = ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase')
    quantity = IntegerField()

    class Meta:
        unique_together = ['token', 'product']


class MonthlyQuota(AbstractBaseModel):
    """To store product quantity availabale for each card owner"""
    product = ForeignKey(Product, on_delete=models.CASCADE, related_name='quota')
    quantity = IntegerField()
    card_type = IntegerField(default=CardType, choices=CardType.choices())
    age_group = IntegerField(default=None, choices=AgeGroupType.choices())
    date = DateField(auto_now_add=True)
    current_year = IntegerField(default=0)
    current_month = IntegerField(default=0)

    class Meta:
        unique_together = ['product', 'card_type', 'age_group',
                           'current_year', 'current_month']

    def save(self, *args, **kwargs):
        """"""
        self.current_month = self.date.month
        self.current_year = self.date.year
        super(MonthlyQuota, self).save(*args, **kwargs)


class Holidays(AbstractBaseModel):
    """To store holy days"""
    shop = ForeignKey(RationShop, on_delete=models.CASCADE)
    holidays = TextField(default="[]")
    date = DateField(auto_now_add=True)
    current_year = IntegerField(default=0)
    current_month = IntegerField(default=0)

    class Meta:
        unique_together = ['shop', 'current_year', 'current_month']


class PublicHolidays(AbstractBaseModel):
    """To store holy days"""
    holidays = TextField(default="[]")
    date = DateField(auto_now_add=True)
    current_year = IntegerField(default=0)
    current_month = IntegerField(default=0)

    class Meta:
        unique_together = ['current_year', 'current_month']



