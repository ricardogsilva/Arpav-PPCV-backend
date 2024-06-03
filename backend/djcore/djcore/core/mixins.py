from rest_framework.response import Response
from django.core.serializers import serialize
from rest_framework.decorators import action

class OptionListModelMixin(object):

    option_list_fields = ('name','id',)
    option_list_order = None

    def get_queryset(self):
        qs = super(OptionListModelMixin, self).get_queryset()

        q = self.request.query_params.get('q', None)
        if q != None and q != "":
            qs = qs.filter(name__icontains=q)

        ids = self.request.query_params.get('ids', None)
        if ids is list and ids:
            qs = qs.filter(pk__in=ids)

        return qs

    """
    Option-list a queryset.
    """
    @action(methods=['get'], detail=False)
    def option_list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset()

        if request.query_params.get('order') is not None:
            order = request.query_params.get('order').split(',')
        elif self.option_list_order is not None:
            order = self.option_list_order
        else:
            order = self.option_list_fields

        results = queryset.values(*self.option_list_fields).order_by(*order)
        data = {
            'results': results
        }
        return Response(data)
