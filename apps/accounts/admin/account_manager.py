from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import AccountManager
from .user import UserAdmin


@admin.register(AccountManager)
class AccountManagerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
