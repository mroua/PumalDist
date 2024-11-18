from dateutil.utils import today
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from .models import Formation
from .Serializers import *

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class FormationSingupViewSet(viewsets.ModelViewSet):
    queryset = FormationSingup.objects.all()
    serializer_class = FormationSingupSerializer

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class ProblematiqueViewSet(viewsets.ModelViewSet):
    queryset = Problematique.objects.all()
    serializer_class = ProblematiqueSerializer



@login_required
def FormView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id', flat=True))
    )

    if(26 in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type = 24).values_list('id', flat=True)
            )
        )

        formations = Formation.objects.all()

        if(request.user.type == "Distributeur"):
            return render(request, "Dist/Formations.html", {
                "formations": formations,
                "listeauth": listeauth,
                "listmodules": listmodules,
            })
        else:
            return render(request, "Pumal/Formations.html", {
                "formations": formations,
                "listeauth": listeauth,
                "listmodules": listmodules,
            })

    else:
        return render(request,"access.html", {"listmodules": listmodules})



@login_required
def ProbView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id', flat=True))
    )

    if (26 in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type = 25).values_list('id', flat=True)
            )
        )

        problematique = Problematique.objects.filter(etat__in=['Reception', 'En cours', 'Validation'])

        return render(request, "Pumal/problematique.html", {
            "problematique": problematique,
            "listeauth": listeauth,
            "listmodules": listmodules,
        })
    else:
        return render(request,"access.html", {"listmodules": listmodules})

