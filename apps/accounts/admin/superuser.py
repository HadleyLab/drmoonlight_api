from django.contrib.auth.admin import UserAdmin


class SuperUserAdmin(UserAdmin):
    list_display = ('pk', 'full_name', 'is_active', )
