from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from padoa.forecastattributes.models import Variable, ForecastModel, Scenario, DataSeries, YearPeriod, \
    TimeWindow, ValueType #, TimeRange
from padoa.forecastattributes.serializers import VariableSerializer, ForecastModelSerializer, ScenarioSerializer, \
    DataSeriesSerializer, YearPeriodSerializer, TimeWindowSerializer, ValueTypeSerializer #, TimeRangeSerializer
from djcore.djcore.core.mixins import OptionListModelMixin

class CachedParametersList(OptionListModelMixin, ListAPIView, GenericViewSet):
    # @method_decorator(cache_page(3600*7*24))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class VariableList(CachedParametersList):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer

class ForecastModelList(CachedParametersList):
    queryset = ForecastModel.objects.all()
    serializer_class = ForecastModelSerializer

class ScenarioList(CachedParametersList):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class DataSeriesList(CachedParametersList):
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer

class YearPeriodList(CachedParametersList):
    queryset = YearPeriod.objects.all()
    serializer_class = YearPeriodSerializer

class TimeWindowList(CachedParametersList):
    queryset = TimeWindow.objects.all()
    serializer_class = TimeWindowSerializer

class ValueTypeList(CachedParametersList):
    queryset = ValueType.objects.all()
    serializer_class = ValueTypeSerializer

# class TimeRangeList(CachedParametersList):
#     queryset = TimeRange.objects.all()
#     serializer_class = TimeRangeSerializer
