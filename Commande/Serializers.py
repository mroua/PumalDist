import base64
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models import Sum
from rest_framework import serializers
from .models import Dist_Commande, Dist_CommandeLines, Produit, Dist_BonLivraison, Dist_BonLivraisonLine


class Dist_CommandeLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dist_CommandeLines
        fields = ['id', 'produit', 'quantite', 'prixtotal', 'prixunitaire', 'complete']
        read_only_fields = ['prixtotal', 'prixunitaire']


class Dist_CommandeSerializer(serializers.ModelSerializer):
    commandesLines = Dist_CommandeLinesSerializer(many=True)

    class Meta:
        model = Dist_Commande
        fields = ['id', 'distributeur', 'date_ajout', 'etat', 'total', 'commandesLines']
        read_only_fields = ['total', 'date_ajout']

    def create(self, validated_data):
        commandes_lines_data = validated_data.pop('commandesLines')
        commande = Dist_Commande.objects.create(**validated_data)
        total = 0

        for line_data in commandes_lines_data:
            produit = line_data['produit']
            prixunitaire = produit.prix_publique
            prixtotal = prixunitaire * line_data['quantite']
            line_data['prixunitaire'] = prixunitaire
            line_data['prixtotal'] = prixtotal
            total += prixtotal
            Dist_CommandeLines.objects.create(commande=commande, **line_data)

        commande.total = total
        commande.save()

        return commande

    def update(self, instance, validated_data):
        commandes_lines_data = validated_data.pop('commandesLines')
        instance.distributeur = validated_data.get('distributeur', instance.distributeur)
        instance.etat = validated_data.get('etat', instance.etat)
        instance.save()

        total = 0

        for line_data in commandes_lines_data:
            line_id = line_data.get('id')
            if line_id:
                line = Dist_CommandeLines.objects.get(id=line_id, commande=instance)
                line.quantite = line_data.get('quantite', line.quantite)
                line.complete = line_data.get('complete', line.complete)
                line.prixunitaire = line.produit.prix_publique
                line.prixtotal = line.prixunitaire * line.quantite
                line.save()
            else:
                produit = line_data['produit']
                prixunitaire = produit.prix_publique
                prixtotal = prixunitaire * line_data['quantite']
                line_data['prixunitaire'] = prixunitaire
                line_data['prixtotal'] = prixtotal
                Dist_CommandeLines.objects.create(commande=instance, **line_data)
            total += line_data['prixtotal']

        instance.total = total
        instance.save()

        return instance


class Dist_CommandeLinesSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Dist_CommandeLines
        fields = ['id', 'produit', 'quantite', 'prixtotal', 'prixunitaire', 'complete']
        read_only_fields = ['prixtotal', 'prixunitaire']
        depth= 2

