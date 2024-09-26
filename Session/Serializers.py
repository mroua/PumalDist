from django.contrib.auth.models import Permission
from rest_framework import serializers
from .models import *

class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = '__all__'

class LocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localite
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    groups = serializers.CharField(required=False)
    user_permissions = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate_username(self, value):
        user_id = self.instance.id if self.instance else None
        if CustomUser.objects.filter(username=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        user_permissions_data = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if user_permissions_data:
            permissions = user_permissions_data.split(',') if isinstance(user_permissions_data, str) else user_permissions_data
            permission_objects = Permission.objects.filter(id__in=permissions)
            user.user_permissions.set(permission_objects)

        return user

    def update(self, instance, validated_data):
        user_permissions_data = validated_data.pop('user_permissions', None)

        print("here")

        for attr, value in validated_data.items():
            if attr == 'password' and value:
                instance.set_password(value)
            elif attr == 'username':
                if value != instance.username:
                    self.validate_username(value)
                instance.username = value
            else:
                setattr(instance, attr, value)
        instance.save()

        if user_permissions_data:
            permissions = user_permissions_data.split(',') if isinstance(user_permissions_data, str) else user_permissions_data
            permission_objects = Permission.objects.filter(id__in=permissions)
            instance.user_permissions.set(permission_objects)

        return instance



