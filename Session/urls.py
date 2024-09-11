from django.urls import path
from .views import LoginView, Utilisateurs, test, LandingPage

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login'),
    path('landing', LandingPage, name='landing'),
    path('users/', Utilisateurs, name='users'),
    path('test/', test, name='test'),
]
