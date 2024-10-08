from django.contrib import admin
from django.contrib.admin import TabularInline

from account.models import Account, Interest, AccountProfile


class AccountInfoTabularInline(TabularInline):
    model = AccountProfile
    extra = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountInfoTabularInline,)
    search_fields = ("username", "phone")
    list_filter = ("is_staff", "is_superuser")


admin.site.register(
    [
        Interest,
    ]
)