from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


class SchedulerAdmin(UserAdmin):
    list_display = ('pk', 'full_name', 'is_active', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'facility_name',
            'department_name', )}),
        (_('Permissions'), {'fields': ('is_active', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', ),
        }),
        (_('Personal info'), {'fields': ('facility_name', 'department_name',)}),
    )
