from django.urls import path
from .views import DashView

urlpatterns = [
    path('', DashView, name='dashboard'),
]
