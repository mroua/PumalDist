from django.urls import path

from .views import LoginView, Utilisateurs, test, LandingPage, custom_logout, ProfilePage, ChangePasswordView, HistoryDatadisp, Promo

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('password/', ChangePasswordView.as_view(), name='password'),
    path('login', LoginView.as_view(), name='login'),
    path('landing', LandingPage, name='landing'),
    path('users/', Utilisateurs, name='users'),
    path('test/', test, name='test'),
    path('profile/', ProfilePage, name='ProfilePage'),
    path('promotion/', Promo, name='promotion'),
    path('hisdisp/', HistoryDatadisp, name='hisdisp'),
    path('logout/', custom_logout, name='logout'),
]
