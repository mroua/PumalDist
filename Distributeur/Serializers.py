from django.contrib.auth.models import Permission
from rest_framework import serializers

from PumaDist.addhistory import addhistory
from Session.Serializers import CustomUserSerializer
from .models import *

class DistributeurSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Distributeur
        fields = (
            'user', 'code', 'designation', 'ville', 'adresse', 'nif', 'nis', 'art', 'rc', 'plafonnement', 'bloquer',
            'echeance_jour', 'ristourn_a', 'ristourn_na', 'objectif_a', 'objectif_m'
        )
        extra_kwargs = {
            'ville': {'required': False}
        }



    def create(self, validated_data):
        user_data = validated_data.pop('user')
        responsable = user_data.pop('responsable')
        ville = user_data.pop('ville')

        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.responsable = responsable
        user.ville = ville
        user.save()

        distributeur = Distributeur.objects.create(user=user, ville=ville, **validated_data)

        payeur = Payeur.objects.create(
            distributeur=distributeur,
            code=distributeur.code,
            designation=distributeur.designation,
            ville=ville,  # Ensure ville is handled correctly here
            telephone=distributeur.user.telephone,
            adresse=distributeur.adresse,
            nif=distributeur.nif,
            nis=distributeur.nis,
            art=distributeur.art,
            rc=distributeur.rc
        )
        payeur.save()

        serializer = DistributeurSerializer(distributeur, context={'depth': 2})
        addhistory({}, serializer.data, 'distributeur', 1, user=self.context.get('user'))

        return distributeur

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        oldvalue = DistributeurSerializer(instance, context={'depth': 2}).data
        ville = user_data.pop('ville')
        #print(ville)

        if user_data:
            responsable = user_data.pop('responsable')
            user_serializer = CustomUserSerializer(instance.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            instance.user.responsable = responsable
            instance.user.ville = ville
            instance.user.save()


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = DistributeurSerializer(instance)
        addhistory(oldvalue, serializer.data, 'distributeur', 2, user=self.context.get('user'))

        return instance



class payeurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payeur
        fields = '__all__'

    def create(self, validated_data):

        payeur = Payeur.objects.create(**validated_data)

        serializer = payeurSerializer(payeur)
        addhistory({}, serializer.data, 'payeur', 1, user=self.context.get('user'))

        return payeur

    def update(self, instance, validated_data):
        oldvalue = payeurSerializer(instance).data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = payeurSerializer(instance)
        addhistory(oldvalue, serializer.data, 'payeur', 2, user=self.context.get('user'))

        return instance