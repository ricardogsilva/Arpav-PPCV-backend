from rest_framework import routers
from .views import *
# from django.conf.urls import url


app_name = 'users'

router = routers.SimpleRouter()
router.register(r'', UserListView)
# router.register(r'option_list', UserOptionListView)
router.register(r'destroy', UserBulkView)
router.register(r'', UserViewSet)

urlpatterns = router.urls