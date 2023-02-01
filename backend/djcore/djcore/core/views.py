from rest_framework import generics, viewsets, mixins, response
from djcore.djcore.core.mixins import OptionListModelMixin
from rest_framework.decorators import action, api_view, schema

class OptionListAPIView(OptionListModelMixin,
                  generics.GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    # @detail_route()
    # @list_route()
    def get(self, request, *args, **kwargs):
        return self.option_list(request, *args, **kwargs)


@api_view(['GET'])
def index(request):
    return response.Response({"status": "OK"})