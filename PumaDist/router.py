
from rest_framework import routers

from Session.views import ProfileViewSet
from Distributeur.views import DistributeurViewSet, PayeurViewSet
from Produits.views import ProduitViewSet
from Commande.views import Dist_CommandeLinesViewSet, Dist_CommandeViewSet, Dist_BonLivraisonViewSet, \
    Dist_BonLivraisonLineViewSet, Dist_CommandeDetailViewSet, \
    Dist_BonLivraisonDetailViewset, Dist_BonLivraisonNormalViewset

from Encaissement.views import BanqueViewSet, AccountViewSet, FacturesViewSet, EncaissementViewSet
from Formation.views import FormationViewSet, FormationSingupViewSet, EquipeViewSet, ProblematiqueViewSet

router1 = routers.DefaultRouter()

#Creance register Viewsets

router1.register('user', ProfileViewSet)
router1.register('distributeur', DistributeurViewSet)
router1.register('payeur', PayeurViewSet)
router1.register('produit', ProduitViewSet)


#router1.register('banque', BanqueViewSet)
router1.register('account', AccountViewSet)
router1.register('facture', FacturesViewSet)
router1.register('encaissement', EncaissementViewSet)


router1.register('commandelines', Dist_CommandeLinesViewSet)
"""router1.register('commande', Dist_CommandeViewSet)
router1.register('commandedetail', Dist_CommandeDetailViewSet)"""
router1.register('commande', Dist_CommandeViewSet, basename='commande')
router1.register('commandedetail', Dist_CommandeDetailViewSet, basename='commandedetail')
#router1.register('blivraison', Dist_BonLivraisonViewSet, basename='blivraison')
router1.register('blivraisonlines', Dist_BonLivraisonLineViewSet)
router1.register('blivraisondetail', Dist_BonLivraisonDetailViewset, basename='blivraisondetail')



router1.register('blivraison', Dist_BonLivraisonNormalViewset, basename='blivraison')



router1.register('formation', FormationViewSet, basename='formation')
router1.register('formationsingup', FormationSingupViewSet, basename='formationsingup')
router1.register('problematique', ProblematiqueViewSet, basename='problematique')