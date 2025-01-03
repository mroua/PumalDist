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


    """def create(self, request, *args, **kwargs):
        print('coucou')

        print(request.data)


        return Response("coucou")"""

class FormationSingupViewSet(viewsets.ModelViewSet):
    queryset = FormationSingup.objects.all()
    serializer_class = FormationSingupSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context

class ProblematiqueViewSet(viewsets.ModelViewSet):
    queryset = Problematique.objects.all()
    serializer_class = ProblematiqueSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context



@login_required
def FormView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    if('problematique' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type__model='formation').values_list('codename', flat=True)
            )
        )

        formations = Formation.objects.all()

        if(request.user.type in ["Distributeur", "Employé"]):

            date_debut = request.GET.get('date_debut', None)
            date_fin = request.GET.get('date_fin', None)


            if date_debut:
                formations = formations.filter(datedebut__gte=date_debut)

            if date_fin:
                # Calculate the end date dynamically as `datedebut + duree`
                formations = formations.filter(datedebut__lte=date_fin, datedebut__gte=('datedebut') + timedelta(days=('duree')))

            return render(request, "Dist/Formations.html", {
                "formations": formations,
                "listeauth": listeauth,
                "listmodules": listmodules,
            })
        else:

            date_debut = request.GET.get('date_debut', None)
            date_fin = request.GET.get('date_fin', None)


            if date_debut:
                formations = formations.filter(datedebut__gte=date_debut)

            if date_fin:
                # Calculate the end date dynamically as `datedebut + duree`
                formations = formations.filter(datedebut__lte=date_fin, datedebut__gte=F('datedebut') + timedelta(days=F('duree')))

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
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )


    if ('formation' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type__model='Problematique').values_list('codename', flat=True)
            )
        )
        if (request.user.type in ["Distributeur", "Employé"]):
            problematique = Problematique.objects.filter(etat__in=['Reception', 'En cours', 'Validation'], profile=request.user)

            return render(request, "Dist/problematique.html", {
                "problematique": problematique,
                "listeauth": listeauth,
                "listmodules": listmodules,
            })
        else:

            problematique = Problematique.objects.filter(etat__in=['Reception', 'En cours', 'Validation'])

            return render(request, "Pumal/problematique.html", {
                "problematique": problematique,
                "listeauth": listeauth,
                "listmodules": listmodules,
            })
    else:
        return render(request,"access.html", {"listmodules": listmodules})

