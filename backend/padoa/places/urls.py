from django.conf.urls import url
from .views import CitiesList
from rest_framework import routers

app_name = 'places'
router = routers.SimpleRouter()
router.register(r'cities', CitiesList)

urlpatterns =  router.urls

