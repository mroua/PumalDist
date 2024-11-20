"""
URL configuration for PumaDist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Session.views import test2
from .router import router1
from django.conf.urls.static import static

from PumaDist import settings
from Produits.views import ProductList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include("Dashboard.urls")),
    path('', include("Session.urls")),
    path('distributeur/', include("Distributeur.urls")),
    path('produit/', include("Produits.urls")),
    path('commande/', include("Commande.urls")),
    path('encaissement/', include("Encaissement.urls")),
    path('formation/', include("Formation.urls")),
    path('api/products', ProductList.as_view()),


    path('api/', include(router1.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
