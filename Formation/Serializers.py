from datetime import timedelta

from django.db.models import Sum
from rest_framework import serializers
from .models import *



class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["datefin"] = instance.datedebut + timedelta(days=instance.duree)
        representation['placerestante'] = instance.nbrplace - FormationSingup.objects.filter(formation=instance).aggregate(total=Sum('nbrelem'))['total'] or 0

        formation_signups = FormationSingup.objects.filter(formation=instance)
        representation['groups'] = []

        for signup in formation_signups:
            equipes = Equipe.objects.filter(
                formation=signup)  # Adjust this filter to match the correct relationship
            equipes_data = EquipeSerializer(equipes, many=True).data

            representation['groups'].append({
                'id': signup.id,
                'distributeur': signup.distributeur.id,
                'distributeurname': signup.distributeur.designation,
                'nbrelem': signup.nbrelem,
                'prixtotal': signup.prixtotal,
                'dateajout': signup.dateajout,
                'Equipeline': equipes_data  # Add related Equipe data here
            })

        return representation


class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'
        extra_kwargs = {
            'formation': {'required': False}  # Make 'formation' optional
        }


class ProblematiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problematique
        fields = '__all__'


class FormationSingupSerializer(serializers.ModelSerializer):
    Equipeline = EquipeSerializer(many=True)

    class Meta:
        model = FormationSingup
        fields = '__all__'

    def validate(self, data):
        formation = data.get('formation')
        nbrelem = data.get('nbrelem')

        # Check if the number of requested elements exceeds the available places
        if formation and nbrelem is not None:
            available_places = formation.nbrplace
            if nbrelem > available_places:
                raise serializers.ValidationError({
                    'nbrelem': 'The number of elements exceeds the available places in the formation.'
                })

        return data

    def create(self, validated_data):
        equipes_data = validated_data.pop('Equipeline', [])
        formation_signup = FormationSingup.objects.create(**validated_data)

        for equipe_data in equipes_data:
            Equipe.objects.create(formation=formation_signup, **equipe_data)

        return formation_signup

    def update(self, instance, validated_data):
        equipes_data = validated_data.pop('Equipeline', [])
        formation = validated_data.get('formation', instance.formation)
        nbrelem = validated_data.get('nbrelem', instance.nbrelem)

        # Check if the number of requested elements exceeds the available places
        if formation and nbrelem is not None:
            available_places = formation.nbrplace
            if nbrelem > available_places:
                raise serializers.ValidationError({
                    'nbrelem': 'The number of elements exceeds the available places in the formation.'
                })

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if equipes_data:
            instance.Equipeline.all().delete()  # Clear previous data
            for equipe_data in equipes_data:
                Equipe.objects.create(formation=instance, **equipe_data)

        return instance