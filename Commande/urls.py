from django.urls import path

from .views import CommandeView, BlivraisonView

urlpatterns = [
    path('', CommandeView, name='commande'),
    path('bl', BlivraisonView, name='bl'),

]
