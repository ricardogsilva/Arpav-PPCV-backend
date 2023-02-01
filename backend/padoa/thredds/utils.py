from time import sleep
import xmltodict as xmltodict
from django.conf import settings
# from pydap.cas.get_cookies import setup_session
from pydap.client import open_url
import requests, json
from requests.auth import HTTPBasicAuth, _basic_auth_str
from threddsclient import read_url
from dateutil.parser import parse as timeparse
from datetime import datetime, timedelta, time as timed
import pytz, urllib
from io import StringIO
import pandas as pd



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Authorization': _basic_auth_str(settings.THREDDS['user'], settings.THREDDS['password']),
}
def getSession():
    session = requests.Session()
    session.headers.update(headers)
    return session

session = getSession()

def getThreddsDirectory(directory):
    url = settings.THREDDS['host']+'catalog/'+directory+'/catalog.html'
    return read_url(url)

def getWmsPath(dataset):
    return 'wms/'+dataset

def getWmsUrl(dataset):
    return settings.THREDDS['host']+getWmsPath(dataset)

def getWmsCapabilitiesUrl(dataset):
    return getWmsUrl(dataset)+'?request=GetCapabilities&service=WMS&version=1.3.0'

def getOpenDapUrl(dataset):
    return settings.THREDDS['host']+'dodsC/'+dataset #+'.ascii'

def openDapUrl(dataset):
    url=getOpenDapUrl(dataset)
    session = getSession()
    return open_url(url, session=session)

def getWmsCapabilities(dataset):
    url=getWmsCapabilitiesUrl(dataset)
    # print(url)
    sleep(0.2)
    session.get(getOpenDapUrl(dataset))
    sleep(0.1)
    res = session.get(url)
    if res.status_code != 200:
        if res.headers.get('location'):
            r = session.get(res.headers.get('location'))
            return getWmsCapabilities(dataset)
        print(res.headers.get('location'))
        print(res.__dict__)
        print(url)
        res = session.get(url)
    return xmltodict.parse(res.content)


def getWmsMetadata(dataset, layer):
    url = getWmsUrl(dataset)+'?request=GetMetadata&item=layerDetails&layerName='+layer
    sleep(0.2)
    session.get(getOpenDapUrl(dataset))
    sleep(0.1)
    res = session.get(url)
    if res.status_code != 200:
        if res.headers.get('location'):
            r = session.get(res.headers.get('location'))
            return getWmsMetadata(dataset)
        res = session.get(url)
    # print(res.content)
    return json.loads(res.content)

def getWmsLayers(dataset):
    capabilities = getWmsCapabilities(dataset)
    return capabilities['WMS_Capabilities']['Capability']['Layer']['Layer']['Layer']

def getLayerAttributes(dataset):
    capabilities = getWmsCapabilities(dataset)
    return capabilities['WMS_Capabilities']['Capability']

def getLayerMinMax(dataset, layer):
    url = getWmsUrl(dataset)+'?request=GetMetadata&item=minmax&layers='+layer['Name']+'&styles=default-scalar&version=1.1.1&bbox=10.05%2C44.2698%2C14.25%2C47.6298&srs=CRS%3A84&crs=CRS%3A84&height=100&width=100'
    res = session.get(url)
    res = res.content.decode("utf-8")
    return json.loads(res)
#     capabilities = getWmsCapabilities(dataset)
#     return capabilities['WMS_Capabilities']['Capability']['Layer']['Layer']['Layer'][layer]['Extent']


def setDateToUtc(date):
    if not isinstance(date, datetime):
        date = timeparse(date)
    return date.replace(tzinfo=pytz.timezone('utc'))

