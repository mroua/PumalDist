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
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation
    def create(self, validated_data):
        # Pop user_permissions from the validated data
        user_permissions_data = validated_data.pop('user_permissions', None)
        print(user_permissions_data)

        # Create the user instance
        user = CustomUser.objects.create(**validated_data)

        # Set user permissions if provided
        if user_permissions_data:
            # Split the string into a list if passed as a comma-separated string
            permissions = user_permissions_data.split(',') if isinstance(user_permissions_data,
                                                                         str) else user_permissions_data
            permission_objects = Permission.objects.filter(id__in=permissions)
            user.user_permissions.set(permission_objects)

        return user

    def update(self, instance, validated_data):
        # Pop user_permissions from the validated data
        user_permissions_data = validated_data.pop('user_permissions', None)

        # Update the user instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Set user permissions if provided
        if user_permissions_data:
            # Split the string into a list if passed as a comma-separated string
            permissions = user_permissions_data.split(',') if isinstance(user_permissions_data,
                                                                         str) else user_permissions_data
            permission_objects = Permission.objects.filter(id__in=permissions)
            instance.user_permissions.set(permission_objects)

        return instance