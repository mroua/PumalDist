from django.urls import path

from .views import ProduitView

urlpatterns = [
    path('', ProduitView, name='produit'),
]
