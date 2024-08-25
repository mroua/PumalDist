from django.contrib.auth.models import AbstractUser
from django.db import models


Typeprofile = [
        ('Admin', 'Admin'),
        ('Distributeur', 'Distributeur'),
        ('Agent', 'Agent'),
        #('Distributeur', 'Distributeur'),
        #('Corporate', 'Corporate'),
    ]

Typeregion = [
        ('Est', 'Est'),
        ('Ouest', 'Ouest'),
        ('Centre', 'Centre'),
    ]

class Ville(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=80)
    region = models.CharField(max_length=6, choices=Typeregion, default='EST', blank=True, null=True)

    def __str__(self):
        return self.designation

class Localite(models.Model):
    id = models.AutoField(primary_key=True)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    designation = models.CharField(max_length=40)

    def __str__(self):
        return self.designation

    def villeact(self):
        return self.ville.designation

class CustomUser(AbstractUser):
    type = models.CharField(max_length=12, choices=Typeprofile, default='Agent')
    region = models.CharField(max_length=6, choices=Typeregion, default='EST', blank=True, null=True)
    telephone = models.CharField(max_length=80, blank=True)
    responsable = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="Profile/", null=True, blank=True)

    def __str__(self):
        return self.username

    def nom(self):
        return self.last_name+' '+self.first_name