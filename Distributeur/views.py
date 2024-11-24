from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.exceptions import ValidationError

from Distributeur.Serializers import DistributeurSerializer, payeurSerializer
from Session.Serializers import CustomUserSerializer
from .models import *


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class DistributeurViewSet(viewsets.ModelViewSet):
    queryset = Distributeur.objects.all()
    serializer_class = DistributeurSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    """def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the current Distributeur instance

        # Extract user data from request
        user_data = request.data.get('user', {})

        # Update the user fields if provided
        if user_data:
            user_instance = instance.user  # Get the related user instance
            user_instance.username = user_data.get('username', user_instance.username)
            user_instance.email = user_data.get('email', user_instance.email)
            user_instance.first_name = user_data.get('first_name', user_instance.first_name)
            user_instance.last_name = user_data.get('last_name', user_instance.last_name)
            user_instance.telephone = user_data.get('telephone', user_instance.telephone)
            try:
                user_instance.responsable = user_data.get('responsable', user_instance.responsable)
            except Exception:
                pass
            user_instance.region = user_data.get('region', user_instance.region)
            user_instance.is_active = user_data.get('is_active', user_instance.is_active)
            user_instance.save()  # Save changes to user

        # Update the Distributeur fields
        for attr, value in request.data.items():
            if attr == 'user':  # Skip 'user' since it's handled separately
                continue
            if attr == 'ville':
                try:
                    instance.ville = Ville.objects.get(id=int(value))  # Ensure 'ville' is an integer
                except (ValueError, Ville.DoesNotExist):
                    raise ValidationError(f"Invalid value for 'ville'.")
            else:
                setattr(instance, attr, value)

        # Save the updated Distributeur instance
        instance.save()

        # Return the updated data
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)"""


class PayeurViewSet(viewsets.ModelViewSet):
    queryset = Payeur.objects.all()
    serializer_class = payeurSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['distributeur']


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


@login_required
def DistribView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id', flat=True))
    )

    if (10 in listmodules):

        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type=10).values_list('id', flat=True)
            )
        )

        dist_list = Distributeur.objects.all()
        ville_list = Ville.objects.all()

        users_select = CustomUser.objects.filter(
            Q(type="Agent", is_active=True) |
            Q(type='Admin', is_active=True)
        ).order_by('id')

        # return render(request, "Distributeur.html",
        return render(request, "Pumal/Distributeur.html",
                      {
                          'dist_list': dist_list,
                          'ville_list': ville_list,
                          'users_select': users_select,
                          'listeauth': listeauth,
                          "listmodules": listmodules
                      })
    else:
        return render(request,"access.html", {"listmodules": listmodules})


@login_required
def PayView(request):
    if(request.user.type == "Distributeur"):
        pass
    else:
        listmodules  = list(
            set(request.user.user_permissions.values_list('content_type_id', flat=True))
        )

        if (11 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type=11).values_list('id', flat=True)
                )
            )

            dist_list = Payeur.objects.filter(draft=False)
            ville_list = Ville.objects.all()

            users_select = Distributeur.objects.all().order_by('id')


            return render(request, "Pumal/Payeur.html",
                          {
                              'dist_list': dist_list,
                              'ville_list': ville_list,
                              'users_select': users_select,
                              'listeauth': listeauth,
                              "listmodules": listmodules
                          })
        else:
            return render(request,"access.html", {"listmodules": listmodules})



@login_required
def PayDiftView(request):
    if (request.user.type == "Distributeur"):
        listmodules = list(
            set(request.user.user_permissions.values_list('content_type_id', flat=True))
        )

        if (11 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type=11).values_list('id', flat=True)
                )
            )

            # Get filter parameters
            code = request.GET.get('code', '').strip()
            designation = request.GET.get('designation', '').strip()
            telephone = request.GET.get('telephone', '').strip()
            adresse = request.GET.get('adresse', '').strip()
            nif = request.GET.get('nif', '').strip()
            nis = request.GET.get('nis', '').strip()
            art = request.GET.get('art', '').strip()
            rc = request.GET.get('rc', '').strip()
            distributeur = request.GET.get('distributeur', '')
            ville = request.GET.get('ville', '')
            active = request.GET.get('active', '')


            dist_list = Payeur.objects.filter(distributeur__user = request.user)

            if code:
                dist_list = dist_list.filter(code__icontains=code)
            if designation:
                dist_list = dist_list.filter(designation__icontains=designation)
            if telephone:
                dist_list = dist_list.filter(telephone__icontains=telephone)
            if adresse:
                dist_list = dist_list.filter(adresse__icontains=adresse)
            if nif:
                dist_list = dist_list.filter(nif__icontains=nif)
            if nis:
                dist_list = dist_list.filter(nis__icontains=nis)
            if art:
                dist_list = dist_list.filter(art__icontains=art)
            if rc:
                dist_list = dist_list.filter(rc__icontains=rc)
            if distributeur:
                dist_list = dist_list.filter(distributeur_id=distributeur)
            if ville:
                dist_list = dist_list.filter(ville_id=ville)
            if active:
                dist_list = dist_list.filter(active=(active == 'true'))


            ville_list = Ville.objects.all()



            return render(request, "Dist/PayeurDraft.html",
                          {
                              'dist_list': dist_list,
                              'ville_list': ville_list,
                              'listeauth': listeauth,
                              "listmodules": listmodules
                          })
        else:
            return render(request,"access.html", {"listmodules": listmodules})

    else:
        listmodules  = list(
            set(request.user.user_permissions.values_list('content_type_id', flat=True))
        )

        if (11 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type = 11).values_list('id', flat=True)
                )
            )

            dist_list = Payeur.objects.filter(draft = True)
            ville_list = Ville.objects.all()

            users_select = Distributeur.objects.all().order_by('id')


            return render(request, "Pumal/PayeurDraft.html",
                          {
                              'dist_list': dist_list,
                              'ville_list': ville_list,
                              'users_select': users_select,
                              'listeauth': listeauth,
                              "listmodules": listmodules
                          })
        else:
            return render(request,"access.html", {"listmodules": listmodules})

