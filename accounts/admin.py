from django.contrib import admin
from accounts.models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class MemberAdmin(admin.TabularInline):
    """Class view to customize user device admin."""

    model = Member
    fk_name = "card"
    list_display = ('idencode', 'card')


class CardAdmin(admin.ModelAdmin):
    """Class view to customize user device admin."""

    list_display = ('idencode', 'card_type')
    inlines = [MemberAdmin]


class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "type", "is_staff")


admin.autodiscover()
admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(RationShop)
admin.site.register(Card, CardAdmin)
admin.site.register(OtpToken)
admin.site.register(AccessToken)
admin.site.register(Member)
