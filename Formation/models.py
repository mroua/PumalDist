from django.db import models

# Create your models here.
from Distributeur.models import Distributeur

TypePRO=(
    ('Reclamation', 'Reclamation'),
    ('Intervention', 'Intervention'),
)

EtapePRO=(
    ('Reception', 'Reception'),
    ('En cours', 'En cours'),
    ('Validation', 'Validation'),
    ('Confirmation', 'Confirmation'),
)


class Formation(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=100)
    nbrplace = models.IntegerField()
    duree = models.IntegerField()
    tarif = models.FloatField()
    datedebut = models.DateField()
    dateajout = models.DateField(auto_now_add=True)


class FormationSingup(models.Model):
    id = models.AutoField(primary_key=True)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    distributeur = models.ForeignKey(Distributeur, on_delete=models.CASCADE)
    nbrelem = models.IntegerField()
    prixtotal = models.FloatField()
    dateajout = models.DateField(auto_now_add=True)

class Equipe(models.Model):
    id = models.AutoField(primary_key=True)
    formation = models.ForeignKey(FormationSingup, related_name='Equipeline', on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    dateajout = models.DateField(auto_now_add=True)


class Problematique(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30, choices=TypePRO, default='Reclamation')
    profile = models.ForeignKey(Distributeur, on_delete=models.CASCADE)#distributeur
    intitule = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    erreur = models.CharField(max_length=500)
    date_ajout = models.DateField()
    etat = models.CharField(max_length=30, default='Reception', choices=EtapePRO)

