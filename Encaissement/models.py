from django.db import models

# Create your models here.
from Distributeur.models import Payeur

typeencaissement = (
    ('Cheque', 'Cheque'),
    ('Virement', 'Virement'),
    ('Espece', 'Espece'),
)

typeencaissementfacture = (
    ('Encaissement', 'Encaissement'),
    ('Account', 'Account'),
)


class Banque(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class Factures(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    payeur = models.ForeignKey(Payeur, models.CASCADE)
    montant = models.FloatField(default=0)
    date_ajout= models.DateTimeField(auto_now=True)
    date_echeance = models.DateField(blank=True , null=True)
    complete = models.BooleanField(default=False)
    fc_file = models.FileField(blank=True , null=True)

    def __str__(self):
        return self.payeur.distributeur.designation+'/ '+ self.payeur.designation

    @property
    def restant(self):
        # Calculate the sum of all validated encaissements for this facture
        encaissements_sum = \
        self.Facture_encaissement.filter(encaissement__validation=True).aggregate(total=models.Sum('montant'))[
            'total'] or 0

        # Calculate and return the remaining amount
        return self.montant - encaissements_sum


class Encaissement(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    montant = models.FloatField(default=0)
    payeur = models.ForeignKey(Payeur, models.CASCADE)
    type = models.CharField(max_length=20, choices=typeencaissement)
    numero = models.CharField(max_length=50)
    date_validation = models.DateField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    validation = models.BooleanField(default=False)

    validation_depot = models.BooleanField(default=False)
    banque = models.ForeignKey(Banque, null=True, blank=True, on_delete=models.CASCADE)
    date_depot = models.DateField(null=True, blank=True)
    date_cheque = models.DateField(null=True, blank=True)

    substitution = models.BooleanField(default=False)
    listefacturesub = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.montant)


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    payeur = models.ForeignKey(Payeur, models.CASCADE)
    montant_init = models.FloatField(default=0)
    montant = models.FloatField(default=0)
    type = models.CharField(max_length=20, choices=typeencaissement)
    numero = models.CharField(max_length=50)
    date_validation = models.DateField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    validation = models.BooleanField(default=False)

    encaissement = models.ForeignKey(Encaissement, models.CASCADE, null=True, blank=True)


    validation_depot = models.BooleanField(default=False)
    banque = models.ForeignKey(Banque, null=True, blank=True, on_delete=models.CASCADE)
    date_depot = models.DateField(null=True, blank=True)
    date_cheque = models.DateField(null=True, blank=True)

    substitution = models.BooleanField(default=False)
    payeursubstite = models.ForeignKey(Payeur, models.CASCADE, null=True, blank=True, related_name="payeursubstite")



class EncaissementFacture(models.Model):
    id = models.AutoField(primary_key=True)
    facture = models.ForeignKey(Factures, models.CASCADE,related_name='Facture_encaissement')
    type= models.CharField(max_length=20, choices=typeencaissementfacture, default='Encaissement')
    encaissement = models.ForeignKey(Encaissement, models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(Account, models.CASCADE, null=True, blank=True)
    montant = models.FloatField(default=0)


    def __str__(self):
        return str(self.montant)


