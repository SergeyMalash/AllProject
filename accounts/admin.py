from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account

# admin.site.register(Account, UserAdmin)
admin.site.register(Account)
