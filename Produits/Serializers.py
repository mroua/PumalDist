from django.contrib.auth.models import Permission
from rest_framework import serializers

from Session.Serializers import CustomUserSerializer
from .models import *


class ProduitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produit
        fields = '__all__'