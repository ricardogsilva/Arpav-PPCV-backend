from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Cities
import json

class CitiesSerializer(ModelSerializer):
    name = serializers.CharField(min_length=2,max_length=255)
    latlng = serializers.SerializerMethodField()
    # bbox = serializers.SerializerMethodField()

    def get_latlng(self, obj):
        postgis_point = obj.centroid
        return {'lng': postgis_point.x, 'lat':postgis_point.y}

    # def get_bbox(self, obj):
    #     return json.loads(obj.geometry.envelope.json)

    class Meta:
        model = Cities
        read_only_fields = (
            'id',
            'name',
            'latlng',
            # 'bbox'
        )
        fields = (
            'id',
            'name',
            'latlng',
            # 'bbox'
        )


