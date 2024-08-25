from rest_framework import serializers
from .models import Factures, Encaissement, Account, EncaissementFacture, Banque
from datetime import datetime, timedelta


class BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class FacturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factures
        fields = ['id', 'code', 'payeur', 'montant', 'date_ajout', 'date_echeance', 'complete', 'fc_file']

    def create(self, validated_data):
        payeur = validated_data.get('payeur')
        if not validated_data.get('date_echeance') and payeur:

            days_to_add = payeur.distributeur.echeance_jour
            validated_data['date_echeance'] = datetime.now() + timedelta(days=days_to_add)
        return super().create(validated_data)


class EncaissementSerializer(serializers.ModelSerializer):
    factures = serializers.ListField(write_only=True)

    class Meta:
        model = Encaissement
        fields = ['id', 'code', 'montant', 'payeur', 'type', 'numero', 'date_validation', 'date_ajout', 'validation', 'validation_depot', 'banque', 'date_depot', 'date_cheque', 'substitution', 'listefacturesub', 'factures']

    def create(self, validated_data):
        factures_data = validated_data.pop('factures')
        encaissement = Encaissement.objects.create(**validated_data)

        remaining_montant = encaissement.montant
        payeur = encaissement.payeur

        # Apply encaissement amount to each facture
        for facture_data in factures_data:
            facture = Factures.objects.get(id=facture_data['id'])
            facture_montant = facture_data['montant']

            if remaining_montant >= facture.montant:
                encaissement_facture = EncaissementFacture(
                    facture=facture,
                    type='Encaissement',
                    encaissement=encaissement,
                    montant=facture.montant
                )
                encaissement_facture.save()
                facture.complete = True
                facture.save()
                remaining_montant -= facture.montant
            else:
                encaissement_facture = EncaissementFacture(
                    facture=facture,
                    type='Encaissement',
                    encaissement=encaissement,
                    montant=remaining_montant
                )
                encaissement_facture.save()
                facture.montant -= remaining_montant
                facture.save()
                remaining_montant = 0
                break

        # Use account funds if encaissement funds are exhausted
        if remaining_montant == 0:
            accounts = Account.objects.filter(payeur=payeur, montant__gt=0).order_by('date_ajout')
            for account in accounts:
                for facture_data in factures_data:
                    facture = Factures.objects.get(id=facture_data['id'])
                    facture_montant = facture_data['montant']

                    if account.montant >= facture.montant:
                        encaissement_facture = EncaissementFacture(
                            facture=facture,
                            type='Account',
                            account=account,
                            montant=facture.montant
                        )
                        encaissement_facture.save()
                        facture.complete = True
                        facture.save()
                        account.montant -= facture.montant
                        account.save()
                        facture_montant = 0
                    else:
                        encaissement_facture = EncaissementFacture(
                            facture=facture,
                            type='Account',
                            account=account,
                            montant=account.montant
                        )
                        encaissement_facture.save()
                        facture.montant -= account.montant
                        facture.save()
                        account.montant = 0
                        account.save()

        # If there's still remaining encaissement amount, create a new account
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

        return encaissement