class WmsQueryNew:
    def __init__(self, DATASET_PATH, LAYER, TIME_START, TIME_END, BBOX, X=1, Y=1, WIDTH=2, HEIGHT=2):
        self.dataset_path = DATASET_PATH
        self.layer = LAYER
        self.time_to = setDateToUtc(TIME_END)
        self.time_from = setDateToUtc(TIME_START)

        self.setDefaultData(BBOX, X, Y, WIDTH, HEIGHT)

    def setDefaultData(self, BBOX, X=1, Y=1, WIDTH=2, HEIGHT=2):
        self.default_options = {
            "REQUEST": "GetTimeseries",
            # "ELEVATION": "0",
            "TRANSPARENT": "true",
            # "STYLES": "boxfill/rainbow",
            "COLORSCALERANGE": "-50,50",
            "NUMCOLORBANDS": "20",
            "LOGSCALE": "false",
            "SERVICE": "WMS",
            "VERSION": "1.1.1",
            "FORMAT": "image/png",
            "SRS": "EPSG:4326",
            "CRS": "EPSG:4326",
            "INFO_FORMAT": "text/json",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               # "url": "https://iws.ismar.cnr.it/thredds/wms/tmes/TMES_sea_level_20190907.nc",
            "BBOX": BBOX,
            "X": X,
            "Y": Y,
            "WIDTH": WIDTH,
            "HEIGHT": HEIGHT,
            # "TIME": "2019-09-17T00:00:00.000Z/2019-09-17T23:00:00.000Z",
            # "QUERY_LAYERS": "sea_level-mean",
        }


    def get_timeseries(self):
        data = self.query(True)
        print(data)
        # TODO: formattare i dati come [ [time0, value0], [time1, value1] ]
        return data


    def query(self, raw=False):
        options = self.default_options
        options.update({
            "TIME": self.time_from.isoformat()[0:19] + '.000Z' if self.time_to is None else self.time_from.isoformat()[0:19] + '.000Z' + '/' + self.time_to.isoformat()[0:19] + '.000Z',
            "QUERY_LAYERS": self.layer,
            "LAYERS": self.layer,
        })
        url = getWmsUrl(self.dataset_path) + '?' + urllib.parse.urlencode(options)
        r = session.get(url=url)
        if r.status_code != 200:
            if r.headers.get('location'):
                rh = session.get(r.headers.get('location'))
                return self.query(raw)
        queryData = json.loads(r.content)
        print(json.dumps(queryData))
        return queryData

class NCSSQuery:
    def __init__(self, dataset, layer, time_start, time_end, latitude=None, longitude=None, north=None, west=None, east=None, south=None, session=None):
        # print(['__init__', time_start, time_end])
        self.dataset = dataset
        self.layer = layer
        self.time_start = time_start
        self.time_end = time_end
        self.latitude = latitude
        self.longitude = longitude
        self.session = session
        self.north = north
        self.west = west
        self.east = east
        self.south = south
        self.url = settings.THREDDS['host'] + 'ncss/grid/' + self.dataset

    def getRawTimeseries(self, ext='csv', start=None, end=None):
        params = {
            'var': self.layer,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'time_start': self.time_start.isoformat()[0:19] + 'Z' if start is None else start,
            'time_end': self.time_end.isoformat()[0:19] + 'Z' if end is None else end,
            'timeStride': '',
            'vertCoord': '',
            'accept': ext,
        }
        url = self.url + '?' + urllib.parse.urlencode(params)
        print(url)
        session.get(getOpenDapUrl(self.dataset))
        sleep(0.1)
        res = session.get(url)
        if res.status_code != 200 and res.headers.get('location'):
            rh = session.get(res.headers.get('location'))
            return self.getRawTimeseries(ext)
        if res.status_code != 200:
            print('Error in getTimeserie')
            print(res.content)
        return res.content.decode("utf-8")

    def getTimeserie(self, extraDict={}):
        res = self.getRawTimeseries()
        df = pd.read_csv(StringIO(res), sep=",")
        column_headers = list(df.columns.values)
        latitude = df[column_headers[2]][0]
        longitude = df[column_headers[3]][0]
        unit = column_headers[4].replace(self.layer, '').replace('unit=', '')[2:-2]

        df = df.drop(['station', column_headers[2], column_headers[3]], axis=1).rename(columns={column_headers[4]: 'value'})
        res = json.loads(df.to_json(orient='records'))
        return {
            'dataset': {
                **extraDict,
                'lat': latitude,
                'lng': longitude,
                'unit': unit,
                'dataset': self.dataset,
                'layer': self.layer,
            },
            'values': res,
        }

    def getSubsetNetcdf(self):
        params = {
            'var': self.layer,
            'north': self.north,
            'west': self.west,
            'east': self.east,
            'south': self.south,
            # 'vertStride': '1',
            # 'timeStride': '1',
            'horizStride': '1',
            # 'addLatLon': 'true',
            'time_start': self.time_start,
            'time_end': self.time_end,
            # 'accept': 'netcdf3'
            'accept': 'netcdf4-classic'
        }
        url = self.url + '?' + urllib.parse.urlencode(params)
        print(url)
        session.get(getOpenDapUrl(self.dataset))
        sleep(0.1)
        res = session.get(url)
        if res.status_code != 200:
            print('Error in getSubsetNetcdf')
            print(url)
            if res.headers.get('location'):
                rh = session.get(res.headers.get('location'))
                return self.getTimeserie()
            # print(res.status_code)
            # print(res.content)
            # raise Exception('Error in getSubsetNetcdf')
        return res
