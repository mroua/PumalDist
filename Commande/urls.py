from django.urls import path

from .views import CommandeView, BlivraisonView, EtatViewChange

urlpatterns = [
    path('', CommandeView, name='commande'),
    path('etatview', EtatViewChange, name='etatview'),
    path('bl', BlivraisonView, name='bl'),

]
