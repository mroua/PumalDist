from django.db import models

# Create your models here.
from Session.models import Ville, CustomUser


class Distributeur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=True)
    code = models.CharField(max_length=100, default='0000000', blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    nis = models.CharField(max_length=20, blank=True, null=True)
    art = models.CharField(max_length=20, blank=True, null=True)
    rc = models.CharField(max_length=20, blank=True, null=True)
    plafonnement = models.FloatField(default=1000000, blank=True, null=True)
    bloquer = models.BooleanField(default=False)

    echeance_jour = models.IntegerField(default=0, blank=True, null=True)

    ristourn_a = models.FloatField(default=0)
    ristourn_na = models.FloatField(default=0)
    objectif_a = models.FloatField(default=0)
    objectif_m = models.FloatField(default=0)

    def __str__(self):
        return self.designation


class Payeur(models.Model):
    id = models.AutoField(primary_key=True)
    distributeur = models.ForeignKey(Distributeur, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, default='0000000')
    designation = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    nif = models.CharField(max_length=20, null=True, blank=True)
    nis = models.CharField(max_length=20, null=True, blank=True)
    art = models.CharField(max_length=20, null=True, blank=True)
    rc = models.CharField(max_length=20, null=True, blank=True)


    nif_file = models.FileField(upload_to="PayeurData", blank=True, null=True)
    nis_file = models.FileField(upload_to="PayeurData", blank=True, null=True)
    art_file = models.FileField(upload_to="PayeurData", blank=True, null=True)
    rc_file = models.FileField(upload_to="PayeurData", blank=True, null=True)

    date_ajout = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.designation