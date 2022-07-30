from django.contrib import admin

# Register your models here.
from supply.models import Product, Stock, Token, Purchase, MonthlyQuota, Holidays, PublicHolidays, Notification

admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Token)
admin.site.register(Purchase)
admin.site.register(MonthlyQuota)
admin.site.register(Holidays)
admin.site.register(PublicHolidays)
admin.site.register(Notification)



