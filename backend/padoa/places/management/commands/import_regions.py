import json
import os

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.core.management import BaseCommand
from padoa.places.models import Regions, Provinces, Cities

IMPORTING_REGIONS = [4,5,6]

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):

    # Show this when the user types help
    help = "Importing regions"

    def add_arguments(self, parser):
        parser.add_argument('--files', help='Set a comma separated files to import')


    def handle(self, *args, **options):
        filePath = os.path.join(settings.RESOURCE_ROOT, 'places/')
        print('IMPORTING REGIONS..')
        feature_collection = open(os.path.join(filePath+'limits_IT_regions.geojson'), 'r')
        jsonData = json.load(feature_collection)
        for geom in jsonData['features']:
            item = Regions.objects.filter(pk=geom['properties']['reg_istat_code_num']).exists()
            if not item and geom['properties']['reg_istat_code_num'] in IMPORTING_REGIONS:
                shape = GEOSGeometry(json.dumps(geom['geometry']), srid=4326)
                if shape and isinstance(shape, Polygon):
                    shape = MultiPolygon([shape])
                if shape and (isinstance(shape, MultiPolygon)):
                    featureData = {
                        'geometry': shape,
                        'centroid': shape.centroid,
                        'name': geom['properties']['reg_name'],
                        'id': geom['properties']['reg_istat_code_num'],
                    }
                    item = Regions.objects.create(**featureData)
                    print(item)
        print('IMPORTING PROVINCES..')
        feature_collection = open(os.path.join(filePath+'limits_IT_provinces.geojson'), 'r')
        jsonData = json.load(feature_collection)
        for geom in jsonData['features']:
            item = Provinces.objects.filter(pk=geom['properties']['prov_istat_code_num']).exists()
            if not item and geom['properties']['reg_istat_code_num'] in IMPORTING_REGIONS:
                shape = GEOSGeometry(json.dumps(geom['geometry']), srid=4326)
                if shape and isinstance(shape, Polygon):
                    shape = MultiPolygon([shape])
                if shape and (isinstance(shape, MultiPolygon)):
                    featureData = {
                        'geometry': shape,
                        'centroid': shape.centroid,
                        'name': geom['properties']['prov_name'],
                        'id': geom['properties']['prov_istat_code_num'],
                        'region_id': geom['properties']['reg_istat_code_num'],
                    }
                    item = Provinces.objects.create(**featureData)
                    print(item)
        print('IMPORTING CITIES..')
        feature_collection = open(os.path.join(filePath+'limits_IT_municipalities.geojson'), 'r')
        jsonData = json.load(feature_collection)
        for geom in jsonData['features']:
            item = Cities.objects.filter(pk=geom['properties']['com_istat_code_num']).exists()
            if not item and geom['properties']['reg_istat_code_num'] in IMPORTING_REGIONS:
                shape = GEOSGeometry(json.dumps(geom['geometry']), srid=4326)
                if shape and isinstance(shape, Polygon):
                    shape = MultiPolygon([shape])
                if shape and (isinstance(shape, MultiPolygon)):
                    featureData = {
                        'geometry': shape,
                        'centroid': shape.centroid,
                        'name': geom['properties']['name'],
                        'id': geom['properties']['com_istat_code_num'],
                        'region_id': geom['properties']['reg_istat_code_num'],
                        'province_id': geom['properties']['prov_istat_code_num'],
                        'prov_code': geom['properties']['prov_acr'],
                    }
                    item = Cities.objects.create(**featureData)
                    print(item)


        self.stdout.write("All regions imported!")
