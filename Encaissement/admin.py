from django.contrib import admin

from .models import Encaissement, Factures, EncaissementFacture, Banque, Account

admin.site.register(Encaissement)
admin.site.register(Factures)
admin.site.register(EncaissementFacture)
admin.site.register(Banque)
admin.site.register(Account)
