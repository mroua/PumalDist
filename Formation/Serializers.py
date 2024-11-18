from datetime import timedelta

from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import *



class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user = self.context.get('user')

        representation["datefin"] = instance.datedebut + timedelta(days=instance.duree)
        try:
            representation['placerestante'] = instance.nbrplace - FormationSingup.objects.filter(formation=instance).aggregate(total=Sum('nbrelem'))['total'] or 0
        except Exception:
            representation['placerestante'] = 0

        if(user.type=="Distributeur"):
            formation_signups = FormationSingup.objects.filter(formation=instance, distributeur__user=user)
        else:
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
    #nbrelem = serializers.IntegerField(required=False)
    #prixtotal = serializers.FloatField(required=False)

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
        formation = validated_data.get('formation')

        FormationSingup.objects.filter(formation=formation, distributeur=validated_data.get('distributeur')).delete()

        nbrtotal = len(equipes_data)
        if(nbrtotal > 0 and formation.place_restante() > nbrtotal):
            formation_signup = FormationSingup.objects.create(**validated_data)
            formation_signup.nbrelem = nbrtotal
            formation_signup.prixtotal = nbrtotal * formation_signup.formation.tarif
            formation_signup.save()

            for equipe_data in equipes_data:
                newelem = Equipe.objects.create(formation=formation_signup, **equipe_data)
                newelem.save()

            return formation_signup
        pass

    def update(self, instance, validated_data):
        equipes_data = validated_data.pop('Equipeline', [])
        formation = validated_data.get('formation', instance.formation)
        nbrtotal = len(equipes_data)
        instance.Equipeline.all().delete()

        if(len(equipes_data) == 0):
            instance.delete()
            return Response("Done", status=status.HTTP_200_OK)
        else:
            if formation and nbrtotal < formation.place_restante():
                available_places = formation.nbrplace
                if nbrtotal > available_places:
                    raise serializers.ValidationError({
                        'nbrelem': "Le nombre d'inscriptons dépasse les places disponible."
                    })

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if equipes_data:
                for equipe_data in equipes_data:
                    Equipe.objects.create(formation=instance, **equipe_data)

            return instance