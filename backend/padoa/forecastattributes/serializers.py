from rest_framework.serializers import ModelSerializer, BaseSerializer
from rest_framework import serializers
from padoa.forecastattributes.models import *


class BaseAttributeSerializer(ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    order_item = serializers.IntegerField()

    class Meta:
        read_only_fields = ('id','name','description','order_item')
        fields = '__all__'

    # def to_internal_value(self, data):
    #     if type(data) is str:
    #         data = self.ModelClass.objects.get(name=data)
    #     return super(BaseAttributeSerializer, self).to_internal_value(data)

    # def to_representation(self, instance):
    #     return instance.name


class VariableSerializer(BaseAttributeSerializer):
    class Meta:
        model = Variable
        fields = '__all__'

class ForecastModelSerializer(BaseAttributeSerializer):
    class Meta:
        model = ForecastModel
        fields = '__all__'

class ScenarioSerializer(BaseAttributeSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'

class DataSeriesSerializer(BaseAttributeSerializer):
    class Meta:
        model = DataSeries
        fields = '__all__'

class YearPeriodSerializer(BaseAttributeSerializer):
    class Meta:
        model = YearPeriod
        fields = '__all__'

class TimeWindowSerializer(BaseAttributeSerializer):
    class Meta:
        model = TimeWindow
        fields = '__all__'

class ValueTypeSerializer(BaseAttributeSerializer):
    class Meta:
        model = ValueType
        fields = '__all__'

# class TimeRangeSerializer(BaseAttributeSerializer):
#     class Meta:
#         model = TimeRange
#         fields = '__all__'
