from django.contrib import admin

from apps.accounts.models import Speciality


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    pass
