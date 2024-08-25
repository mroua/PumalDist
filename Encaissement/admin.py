from django.contrib import admin

from .models import Encaissement, Factures, EncaissementFacture, Banque

admin.site.register(Encaissement)
admin.site.register(Factures)
admin.site.register(EncaissementFacture)
admin.site.register(Banque)
