from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.core import exceptions
from rest_framework_bulk.drf3.serializers import (
    BulkListSerializer,
    BulkSerializerMixin,
)
from djcore.djcore.groups.serializers import GroupSerializer

class UserSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    def get_user_permissions(self, user):
        return user.get_all_permissions()

    def get_username(self, user):
        return user.email

    class Meta:
        model = User
        exclude = ('password',)
        extra_kwargs = {
            'id': {'read_only': True}
        }

class UserLightSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'groups')

class UserCreateSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('password', 'id', 'first_name', 'last_name', 'email',
                  'last_login','is_staff','is_active','date_joined','groups','user_permissions',
                  )
        extra_kwargs = {
            'password': {'write_only': True},
            # 'last_login': {'read_only': True},
            # 'is_staff': {'read_only': True},
            # 'is_active': {'read_only': True},
            # 'date_joined': {'read_only': True},
            # 'groups': {'read_only': True},
            # 'user_permissions': {'read_only': True},
        }
        exclude = ()

    def create(self, validated_data):
        # del validated_data['password_confirmation']
        user = User(
            ** validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
            # raise serializers.ValidationError({'errors':errors})

        return super(UserCreateSerializer, self).validate(data)


class UserBulkSerializer(BulkSerializerMixin, UserSerializer):
    class Meta(object):
        model = User
        # only necessary in DRF3
        list_serializer_class = BulkListSerializer