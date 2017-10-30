from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin


class ApplicationAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ('pk', 'shift', 'owner', 'state', )
    readonly_fields = ('state', )
    fsm_field = ['state', ]
