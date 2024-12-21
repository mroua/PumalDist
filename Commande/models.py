from django.db import models

# Create your models here.
from Distributeur.models import Distributeur, Payeur
from Produits.models import Produit
from Session.models import CustomUser

etatCMD=(
    ('Brouillon', 'Brouillon'),
    ('Reception', 'Receptions Et Enregistrement'),
    ('Traitement', 'Validation Et Traitement'),
    ('Preparation', 'Preparation'),
    ('En cours', "En Cours D'expedition"),
    ('Complete', 'Complete'),
    ('Annule', 'Annulé'),
)


class Dist_Commande(models.Model):
    id = models.AutoField(primary_key=True)
    #distributeur = models.ForeignKey(Distributeur, on_delete=models.CASCADE)#distributeur
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)#distributeur
    date_ajout = models.DateField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=etatCMD, default='Reception')
    total = models.FloatField(default=0)

class Dist_CommandeLines(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    commande = models.ForeignKey(Dist_Commande, related_name='commandesLines', on_delete=models.CASCADE)
    prixtotal = models.FloatField()
    prixunitaire = models.FloatField()
    complete = models.BooleanField(default=False)


class Dist_BonLivraison(models.Model):
    id = models.AutoField(primary_key=True)
    facture = models.CharField(max_length=255,null=True, blank=True)
    payeur = models.ForeignKey(Payeur, models.CASCADE, blank=True, null=True)
    date_ajout = models.DateField(auto_now_add=True)
    date_facturation = models.DateField(null=True, blank=True)
    date_echeance = models.DateField(null=True, blank=True)
    fc_file = models.FileField(upload_to="Factures", blank=True, null=True)
    bl_file = models.FileField(upload_to="BonLivraison", blank=True, null=True)
    commandes = models.ForeignKey(Dist_Commande, related_name='BLCMD', on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    validate = models.BooleanField(default=False)

class Dist_BonLivraisonLine(models.Model):
    id = models.AutoField(primary_key=True)
    bl = models.ForeignKey(Dist_BonLivraison, related_name='BonLivraison', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prixtotal = models.FloatField()
    prixunitaire = models.FloatField()



