from django.contrib.auth.models import AbstractUser
from django.db import models


Typeprofile = [
        ('Admin', 'Admin'),
        ('Agent', 'Agent'),
        ('Admin Régional', 'Admin Régional'),
        ('Admin Wilaya', 'Admin Wilaya'),
        ('Résponsable distributeur', 'Résponsable distributeur'),
        ('Distributeur', 'Distributeur'),
        ('Employé', 'Employé'),
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
    type = models.CharField(max_length=32, choices=Typeprofile, default='Agent')
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, null=True, blank=True)
    region = models.CharField(max_length=6, choices=Typeregion, default='EST', blank=True, null=True)
    telephone = models.CharField(max_length=80, blank=True)
    responsable = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="Profile/", null=True, blank=True)

    def __str__(self):
        return self.username

    def nom(self):
        return self.last_name+' '+self.first_name

    def designation(self):
        print(self.type)
        if(self.type == 'Distributeur'):
            distdesignation = self.distributeur_set.first().designation#Distributeur.objects.get(user=self).designation
        elif(self.type == 'Employé'):
            distdesignation = self.responsable.distributeur_set.first().designation#Distributeur.objects.get(user=self).designation
        else:
            distdesignation = ""
        return distdesignation

class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    titre = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)


class ImagesPromotion(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="Promotions", blank=True, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    elem_id = models.IntegerField()
    user_representative = models.CharField(max_length=200)
    action_flag = models.IntegerField(default=0)
    old_msg = models.TextField(default={})
    new_msg = models.TextField(default={})
    content_type = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    vue = models.BooleanField(default=False)
    viewer_id = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200)



class UserURLHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)