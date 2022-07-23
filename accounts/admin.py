from django.contrib import admin
from accounts.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(RationShop)
admin.site.register(Card)
admin.site.register(OtpToken)
admin.site.register(AccessToken)
admin.site.register(Member)
