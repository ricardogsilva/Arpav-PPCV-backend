from django.contrib import admin
from .models import *


class VariableAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )


class ForecastModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )


class ScenarioAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )


class DataSeriesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )


class YearPeriodAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )

class TimeWindowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )

class ValueTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )

admin.site.register(Variable, VariableAdmin)
admin.site.register(ForecastModel, ForecastModelAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(DataSeries, DataSeriesAdmin)
admin.site.register(YearPeriod, YearPeriodAdmin)
admin.site.register(TimeWindow, TimeWindowAdmin)
admin.site.register(ValueType, ValueTypeAdmin)
