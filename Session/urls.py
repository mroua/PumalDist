from django.urls import path
from .views import LoginView, Utilisateurs

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login'),
    path('users/', Utilisateurs, name='users'),
]
