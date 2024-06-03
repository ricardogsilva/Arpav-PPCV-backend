from rest_framework import generics, viewsets
from .models import User
# from rest_framework.permissions import IsAdminUser
from djcore.djcore.core.permissions import DjangoAdminOrObjectPermission
from .serializers import  UserSerializer, UserCreateSerializer, UserBulkSerializer, UserLightSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkDestroyAPIView
from django.db.models import Q
from django.contrib.auth.models import Group
# from djcore.djcore.core.views import OptionListAPIView
from rest_framework.decorators import action
from djcore.djcore.core.mixins import OptionListModelMixin
from rest_framework.response import Response

class UserViewSet(generics.RetrieveUpdateDestroyAPIView,viewsets.GenericViewSet):
    """
    Creates, Updates, and retrives User accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DjangoAdminOrObjectPermission,)

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        response = super(UserViewSet, self).update(request, *args, **kwargs)
        if response.data.get('id') and request.data.get('groups'):
            user = User.objects.get(pk=response.data.get('id'))
            groups = Group.objects.filter(pk__in=list( map(lambda x: x.get('id'), request.data.get('groups') )))
            user.groups = groups
            user.save()
        return response


# class UserOptionListView(OptionListAPIView,viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     permission_classes = (DjangoAdminOrObjectPermission,)

class UserListView(generics.ListCreateAPIView,OptionListModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # permission_classes = ()
    permission_classes = (DjangoAdminOrObjectPermission,)
    option_list_fields = ('id','first_name','last_name')
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        response = super(UserListView, self).create(request, *args, **kwargs)
        if response.data.get('id') and request.data.get('groups'):
            user = User.objects.get(pk=response.data.get('id'))
            groups = Group.objects.filter(pk__in=list( map(lambda x: x.get('id'), request.data.get('groups') )))
            user.groups = groups
            user.save()
        return response

    """
    Option-list a queryset.
    """
    @action(methods=['get'], detail=False)
    def option_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('order') is not None:
            order = request.query_params.get('order').split(',')
        elif self.option_list_order is not None:
            order = self.option_list_order
        else:
            order = self.option_list_fields

        serialized_class = UserLightSerializer(queryset.order_by(*order).all(), many=True)

        data = {
            'results': serialized_class.data
        }
        return Response(data)


    def get_queryset(self):
        qs = super(UserListView, self).get_queryset()

        qs = qs.exclude(username='AnonymousUser').exclude(is_superuser=True)

        q = self.request.query_params.get('q', None)
        if q != None and q != "":
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q))

        return qs



class UserBulkView(BulkDestroyAPIView, ModelViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserBulkSerializer
    ids = []
    permission_classes = (DjangoAdminOrObjectPermission,)

    def filter_queryset(self,qs):
        return qs.filter(pk__in=self.ids).all()

    def delete(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            self.ids = ids.split(',')
        return self.bulk_destroy(request, *args, **kwargs)

    def allow_bulk_destroy(self, qs, filtered):
        return qs is not filtered
