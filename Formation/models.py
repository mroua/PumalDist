from django.db import models
from django.db.models import Sum

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


    def place_restante(self):
        total_nbrelem = FormationSingup.objects.filter(formation=self).aggregate(total=Sum('nbrelem'))['total'] or 0
        return max(self.nbrplace - total_nbrelem, 0)


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
    intitule = models.CharField(max_length=300)
    message = models.TextField()
    date_ajout = models.DateField(auto_now_add=True)
    etat = models.CharField(max_length=30, default='Reception', choices=EtapePRO)

