from django.contrib.auth.models import Permission
from rest_framework import serializers

from Session.Serializers import CustomUserSerializer
from .models import *

class DistributeurSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Distributeur
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        distributeur = Distributeur.objects.create(user=user, **validated_data)

        return distributeur

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user_serializer = CustomUserSerializer(instance.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class payeurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payeur
        fields = '__all__'