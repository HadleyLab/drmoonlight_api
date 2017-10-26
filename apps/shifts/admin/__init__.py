from django.contrib import admin

from apps.shifts.models import *


admin.site.register(Shift)
admin.site.register(Application)
admin.site.register(Message)
