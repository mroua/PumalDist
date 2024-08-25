from django.contrib import admin

# Register your models here.

from .models import TypeProduit, Couleur, Mesure, Produit

admin.site.register(TypeProduit)
admin.site.register(Couleur)
admin.site.register(Mesure)
admin.site.register(Produit)
