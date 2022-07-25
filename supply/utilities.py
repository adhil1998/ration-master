import ast
from datetime import datetime, timedelta

from common.exceptions import BadRequest
from supply.constants import MAX_TOKEN
from supply.models import Token, Holidays, PublicHolidays


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

