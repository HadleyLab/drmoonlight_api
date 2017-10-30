from django.contrib import admin

from apps.accounts.models import ResidencyProgram


@admin.register(ResidencyProgram)
class ResidencyProgramAdmin(admin.ModelAdmin):
    pass
