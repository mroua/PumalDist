from django.db.models import Sum
from rest_framework import serializers
from .models import Factures, Encaissement, Account, EncaissementFacture, Banque
from datetime import datetime, timedelta
from datetime import date

from django.utils import timezone



class BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'


class EncaissementFactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncaissementFacture
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if(instance.encaissement):
            if(not instance.encaissement.validation_depot): etat= "En circulaion"
            elif(not instance.encaissement.validation): etat= "En dépot"
            else: etat = "Validé"
            representation['encaissement_etat'] = etat

        return representation


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            # Add extra fields to the representation
            representation['payeur_designation'] = instance.payeur.designation
            representation['distributeur_designation'] = instance.payeur.distributeur.designation
            if(instance.type in ["Cheque", "Virement"]):
                representation['banque_designation'] = instance.banque.designation+" ("+ instance.banque.code +")"
            else:
                representation['banque_designation'] = 'Aucune'

        return representation

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            print(value)
            setattr(instance, attr, value)
            if(attr == "validation_depot"): instance.date_depot = date.today()
            if(attr == "validation"): instance.date_validation = date.today()
        instance.save()
        return instance

class FacturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factures
        fields = ['id', 'code', 'payeur', 'montant', 'date_ajout', 'date_echeance', 'complete', 'fc_file']


    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            # Add extra fields to the representation
            representation['payeur_designation'] = instance.payeur.designation
            representation['distributeur_designation'] = instance.payeur.distributeur.user.first_name+' '+instance.payeur.distributeur.user.last_name
            representation['montant_ttc'] = instance.montant_ttc
            listeencaissement = EncaissementFacture.objects.filter(facture=instance)
            serializer = EncaissementFactureSerializer(listeencaissement, many=True)
            serialized_data = serializer.data

            representation['listeencaissement'] = serialized_data

        return representation


    def create(self, validated_data):
        payeur = validated_data.get('payeur')
        try:
            if not validated_data.get('date_echeance') and payeur:
                days_to_add = payeur.distributeur.echeance_jour
                validated_data['date_echeance'] = (datetime.now() + timedelta(days=days_to_add)).date()
        except Exception as e:
            # Default to 15 days if there is an exception
            validated_data['date_echeance'] = (datetime.now() + timedelta(days=15)).date()

        # Create the Factures instance
        facture = super().create(validated_data)

        # Calculate and update montant_ttc
        facture.montant_ttc = facture.montant_ttc * 0.19 + facture.montant_ttc
        facture.save()  # Save the updated instance to the database

        return facture

class EncaissementSerializer(serializers.ModelSerializer):
    factures = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    numero = serializers.CharField(required=False)

    class Meta:
        model = Encaissement
        fields = [
            'id', 'montant', 'payeur', 'type', 'numero', 'banque',
            'date_depot', 'date_cheque', 'substitution', 'listefacturesub', 'factures'
        ]


    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            # Add extra fields to the representation
            representation['payeur_designation'] = instance.payeur.designation
            representation['distributeur_designation'] = instance.payeur.distributeur.user.first_name+' '+instance.payeur.distributeur.user.last_name
            if(instance.type in ["Cheque", "Virement"]):
                representation['banque_designation'] = instance.banque.designation+" ("+ instance.banque.code +")"
            else:
                representation['banque_designation'] = 'Aucune'

        return representation

    def create(self, validated_data):
        factures_ids = validated_data.pop('factures')

        # Check if the type is "Espece"
        if validated_data.get('type') == "Espece":
            validated_data['validation'] = True
            validated_data['validation_depot'] = True
            validated_data['date_validation'] = timezone.now().date()
            validated_data['date_depot'] = timezone.now().date()

        encaissement = Encaissement.objects.create(**validated_data)

        remaining_montant = encaissement.montant
        payeur = encaissement.payeur

        for facture_id in factures_ids:
            facture = Factures.objects.get(id=facture_id)
            facture_montant = facture.montant_ttc - (EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))['montant__sum'] or 0)

            if remaining_montant >= facture_montant:
                # Full amount applied to the facture
                encaissement_facture = EncaissementFacture(
                    facture=facture,
                    type='Encaissement',
                    encaissement=encaissement,
                    montant=facture_montant
                )
                encaissement_facture.save()
                remaining_montant -= facture_montant
            else:
                # Partially apply the remaining montant to the facture
                encaissement_facture = EncaissementFacture(
                    facture=facture,
                    type='Encaissement',
                    encaissement=encaissement,
                    montant=remaining_montant
                )
                encaissement_facture.save()
                remaining_montant = 0
                break

        # If there's remaining montant, use account funds
        if remaining_montant > 0:
            accounts = Account.objects.filter(payeur=payeur, montant__gt=0).order_by('date_ajout')
            for account in accounts:
                for facture_id in factures_ids:
                    facture = Factures.objects.get(id=facture_id)
                    facture_montant = facture.montant_ttc - (EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))['montant__sum'] or 0)

                    if account.montant >= facture_montant:
                        encaissement_facture = EncaissementFacture(
                            facture=facture,
                            type='Account',
                            account=account,
                            montant=facture_montant
                        )
                        encaissement_facture.save()
                        account.montant -= facture_montant
                        account.save()
                        remaining_montant = 0
                    else:
                        encaissement_facture = EncaissementFacture(
                            facture=facture,
                            type='Account',
                            account=account,
                            montant=account.montant
                        )
                        encaissement_facture.save()
                        remaining_montant -= account.montant
                        account.montant = 0
                        account.save()
                    if remaining_montant == 0:
                        break

        # If there's still remaining montant, create a new account
        if remaining_montant > 0:
            Account.objects.create(
                code=encaissement.code,
                payeur=encaissement.payeur,
                montant_init=remaining_montant,
                montant=remaining_montant,
                type=encaissement.type,
                numero=encaissement.numero,
                encaissement=encaissement
            )

        # Update the `complet` field based on whether the total montant_ttc is fully covered
        for facture_id in factures_ids:
            facture = Factures.objects.get(id=facture_id)
            total_encaissement = EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))['montant__sum'] or 0
            facture.complete = total_encaissement >= facture.montant_ttc
            facture.save()

        return encaissement
