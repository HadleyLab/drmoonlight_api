from django.contrib import admin

from apps.shifts.models import *
from .application import ApplicationAdmin


admin.site.register(Shift)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Message)
