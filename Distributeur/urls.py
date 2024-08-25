from django.urls import path

from .views import DistribView, PayView

urlpatterns = [
    path('', DistribView, name='distributeur'),
    path('payeur', PayView, name='payeur'),
]
