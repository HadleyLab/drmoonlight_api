from django.contrib import admin

from apps.shifts.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
