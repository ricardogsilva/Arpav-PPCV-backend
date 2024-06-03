import json, zipfile, io
# import StringIO
from django.http import FileResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.routers import BaseRouter
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from padoa.thredds.models import Map, UserDownload
from padoa.thredds.serializers import MapSerializer, UserDownloadSerializer
from djcore.djcore.core.mixins import OptionListModelMixin
from padoa.thredds.utils import WmsQueryNew, NCSSQuery


def save_userdownloaddata(data):
    userDownloadData = {
        'reason': data.get('other_reason') if data.get('reason') == 'other' else data.get('reason'),
        'place': data.get('place','-'),
        'accept_disclaimer': data.get('accept_disclaimer') == 'true',
        'membership': data.get('membership','-'),
        'public': data.get('public') == 'true',
        'parameters': json.dumps(data)
    }
    serializer = UserDownloadSerializer(data=userDownloadData)
    serializer.is_valid(raise_exception=True)
    serializer.save()

class MyOffsetPagination(LimitOffsetPagination):
    default_limit = 8000
    max_limit = 8000

class MapList(ListAPIView,OptionListModelMixin,GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    pagination_class = MyOffsetPagination

    @method_decorator(cache_page(3600*7*24))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# class TimeSeries(APIView):
#     permission_classes = (AllowAny,)
#     def get(self, request):
#         DATASET_PATH = request.query_params.get('dataset_path')
#         LAYER = request.query_params.get('layer')
#         m = Map.objects.filter(path=DATASET_PATH).first()
#         ext = map(lambda x : str(x), m.spatialbounds.extent)
#         bbox = ",".join(ext)
#         wms = WmsQueryNew(DATASET_PATH, LAYER, m.time_start, m.time_end, bbox, X=1, Y=1, WIDTH=2, HEIGHT=2)
#         time_serie = wms.get_timeseries()
#         response_dictionary = {
#                 "results":{
#                     "map": MapSerializer(m).data,
#                     "timeseries": time_serie,
#                 }
#             }
#         return Response(response_dictionary)


class NCSSTimeserie(APIView, BaseRouter):
    permission_classes = (AllowAny,)
    def get(self, request):
        if(request.query_params.get('id')):
            ids = [request.query_params.get('id')]
        elif(request.query_params.get('ids')):
            ids = request.query_params.get('ids').split(',')
        maps = Map.objects.filter(id__in=ids).all()
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        # time_end = request.query_params.get('time_end', m.time_end)
        # time_start = request.query_params.get('time_start')
        print([[m.path, m.layer_id, m.time_start, m.time_end] for m in maps])
        results = [NCSSQuery(m.path, m.layer_id, m.time_start, m.time_end, latitude=latitude, longitude=longitude).getTimeserie(extraDict=MapSerializer(m).data) for m in maps]
        response_dictionary = {
                "results": results
            }
        return Response(response_dictionary)

    def post(self, request):
        save_userdownloaddata(request.data)
        ids = request.data.get('ids')
        maps = Map.objects.filter(id__in=ids).all()
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        start = request.data.get('start')
        end = request.data.get('end')
        results = [{
            'data': NCSSQuery(m.path, m.layer_id, m.time_start, m.time_end, latitude=latitude, longitude=longitude).getRawTimeseries(start=start, end=end),
            'filename': m.path.replace('/','_') + '.csv'
        } for m in maps]
        variable_id = maps[0].variable_id
        buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(buffer, 'w')
        [zip_file.writestr(r['filename'], r['data']) for r in results]
        zip_file.close()
        response = HttpResponse(buffer.getvalue())
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = 'attachment; filename='+variable_id+'.zip'
        return response

class NCSSSubset(APIView, BaseRouter):
    permission_classes = (AllowAny,)
    def post(self, request):
        save_userdownloaddata(request.data)
        m = Map.objects.filter(id=request.data.get('id')).first()
        res = NCSSQuery(m.path, m.layer_id, request.data.get('time_start'), request.data.get('time_end'), north=request.data.get('north'), west=request.data.get('west'), east=request.data.get('east'), south=request.data.get('south')).getSubsetNetcdf()
        filename = m.path.replace('/', '_') + '.nc'
        response = FileResponse(res, as_attachment=True, filename=filename)
        response.set_headers({'Content-Type': 'application/octet-stream'})
        return response;
    def get(self, request):
        save_userdownloaddata(request.query_params)
        m = Map.objects.filter(id=request.query_params.get('id')).first()
        res = NCSSQuery(m.path, m.layer_id, request.query_params.get('time_start'), request.query_params.get('time_end'), north=request.query_params.get('north'), west=request.query_params.get('west'), east=request.query_params.get('east'), south=request.query_params.get('south')).getSubsetNetcdf()
        filename = m.path.replace('/', '_') + '.nc'
        response = FileResponse(res, as_attachment=True, filename=filename)
        response.set_headers({'Content-Type': 'application/octet-stream'})
        return response;

#http://localhost:8000/thredds/ncss/netcdf/?id=7&time_start=1976-07-17T00%3A00%3A00Z&time_end=2099-07-17T00%3A00%3A00Z&north=46.0&west=13.0&east=14&south=45
#http://192.167.167.61:8000/thredds/ncss/netcdf/?id=7&time_start=1976-07-17T00%3A00%3A00Z&time_end=2099-07-17T00%3A00%3A00Z&north=46.0&west=13.0&east=14&south=45
