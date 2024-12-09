from django.db.models import Sum
from rest_framework import serializers

from PumaDist.addhistory import addhistory
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

        if (instance.encaissement):
            if (not instance.encaissement.validation_depot):
                etat = "En circulaion"
            elif (not instance.encaissement.validation):
                etat = "En dépot"
            else:
                etat = "Validé"
            representation['encaissement_etat'] = etat

        return representation


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)
        try:
            # Add extra fields to the representation
            representation['payeur_designation'] = instance.payeur.designation
            representation['distributeur_designation'] = instance.payeur.distributeur.designation
            if (instance.type in ["Cheque", "Virement"]):
                representation['banque_designation'] = instance.banque.designation + " (" + instance.banque.code + ")"
            else:
                representation['banque_designation'] = 'Aucune'
        except Exception:
            pass
        return representation

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():

            setattr(instance, attr, value)
            if (attr == "validation_depot"): instance.date_depot = date.today()
            if (attr == "validation"): instance.date_validation = date.today()
        instance.save()


        serializer = AccountSerializer(instance)

        addhistory({}, serializer.data, 'account', 2, user=self.context.get('user'))
        return instance


class FacturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factures
        fields = ['id', 'code', 'payeur', 'montant', 'date_ajout', 'date_echeance', 'complete', 'fc_file']

    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)
        #if self.context['request'].method == 'GET':
            # Add extra fields to the representation
        try:
            representation['payeur_designation'] = instance.payeur.designation
            representation[
                    'distributeur_nom'] = instance.payeur.distributeur.user.first_name + ' ' + instance.payeur.distributeur.user.last_name
            representation['distributeur_designation'] = instance.payeur.distributeur.designation
            representation['montant_ttc'] = instance.montant_ttc
            listeencaissement = EncaissementFacture.objects.filter(facture=instance)
            serializer = EncaissementFactureSerializer(listeencaissement, many=True)
            serialized_data = serializer.data

            representation['listeencaissement'] = serialized_data
        except Exception:
            pass

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
        facture.montant_ttc = facture.montant * 0.19 + facture.montant
        facture.save()  # Save the updated instance to the database


        serializer = FacturesSerializer(facture)

        addhistory({}, serializer.data, "factures", 1, user=self.context.get('user'))

        return facture


class EncaissementSerializer(serializers.ModelSerializer):
    """esponse
    Text: {"payeur": ["This field is required."],
           "date_cheque": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."],
           "factures": ["This field is required."]}"""

    factures = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    numero = serializers.CharField(required=False)

    class Meta:
        model = Encaissement
        fields = [
            'id', 'montant', 'payeur', 'type', 'numero', 'banque', 'code', 'date_validation', 'date_ajout',
            'validation', 'validation_depot',
            'date_depot', 'date_cheque', 'substitution', 'listefacturesub', 'factures'
        ]
        extra_kwargs = {
            "payeur": {"required": False},
            "date_cheque": {"required": False},
            "factures": {"required": False},
        }

    def to_representation(self, instance):
        # Modify the representation to include the extra fields only on GET requests
        representation = super().to_representation(instance)


        #if self.context['request'].method == 'GET':
            # Add extra fields to the representation
        try:
            representation['payeur_designation'] = instance.payeur.designation
            representation['distributeur_designation'] = instance.payeur.distributeur.designation
                # representation['distributeur_designation'] = instance.payeur.distributeur.user.first_name+' '+instance.payeur.distributeur.user.last_name
            if (instance.type in ["Cheque", "Virement"]):
                representation['banque_designation'] = instance.banque.designation + " (" + instance.banque.code + ")"
            else:
                representation['banque_designation'] = 'Aucune'
        except Exception:
            pass

        return representation

    def create(self, validated_data):
        factures_ids = validated_data.pop('factures')

        # Check if the type is "Espece"
        if validated_data.get('type') == "Espece":
            validated_data['validation'] = True
            validated_data['validation_depot'] = True
            validated_data['date_validation'] = timezone.now().date()
            validated_data['date_depot'] = timezone.now().date()

        if (validated_data['montant'] != 0):
            encaissement = Encaissement.objects.create(**validated_data)

            remaining_montant = encaissement.montant
            payeur = encaissement.payeur

            for facture_id in factures_ids:
                facture = Factures.objects.get(id=facture_id)
                facture_montant = facture.montant_ttc - (
                            EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))[
                                'montant__sum'] or 0)

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
            retour = encaissement
        else:
            remaining_montant = 0
            payeur = validated_data['payeur']


            # If there's remaining montant, use account funds
        if remaining_montant >= 0:
            accounts = Account.objects.filter(payeur=payeur, montant__gt=0).order_by('date_ajout')
            for account in accounts:
                for facture_id in factures_ids:
                    facture = Factures.objects.get(id=facture_id)
                    facture_montant = facture.montant_ttc - (
                                EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))[
                                    'montant__sum'] or 0)

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



        # Update the `complet` field based on whether the total montant_ttc is fully covered
        for facture_id in factures_ids:
            facture = Factures.objects.get(id=facture_id)
            total_encaissement = EncaissementFacture.objects.filter(facture=facture).aggregate(Sum('montant'))[
                                     'montant__sum'] or 0
            facture.complete = total_encaissement >= facture.montant_ttc
            facture.save()


        serializer = EncaissementSerializer(encaissement)

        addhistory({}, serializer.data, 'encaissement', 1, user=self.context.get('user'))

        return "done"


    """def update(self, instance, validated_data):
        print("holzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        print(validated_data)
        for attr, value in validated_data.items():
            print(attr)
            setattr(instance, attr, value)
            if(attr == "validation_depot"): instance.date_depot = date.today()
            if(attr == "validation"): instance.date_validation = date.today()
        instance.save()
        listeaccount = Account.objects.filter(encaissement=instance)
        for elem in listeaccount:
            elem.validation = instance.validation
            elem.validation_depot = instance.validation_depot

            elem.save()

        return instance
"""
