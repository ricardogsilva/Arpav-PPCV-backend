from rest_framework import routers
from .views import *
# from django.conf.urls import url


app_name = 'groups'

router = routers.SimpleRouter()
router.register(r'', GroupListView)

urlpatterns = router.urls
