from django.contrib.auth.models import Permission
from rest_framework import serializers

from PumaDist.addhistory import addhistory
from Session.Serializers import CustomUserSerializer
from .models import *


class ProduitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produit
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['typemesure'] = instance.mesure.type

        return representation


    def create(self, validated_data):

        prod = Produit.objects.create(**validated_data)

        serializer = ProduitSerializer(prod)
        addhistory({}, serializer.data, 15, 1, user=self.context.get('user'))

        return prod

    def update(self, instance, validated_data):
        oldvalue = ProduitSerializer(instance).data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = ProduitSerializer(instance)
        addhistory(oldvalue, serializer.data, 15, 2, user=self.context.get('user'))

        return instance