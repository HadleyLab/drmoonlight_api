from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from apps.accounts.models import Resident
from .user import UserAdmin


@admin.register(Resident)
class ResidentAdmin(FSMTransitionMixin, UserAdmin):
    list_display = ('pk', 'full_name', 'is_active', 'state', )
    readonly_fields = ('state', )
    fsm_field = ['state', ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'state', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
