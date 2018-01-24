from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import Scheduler
from .user import UserAdmin


@admin.register(Scheduler)
class SchedulerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'avatar',
            'facility_name', 'department_name', )}),
        (_('Permissions'), {'fields': ('is_active', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
