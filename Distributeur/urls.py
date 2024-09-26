from django.urls import path

from .views import DistribView, PayView, PayDiftView

urlpatterns = [
    path('', DistribView, name='distributeur'),
    path('payeur', PayView, name='payeur'),
    path('payeurdraft', PayDiftView, name='payeurdraft'),
]
