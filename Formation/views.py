from rest_framework import viewsets
from .models import Formation
from .Serializers import *

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

class FormationSingupViewSet(viewsets.ModelViewSet):
    queryset = FormationSingup.objects.all()
    serializer_class = FormationSingupSerializer

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class ProblematiqueViewSet(viewsets.ModelViewSet):
    queryset = Problematique.objects.all()
    serializer_class = ProblematiqueSerializer