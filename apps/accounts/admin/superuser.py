from django.contrib import admin

from apps.accounts.models import SuperUser
from .user import UserAdmin


@admin.register(SuperUser)
class SuperUserAdmin(UserAdmin):
    list_display = ('pk', 'full_name', 'is_active', )
