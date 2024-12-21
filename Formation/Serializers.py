from datetime import timedelta

from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.response import Response

from PumaDist.addhistory import addhistory
from .models import *


"""
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
        try:
            if(user.type=="Distributeur"):
                formation_signups = FormationSingup.objects.filter(formation=instance, distributeur__user=user)
            else:
                formation_signups = FormationSingup.objects.filter(formation=instance)
        except Exception:
            pass

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

    def create(self, validated_data):

        form = Formation.objects.create(**validated_data)

        serializer = FormationSerializer(form)
        addhistory({}, serializer.data, 'formation', 1, user=self.context.get('user'))

        return form

    def update(self, instance, validated_data):
        oldvalue = FormationSerializer(instance).data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = FormationSerializer(instance)
        addhistory(oldvalue, serializer.data, 'formation', 2, user=self.context.get('user'))

        return instance
"""

class ImagesFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesFormation
        fields = ['id', 'image']

class ImagesProblematiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesProblematique
        fields = ['id', 'image']

class FormationSerializer(serializers.ModelSerializer):
    images = ImagesFormationSerializer(many=True, write_only=True, required=False)
    images_urls = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Formation
        fields = [
            'id', 'titre', 'nbrplace', 'duree', 'tarif', 'datedebut', 'dateajout',
            'text', 'lieu', 'est', 'ouest', 'centre', 'place_restante', 'images', 'images_urls'
        ]
        read_only_fields = ['dateajout', 'place_restante']

    def get_images_urls(self, obj):
        """Get URLs of related images."""
        return [img.image.url for img in obj.imagesformation_set.all()]

    def create(self, validated_data):
        # Extract and process `images` data
        images_data = self.context['request'].FILES.getlist('images')  # Retrieve file list from request
        formation = Formation.objects.create(**validated_data)
        for image_file in images_data:
            ImagesFormation.objects.create(formation=formation, image=image_file)  # Save image file
        return formation

    def update(self, instance, validated_data):
        # Extract and process `images` data
        images_data = self.context['request'].FILES.getlist('images')  # Retrieve file list from request

        # Update formation fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Clear existing images and add new ones
        if images_data:
            instance.imagesformation_set.all().delete()
            for image_file in images_data:
                ImagesFormation.objects.create(formation=instance, image=image_file)  # Save image file

        return instance

        
class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'
        extra_kwargs = {
            'formation': {'required': False}  # Make 'formation' optional
        }


class ProblematiqueSerializer(serializers.ModelSerializer):
    images = ImagesProblematiqueSerializer(many=True, write_only=True, required=False)
    images_urls = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Problematique
        fields = '__all__'

    def get_images_urls(self, obj):
        """Get URLs of related images."""
        return [img.image.url for img in obj.imagesformation_set.all()]

    def create(self, validated_data):

        form = Problematique.objects.create(**validated_data)

        serializer = ProblematiqueSerializer(form)
        addhistory({}, serializer.data, 'problematique', 1, user=self.context.get('user'))

        return form

    def update(self, instance, validated_data):
        oldvalue = ProblematiqueSerializer(instance).data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = ProblematiqueSerializer(instance)
        addhistory(oldvalue, serializer.data, 'problematique', 2, user=self.context.get('user'))

        return instance


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

        serializer = FormationSingupSerializer(formation_signup)
        addhistory({}, serializer.data, 'formationsingup', 1, user=self.context.get('user'))
        return formation_signup



    def update(self, instance, validated_data):
        equipes_data = validated_data.pop('Equipeline', [])
        formation = validated_data.get('formation', instance.formation)
        nbrtotal = len(equipes_data)
        oldvalue = FormationSerializer(instance).data
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

            serializer = FormationSerializer(instance)
            addhistory(oldvalue, serializer.data, 'formationsingup', 2, user=self.context.get('user'))
            return instance