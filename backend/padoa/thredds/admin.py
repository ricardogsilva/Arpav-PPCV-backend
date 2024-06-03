from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from .models import *


class MapAdmin(GeoModelAdmin):
    list_display = (
        'id',
        'path',
        # 'layer_id',
        'variable_id',
        'forecast_model_id',
        'scenario_id',
        'data_series_id',
        'year_period_id',
        'value_type_id',
        # 'time_window_id',
        'unit',
        'palette',
        'color_scale_min',
        'color_scale_max'
    )
    list_filter = ('variable_id', 'forecast_model_id', 'value_type_id', 'data_series_id', 'year_period_id',)


admin.site.register(Map, MapAdmin)
admin.site.register(UserDownload)
