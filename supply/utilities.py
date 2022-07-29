import ast
from datetime import datetime, timedelta

from django.db.models import Count, Q, F

from accounts.constants import AgeGroupType
from common.exceptions import BadRequest
from supply.constants import MAX_TOKEN
from supply.models import Token, Holidays, PublicHolidays, Product, MonthlyQuota


def create_token_time(shop):
    tomorrow = datetime.now() + timedelta(days=1)
    date = get_valid_date(shop, tomorrow)
    token_count = Token.objects.filter(
            time__day=date.day, time__year=date.year, time__month=date.month).count()
    if token_count == 0:
        date = date.replace(hour=8, minute=30)
    elif token_count < 54:
        date = date.replace(hour=8, minute=30) + timedelta(minutes=5*token_count)
    else:
        date = date.replace(hour=3, minute=00) + timedelta(minutes=5*(token_count-54))
    return date, token_count + 1


def get_valid_date(shop, date):
    if date.month != datetime.now().month:
        raise BadRequest("NO TOKEN AVAILABLE FOR THIS MONTH")
    elif Holidays.objects.filter(
            current_month=datetime.now().month, shop=shop,
            current_year=datetime.now().year).exists() and date.day in ast.literal_eval(
        Holidays.objects.get(
            current_month=datetime.now().month, current_year=datetime.now().year).holidays):
        return get_valid_date(shop, date + timedelta(days=1))
    elif PublicHolidays.objects.filter(
            current_month=datetime.now().month,
            current_year=datetime.now().year).exists() and date.day in list(PublicHolidays.objects.get(
            current_month=datetime.now().month,
            current_year=datetime.now().year).holidays):
        return get_valid_date(shop, date + timedelta(days=1))
    elif Token.objects.filter(
            time__day=date.day, time__year=date.year, time__month=date.month).count() >= MAX_TOKEN:
        return get_valid_date(shop, date + timedelta(days=1))
    else:
        return date


def available_quota(token):
    """"""
    obj = token.card
    query = Q(
        quota__current_month=datetime.now().month,
        quota__current_year=datetime.now().year,
        quota__card_type=obj.card_type)
    purchase_ids = list(token.purchase.all().values_list('product__id', flat=True))
    stock_product_ids = list(token.shop.stock.all().values_list('product__id', flat=True))
    products = Product.objects.filter(id__in=stock_product_ids).annotate(ration=Count('quota', filter=query)).exclude(
        ration=0).exclude(id__in=purchase_ids)
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