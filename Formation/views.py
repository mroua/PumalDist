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

        print(listeauth)

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
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )


    if ('formation' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type__model='formation').values_list('codename', flat=True)
            )
        )
        if (request.user.type=="Distributeur"):
            problematique = Problematique.objects.filter(etat__in=['Reception', 'En cours', 'Validation'], profile__user=request.user)

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