class Dist_CommandeSerializerDetail(serializers.ModelSerializer):
    commandesLines = Dist_CommandeLinesSerializerDetail(many=True)

    class Meta:
        model = Dist_Commande
        fields = ['id', 'distributeur', 'date_ajout', 'etat', 'total', 'commandesLines']
        read_only_fields = ['total', 'date_ajout']
        depth= 2

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        """bon_livraison_qs = Dist_BonLivraison.objects.filter(commandes=instance)
        bon_livraison_serialized = Dist_BonLivraisonSerializer(bon_livraison_qs, many=True).data
        representation['bonLivraison'] = bon_livraison_serialized"""

        for elem in representation['commandesLines']:
            bon_livraisons = Dist_BonLivraison.objects.filter(commandes=instance)
            restantprod = Dist_BonLivraisonLine.objects.filter(bl__in=bon_livraisons, produit__id=elem['produit']['id'])

            totals = restantprod.aggregate(
                total_quantite=Sum('quantite'),
                total_prixtotal=Sum('prixtotal')
            )

            elem["total_quantite"] = totals['total_quantite'] if totals['total_quantite'] else 0
            elem["total_prixtotal"] = totals['total_prixtotal'] if totals['total_prixtotal'] else 0

        return representation

    def create(self, validated_data):
        commandes_lines_data = validated_data.pop('commandesLines')
        commande = Dist_Commande.objects.create(**validated_data)
        total = 0

        for line_data in commandes_lines_data:
            produit = line_data['produit']
            prixunitaire = produit.prix_publique
            prixtotal = prixunitaire * line_data['quantite']
            line_data['prixunitaire'] = prixunitaire
            line_data['prixtotal'] = prixtotal
            total += prixtotal
            Dist_CommandeLines.objects.create(commande=commande, **line_data)

        commande.total = total
        commande.save()

        return commande

    def update(self, instance, validated_data):
        commandes_lines_data = validated_data.pop('commandesLines')
        instance.distributeur = validated_data.get('distributeur', instance.distributeur)
        instance.etat = validated_data.get('etat', instance.etat)
        instance.save()

        total = 0

        for line_data in commandes_lines_data:
            line_id = line_data.get('id')
            if line_id:
                line = Dist_CommandeLines.objects.get(id=line_id, commande=instance)
                line.quantite = line_data.get('quantite', line.quantite)
                line.complete = line_data.get('complete', line.complete)
                line.prixunitaire = line.produit.prix_publique
                line.prixtotal = line.prixunitaire * line.quantite
                line.save()
            else:
                produit = line_data['produit']
                prixunitaire = produit.prix_publique
                prixtotal = prixunitaire * line_data['quantite']
                line_data['prixunitaire'] = prixunitaire
                line_data['prixtotal'] = prixtotal
                Dist_CommandeLines.objects.create(commande=instance, **line_data)
            total += line_data['prixtotal']

        instance.total = total
        instance.save()

        return instance


class Dist_BonLivraisonLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dist_BonLivraisonLine
        fields = ['id', 'produit', 'quantite', 'prixtotal', 'prixunitaire']
        read_only_fields = ['prixtotal', 'prixunitaire']

