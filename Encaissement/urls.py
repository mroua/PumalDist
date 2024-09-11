from django.urls import path

from .views import EncaissementView, FactureView, AccompteDist, get_factures, AccompteView, EncaissementDetailView

urlpatterns = [
    path('', EncaissementView, name='encaissement'),
    path('encaissementvalidate', EncaissementDetailView, name='encaissementvalidate'),
    path('accompte', AccompteView, name='accompte'),
    path('facture', FactureView, name='facture'),
    path('accomptetotal', AccompteDist, name='accomptetotal'),
    path('get-factures/<int:payeur_id>/', get_factures, name='get_factures'),
]
