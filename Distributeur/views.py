from django.contrib.auth import authenticate, login as dj_login
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

from Distributeur.Serializers import DistributeurSerializer, payeurSerializer
from .models import *


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class DistributeurViewSet(viewsets.ModelViewSet):
    queryset = Distributeur.objects.all()
    serializer_class = DistributeurSerializer


class PayeurViewSet(viewsets.ModelViewSet):
    queryset = Payeur.objects.all()
    serializer_class = payeurSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['distributeur']


@login_required
def DistribView(request):
    dist_list = Distributeur.objects.all()
    ville_list = Ville.objects.all()

    users_select = CustomUser.objects.filter(
        Q(type="Agent", is_active=True)|
        Q(type='Admin', is_active=True)
    ).order_by('id')

    return render(request, "Distributeur.html",
                  {
                      'dist_list': dist_list,
                      'ville_list': ville_list,
                      'users_select': users_select
                  })
@login_required
def PayView(request):
    dist_list = Payeur.objects.filter(draft = False)
    ville_list = Ville.objects.all()

    users_select = Distributeur.objects.all().order_by('id')

    print(users_select)

    return render(request, "Payeur.html",
                  {
                      'dist_list': dist_list,
                      'ville_list': ville_list,
                      'users_select': users_select
                  })