from django.contrib import admin


from .models import Dist_Commande, Dist_BonLivraison, Dist_BonLivraisonLine, Dist_CommandeLines

admin.site.register(Dist_Commande)
admin.site.register(Dist_BonLivraison)
admin.site.register(Dist_BonLivraisonLine)
admin.site.register(Dist_CommandeLines)