from rest_framework import routers
from .views import index
from django.conf.urls import url

app_name = 'core'

urlpatterns = [
    url(r'^$', index, name='index'),
]
