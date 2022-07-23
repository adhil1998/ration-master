from django.contrib import admin
from accounts.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.autodiscover()
admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(RationShop)
admin.site.register(Card)
admin.site.register(OtpToken)
admin.site.register(AccessToken)
admin.site.register(Member)
