# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class BaseAttribute(models.Model):
    id = models.CharField(max_length=255, primary_key=True, null=False, blank=False, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.CharField(max_length=255, unique=False, null=True, blank=True)
    order_item = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['order_item']

class Variable(BaseAttribute):
    @property
    def attribute_type(self):
        return 'Variable'

class ForecastModel(BaseAttribute):
    @property
    def attribute_type(self):
        return 'ForecastModel'

class Scenario(BaseAttribute):
    @property
    def attribute_type(self):
        return 'Scenario'

# YES / NO ? TO VERIFY IF NEEDED come label: Anomalia trentennale || Serie annuali / stagionali
class DataSeries(BaseAttribute):
    @property
    def attribute_type(self):
        return 'DataSeries'

class YearPeriod(BaseAttribute): # season N or annual
    @property
    def attribute_type(self):
        return 'YearPeriod'

class TimeWindow(BaseAttribute): # tw1/tw2 only for anomalie trentennali
    @property
    def attribute_type(self):
        return 'TimeWindow'

class ValueType(BaseAttribute): # anomaly | absolute
    @property
    def attribute_type(self):
        return 'ValueType'

# se decommenti, decommentare anche Serializer, urls e view
# class TimeRange(BaseAttribute):
#     @property
#     def attribute_type(self):
#         return 'TimeRange'


@receiver(post_save, sender=Variable)
def variable_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=ForecastModel)
def model_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=Scenario)
def scenario_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=DataSeries)
def datas_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=YearPeriod)
def year_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=ValueType)
def value_handler(sender, **kwargs):
    cache.clear()
@receiver(post_save, sender=TimeWindow)
def time_handler(sender, **kwargs):
    cache.clear()
