from django.contrib import admin

from apps.shifts.models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    pass
