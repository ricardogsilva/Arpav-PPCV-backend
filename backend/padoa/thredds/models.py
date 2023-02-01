# from django.db import models
from django.contrib.gis.db import models
from padoa.forecastattributes.models import Variable, ForecastModel, Scenario, DataSeries, \
    YearPeriod, TimeWindow, ValueType #, TimeRange
# from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

# Create your models here.
available_palettes = (
        "default",
        "default-inv",
        "div-BrBG",
        "div-BrBG-inv",
        "div-BuRd",
        "div-BuRd-inv",
        "div-BuRd2",
        "div-BuRd2-inv",
        "div-PRGn",
        "div-PRGn-inv",
        "div-PiYG",
        "div-PiYG-inv",
        "div-PuOr",
        "div-PuOr-inv",
        "div-RdBu",
        "div-RdBu-inv",
        "div-RdGy",
        "div-RdGy-inv",
        "div-RdYlBu",
        "div-RdYlBu-inv",
        "div-RdYlGn",
        "div-RdYlGn-inv",
        "div-Spectral",
        "div-Spectral-inv",
        "psu-inferno",
        "psu-inferno-inv",
        "psu-magma",
        "psu-magma-inv",
        "psu-plasma",
        "psu-plasma-inv",
        "psu-viridis",
        "psu-viridis-inv",
        "seq-BkBu",
        "seq-BkBu-inv",
        "seq-BkGn",
        "seq-BkGn-inv",
        "seq-BkRd",
        "seq-BkRd-inv",
        "seq-BkYl",
        "seq-BkYl-inv",
        "seq-BlueHeat",
        "seq-BlueHeat-inv",
        "seq-Blues",
        "seq-Blues-inv",
        "seq-BuGn",
        "seq-BuGn-inv",
        "seq-BuPu",
        "seq-BuPu-inv",
        "seq-BuYl",
        "seq-BuYl-inv",
        "seq-GnBu",
        "seq-GnBu-inv",
        "seq-Greens",
        "seq-Greens-inv",
        "seq-Greys",
        "seq-Greys-inv",
        "seq-GreysRev",
        "seq-GreysRev-inv",
        "seq-Heat",
        "seq-Heat-inv",
        "seq-OrRd",
        "seq-OrRd-inv",
        "seq-Oranges",
        "seq-Oranges-inv",
        "seq-PuBu",
        "seq-PuBu-inv",
        "seq-PuBuGn",
        "seq-PuBuGn-inv",
        "seq-PuRd",
        "seq-PuRd-inv",
        "seq-Purples",
        "seq-Purples-inv",
        "seq-RdPu",
        "seq-RdPu-inv",
        "seq-Reds",
        "seq-Reds-inv",
        "seq-YlGn",
        "seq-YlGn-inv",
        "seq-YlGnBu",
        "seq-YlGnBu-inv",
        "seq-YlOrBr",
        "seq-YlOrBr-inv",
        "seq-YlOrRd",
        "seq-YlOrRd-inv",
        "seq-cubeYF",
        "seq-cubeYF-inv",
        "x-Ncview",
        "x-Ncview-inv",
        "x-Occam",
        "x-Occam-inv",
        "x-Rainbow",
        "x-Rainbow-inv",
        "x-Sst",
        "x-Sst-inv"
)
available_styles = (
    "default-scalar",
    "colored_contours",
    "contours",
    "raster"
)
### MAP MODEL:
class Map(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    forecast_model = models.ForeignKey(ForecastModel, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    data_series = models.ForeignKey(DataSeries, on_delete=models.CASCADE)
    year_period = models.ForeignKey(YearPeriod, on_delete=models.CASCADE)
    time_window = models.ForeignKey(TimeWindow, on_delete=models.CASCADE, null=True)
    value_type = models.ForeignKey(ValueType, on_delete=models.CASCADE)
    #timerange = models.ForeignKey(TimeRange, on_delete=models.CASCADE)
    # time dimension? #todo check #TIME FROM  #TIME TO #INTERVAL STRING P1Y in python
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    time_interval = models.CharField(max_length=255,null=True, blank=True)
    csr = models.CharField(max_length=255,null=True, blank=True, default='CRS:84')
    spatialbounds = models.PolygonField (blank=True, null=True)
# LAYER
    layer_id = models.CharField(max_length=255, null=False, blank=False) 
    # layer_name = models.CharField(max_length=255, null=False, blank=False) #removed
    path = models.CharField(max_length=400, null=False, blank=False) 
    # layer_url = models.URLField(max_length=800, blank=False, null=False)
    elevation = models.IntegerField(null=True, blank=True)
    # style = models.CharField(max_length=255, null=True, blank=True)
    palette = models.CharField(max_length=255, null=True, blank=True) 
    unit = models.CharField(max_length=255, null=True, blank=True)
    # numcolorbands = models.IntegerField(default=80)
    # color_scale_range = models.CharField(max_length=255, null=True, blank=True)
    color_scale_min = models.IntegerField(null=True, blank=True)  
    color_scale_max = models.IntegerField(null=True, blank=True) 

### MAP MODEL:
class UserDownload(models.Model):
    public = models.BooleanField(default=False)
    membership = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    accept_disclaimer = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    parameters = models.TextField(max_length=2000, null=False, blank=False, default='')

@receiver(post_save, sender=Map)
def my_handler(sender, **kwargs):
    cache.clear()
