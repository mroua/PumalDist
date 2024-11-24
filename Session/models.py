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
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, null=True, blank=True)
    region = models.CharField(max_length=6, choices=Typeregion, default='EST', blank=True, null=True)
    telephone = models.CharField(max_length=80, blank=True)
    responsable = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="Profile/", null=True, blank=True)

    def __str__(self):
        return self.username

    def nom(self):
        return self.last_name+' '+self.first_name

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