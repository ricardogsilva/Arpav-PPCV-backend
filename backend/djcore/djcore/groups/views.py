from django.contrib.auth.models import Group
from djcore.djcore.core.mixins import OptionListModelMixin
from djcore.djcore.groups.serializers import GroupSerializer
from rest_framework import generics, viewsets
from djcore.djcore.core.permissions import DjangoAdminOrObjectPermission


class GroupListView(generics.ListAPIView,OptionListModelMixin,viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (DjangoAdminOrObjectPermission,)
