# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
import uuid
from django.db import models
from django.contrib.gis.db import models as gismodel
from django.conf import settings
from django.contrib import admin
from django.db.models import Subquery
from django.contrib.gis.admin import OSMGeoAdmin, GeoModelAdmin
from guardian.admin import GuardedModelAdmin, GuardedModelAdminMixin
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.admin import ModelAdmin
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from django.dispatch import receiver
from django.core.cache import cache


class Regions(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False, editable=False)
    name = models.CharField(max_length=190, blank=True, null=True)
    geometry = gismodel.MultiPolygonField(srid=4326, blank=False, null=False, db_index=True)
    centroid = gismodel.PointField(srid=4326, blank=False, null=False, db_index=True)
    def __str__(self):
        return self.name


class Provinces(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False, editable=False)
    name = models.CharField(max_length=190, blank=True, null=True)
    region = models.ForeignKey(Regions, blank=True, null=True, to_field='id', on_delete=models.CASCADE, related_name='province_regions')
    geometry = gismodel.MultiPolygonField(srid=4326, blank=False, null=False, db_index=True)
    centroid = gismodel.PointField(srid=4326, blank=False, null=False, db_index=True)
    def __str__(self):
        return self.name

class Cities(models.Model):
    class Meta:
        verbose_name_plural = "cities"
    id = models.IntegerField(primary_key=True, null=False, blank=False, editable=False)
    name = models.CharField(max_length=190, blank=True, null=True)
    prov_code = models.CharField(max_length=190, blank=True, null=True)
    region = models.ForeignKey(Regions, blank=True, null=True, to_field='id', on_delete=models.CASCADE, related_name='city_regions')
    province = models.ForeignKey(Provinces, blank=True, null=True, to_field='id', on_delete=models.CASCADE, related_name='province')
    geometry = gismodel.MultiPolygonField(srid=4326, blank=False, null=False, db_index=True)
    centroid = gismodel.PointField(srid=4326, blank=False, null=False, db_index=True)
    def __str__(self):
        return self.name + ' ('+self.prov_code+')'

@receiver(post_save, sender=Cities)
def my_handler(sender, **kwargs):
    cache.clear()

@admin.register(Regions)
class RegionsAdmin(GeoModelAdmin):
    pass
@admin.register(Provinces)
class ProvincesAdmin(GeoModelAdmin):
    pass
@admin.register(Cities)
class CitiesAdmin(GeoModelAdmin):
    pass
