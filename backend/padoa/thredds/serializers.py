import urllib

from rest_framework.serializers import ModelSerializer, BaseSerializer
from rest_framework import serializers
from padoa.thredds.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer


# class MapSerializer(GeoFeatureModelSerializer):
class MapSerializer(ModelSerializer):
    variable_id = serializers.CharField()
    # variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    forecast_model_id = serializers.CharField()
    # forecast_model = models.ForeignKey(ForecastModel, on_delete=models.CASCADE)
    scenario_id = serializers.CharField()
    # scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    data_series_id = serializers.CharField()
    # data_series = models.ForeignKey(DataSeries, on_delete=models.CASCADE)
    year_period_id = serializers.CharField()
    # year_period = models.ForeignKey(YearPeriod, on_delete=models.CASCADE)
    time_window_id = serializers.CharField()
    # time_window = models.ForeignKey(TimeWindow, on_delete=models.CASCADE, null=True)
    value_type_id = serializers.CharField()
    # value_type = models.ForeignKey(ValueType, on_delete=models.CASCADE)
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()
    time_interval = serializers.CharField()
    csr = serializers.CharField()
    # spatialbounds = serializers.CharField(read_only=True)
# LAYER
    layer_id = serializers.CharField()
    path = serializers.CharField()
    # layer_url = serializers.CharField()
    palette = serializers.CharField()
    unit = serializers.CharField()
    color_scale_min = serializers.IntegerField()
    color_scale_max = serializers.IntegerField()
    bbox = serializers.SerializerMethodField()
    elevation = serializers.IntegerField()
    legend = serializers.SerializerMethodField()

    def truncate(self, value, decimals = 3):
        return int(value * 10 ** decimals) / 10 ** decimals

    def get_bbox(self, obj):
        ext = obj.spatialbounds.extent
        # return [[ext[2], ext[0]], [ext[3], ext[1]]]
        return [[self.truncate(ext[2] - 0.002), self.truncate(ext[0] + 0.002)], [self.truncate(ext[3] - 0.002), self.truncate(ext[1] + 0.002)]]


    def get_legend(self, obj):
        params = {
            'REQUEST': 'GetLegendGraphic',
            'numcolorbands': '100',
            'LAYERS': obj.layer_id,
            'STYLES': 'default-scalar/'+obj.palette,
            'colorscalerange': str(obj.color_scale_min)+','+str(obj.color_scale_max),
        }
        return f'/thredds/wms/{obj.path}?' + urllib.parse.urlencode(params)

    class Meta:
        model = Map
        read_only_fields = (
            'variable_id',
            # 'forecast_model_id',
            # 'data_series_id',
            # 'year_period_id',
            # 'time_window_id',
            # 'value_type_id',
            'time_start',
            'time_end',
            'time_interval',
            'csr',
            # 'spatialbounds',
            'layer_id',
            'path',
            # 'layer_url',
            'palette',
            'unit',
            'color_scale_min',
            'color_scale_max',
            'elevation',
            'bbox',
        )
        fields = '__all__'
        # geo_field = "spatialbounds"


class UserDownloadSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False)
    place = serializers.CharField(required=False, allow_blank=True)
    membership = serializers.CharField(required=False, allow_blank=True)
    public = serializers.BooleanField(default=False)
    accept_disclaimer = serializers.BooleanField(default=False)
    date = serializers.DateField(required=False)
    parameters = serializers.CharField(max_length=2000, required=False)

    def create(self, validated_data):
        return UserDownload.objects.create(**validated_data)

    class Meta:
        model = UserDownload
        fields = ('reason', 'accept_disclaimer', 'place', 'membership', 'public', 'date', 'parameters')
