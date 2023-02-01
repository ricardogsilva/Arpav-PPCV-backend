from padoa.forecastattributes.views import *
from rest_framework import routers
app_name = 'forcastattributes'

router = routers.SimpleRouter()
router.register(r'variables', VariableList)
router.register(r'forecast_models', ForecastModelList)
router.register(r'scenarios', ScenarioList)
router.register(r'data_series', DataSeriesList)
router.register(r'year_periods', YearPeriodList)
router.register(r'time_windows', TimeWindowList)
router.register(r'value_types', ValueTypeList)
#router.register(r'time_range', TimeRangeList)

urlpatterns =  router.urls