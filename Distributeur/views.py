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

    def update(self, request, *args, **kwargs):
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
        return Response(serializer.data, status=status.HTTP_200_OK)


class PayeurViewSet(viewsets.ModelViewSet):
    queryset = Payeur.objects.all()
    serializer_class = payeurSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['distributeur']


@login_required
def DistribView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id', flat=True))
    )

    if (9 in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type=9).values_list('id', flat=True)
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

        if (10 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type=10).values_list('id', flat=True)
                )
            )

            dist_list = Payeur.objects.filter(draft=False)
            ville_list = Ville.objects.all()

            users_select = Distributeur.objects.all().order_by('id')

            print(users_select)

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

        if (10 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type=10).values_list('id', flat=True)
                )
            )

            dist_list = Payeur.objects.filter(distributeur__user = request.user)
            ville_list = Ville.objects.all()

            users_select = Distributeur.objects.all().order_by('id')

            print(users_select)

            return render(request, "Dist/PayeurDraft.html",
                          {
                              'dist_list': dist_list,
                              'ville_list': ville_list,
                              'users_select': users_select,
                              'listeauth': listeauth,
                              "listmodules": listmodules
                          })
        else:
            return render(request,"access.html", {"listmodules": listmodules})

    else:
        listmodules  = list(
            set(request.user.user_permissions.values_list('content_type_id', flat=True))
        )

        if (10 in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type = 10).values_list('id', flat=True)
                )
            )

            dist_list = Payeur.objects.filter(draft = True)
            ville_list = Ville.objects.all()

            users_select = Distributeur.objects.all().order_by('id')

            print(users_select)

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

