from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from .serializers import CitiesSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from .models import Cities
from ..thredds.views import MyOffsetPagination
from django.views.decorators.cache import cache_page


class CitiesList(ListAPIView,GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitiesSerializer
    pagination_class = MyOffsetPagination

    @method_decorator(cache_page(3600*7*24))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)