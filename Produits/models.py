from django.db import models

# Create your models here.


Typepotentiel = [
    ('Unité', 'Unité'),
    ('Sac', 'Sac'),
]


class TypeProduit(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.designation

class Couleur(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.designation


class Mesure(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=12, choices=Typepotentiel, default='Unité')
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.designation


class Produit(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=255)
    reference = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(TypeProduit, on_delete=models.CASCADE)
    mesure = models.ForeignKey(Mesure, on_delete=models.CASCADE)
    couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Produit/", null=True, blank=True)
    prix_publique = models.FloatField(default=0)
    prix_gros = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.designation