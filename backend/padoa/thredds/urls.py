from padoa.thredds.views import *
from django.urls import include, path
from rest_framework import routers
app_name = 'thredds'

router = routers.SimpleRouter()
router.register(r'maps', MapList)

urlpatterns = [
    # path('wms/timeserie/', TimeSeries.as_view()),
    path('ncss/timeserie/', NCSSTimeserie.as_view()),
    path('ncss/netcdf/', NCSSSubset.as_view())
]
urlpatterns +=  router.urls
