from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import *


class TurbineAdmin(ModelAdmin):
    model=Turbine
    list_display = ('location', 'status')

class AudioAdmin(ModelAdmin):
    model=Audio
    list_display = ('turbine', 'datetime', 'value')

class AnomalyEventsAdmin(ModelAdmin):
    model=AnomalyEvents
    list_display = ('audio',)


modeladmin_register(TurbineAdmin)
modeladmin_register(AudioAdmin)
modeladmin_register(AnomalyEventsAdmin)