class Dist_BonLivraisonSerializer(serializers.ModelSerializer):
    BonLivraison = Dist_BonLivraisonLineSerializer(many=True, required=False)
    fc_file = serializers.CharField(write_only=True, required=False, allow_null=True)
    bl_file = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Dist_BonLivraison
        fields = ['id', 'facture', 'date_ajout', 'date_facturation', 'date_echeance', 'fc_file', 'bl_file', 'commandes',
                  'BonLivraison', 'total']
        read_only_fields = ['date_ajout', 'total']

    def create(self, validated_data):
        fc_file_base64 = validated_data.pop('fc_file', None)
        bl_file_base64 = validated_data.pop('bl_file', None)
        bon_livraison_lines_data = validated_data.pop('BonLivraison')
        bon_livraison = Dist_BonLivraison.objects.create(**validated_data)
        total = 0

        if fc_file_base64:
            fc_file = self._base64_to_file(fc_file_base64)
            bon_livraison.fc_file.save('fc_file', fc_file)
        if bl_file_base64:
            bl_file = self._base64_to_file(bl_file_base64)
            bon_livraison.bl_file.save('bl_file', bl_file)

        for line_data in bon_livraison_lines_data:
            produit = line_data.get('produit')
            if produit is None:
                raise serializers.ValidationError("Produit is required.")
            prixunitaire = produit.prix_publique
            quantite = line_data.get('quantite')
            if quantite is None:
                raise serializers.ValidationError("Quantite is required.")
            prixtotal = prixunitaire * quantite
            line_data['prixunitaire'] = prixunitaire
            line_data['prixtotal'] = prixtotal
            total += prixtotal
            Dist_BonLivraisonLine.objects.create(bl=bon_livraison, **line_data)

        bon_livraison.total = total
        bon_livraison.save()

        return bon_livraison

    def update(self, instance, validated_data):
        fc_file_base64 = validated_data.pop('fc_file', None)
        bl_file_base64 = validated_data.pop('bl_file', None)
        bon_livraison_lines_data = validated_data.pop('BonLivraison', None)

        instance.facture = validated_data.get('facture', instance.facture)
        instance.date_facturation = validated_data.get('date_facturation', instance.date_facturation)
        instance.date_echeance = validated_data.get('date_echeance', instance.date_echeance)

        print("**********************************")
        print(fc_file_base64[:100])
        print(type(fc_file_base64))
        print("**********************************")

        if fc_file_base64:
            fc_file = self._base64_to_file(fc_file_base64)
            print("///////////")
            print(fc_file)
            print("///////////")
            instance.fc_file.save('fc_file', fc_file)
        if bl_file_base64:
            bl_file = self._base64_to_file(bl_file_base64)
            instance.bl_file.save('bl_file', bl_file)

        instance.commandes = validated_data.get('commandes', instance.commandes)
        instance.save()

        total = 0

        if(bon_livraison_lines_data):
            for line_data in bon_livraison_lines_data:
                line_id = line_data.get('id')
                if line_id:
                    line = Dist_BonLivraisonLine.objects.get(id=line_id, bl=instance)
                    line.quantite = line_data.get('quantite', line.quantite)
                    line.prixunitaire = line.produit.prix_publique
                    line.prixtotal = line.prixunitaire * line.quantite
                    line.save()
                else:
                    produit = line_data['produit']
                    prixunitaire = produit.prix_publique
                    quantite = line_data.get('quantite')
                    if quantite is None:
                        raise serializers.ValidationError("Quantite is required.")
                    prixtotal = prixunitaire * quantite
                    line_data['prixunitaire'] = prixunitaire
                    line_data['prixtotal'] = prixtotal
                    Dist_BonLivraisonLine.objects.create(bl=instance, **line_data)
                total += line_data['prixtotal']

            instance.total = total
            instance.save()

        return instance

    def _base64_to_file(self, base64_string):
        try:
            # Check if the base64 string contains the expected delimiter
            if ';base64,' not in base64_string:
                raise ValueError("Invalid base64 string format.")

            # Split the base64 string into format and data parts
            format, base64_data = base64_string.split(';base64,')
            extension = format.split('/')[-1]
            if not extension:
                raise ValueError("Could not determine file extension.")

            # Decode the base64 string into binary data
            data = base64.b64decode(base64_data)

            # Generate a filename with the correct extension
            file_name = f"uploaded_file.{extension}"

            # Create a ContentFile with the binary data
            content_file = ContentFile(data, name=file_name)

            # Optional: Log file details
            print("content_file:", content_file)
            print("File Name:", content_file.name)
            print("File Size:", len(data), "bytes")
            print("File Data (first 100 bytes):", data[:100])

            return content_file

        except Exception as e:
            print(f"Error converting base64 string to file: {e}")
            return None


class Dist_BonLivraisonLineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dist_BonLivraisonLine
        fields = ['id', 'produit', 'quantite', 'prixtotal', 'prixunitaire']
        read_only_fields = ['prixtotal', 'prixunitaire']
        depth= 2

class Dist_BonLivraisonDetailSerializer(serializers.ModelSerializer):
    BonLivraison = Dist_BonLivraisonLineDetailSerializer(many=True, required=False)
    fc_file = serializers.CharField(write_only=True, required=False, allow_null=True)
    bl_file = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Dist_BonLivraison
        fields = ['id', 'facture', 'date_ajout', 'date_facturation', 'date_echeance', 'fc_file', 'bl_file', 'commandes',
                  'BonLivraison', 'total']
        read_only_fields = ['date_ajout', 'total']
        depth= 2


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if(instance.fc_file):
            representation['fc_file'] = instance.fc_file.url
        else: representation['fc_file'] = None
        if(instance.bl_file):
            representation['bl_file'] = instance.bl_file.url
        else: representation['bl_file'] = None


        return representation




