from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from Distributeur.models import Distributeur
from Produits.models import TypeProduit, Couleur, Mesure
from .models import *
from .Serializers import VilleSerializer, CustomUserSerializer, ChangePasswordSerializer
from django.contrib.auth.decorators import login_required


class LoginView(APIView):
    http_method_names = ['post', 'get']

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        try:
            user = authenticate(username=username, password=password)
            if user:
                dj_login(request, user)
                return Response({
                    'user': CustomUserSerializer(user).data,
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/users/')  # Redirect to the dashboard or another page
        return render(request, "Login.html")

class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer


    """filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['country', 'designation']"""

class LocaliteViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Votre mot de passe a été modifié avec succée."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context

    def update(self, request, *args, **kwargs):
        partial = True  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def Utilisateurs(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    print(listmodules)

    listville= Ville.objects.all()

    if('customuser' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type__model = "customuser").values_list('codename', flat=True)
            )
        )

        if(request.user.type=="Distributeur"):
            liste_users = CustomUser.objects.filter(
                responsable=request.user
            ).order_by('id').prefetch_related('user_permissions__content_type')

            ville = request.GET.get('ville', None)
            region = request.GET.get('region', None)
            active = request.GET.get('is_active')
            if(active == "true"):
                is_active = True
            else:
                is_active = False

            if (ville):
                liste_users = liste_users.filter(ville=int(ville))
            if (region):
                liste_users = liste_users.filter(region=region)
            if (active):
                liste_users = liste_users.filter(is_active=is_active)

            #return render(request, "Utilisateur.html", {'liste_users': liste_users,'users_select': users_select})
            return render(request, "Dist/Utilisateur.html", {
                'liste_users': liste_users,
                'listeauth': listeauth,
                "listmodules": listmodules,
                "listville": listville
            })
        else:
            liste_users = CustomUser.objects.filter(
                Q(type="Agent") |
                Q(type="Admin Régional") |
                Q(type="Admin Wilaya") |
                Q(type="Résponsable distributeur") |
                Q(type='Admin')
            ).order_by('id').prefetch_related('user_permissions__content_type')

            type = request.GET.get('type', None)
            ville = request.GET.get('ville', None)
            region = request.GET.get('region', None)
            active = request.GET.get('is_active')
            if (active == "true"):
                is_active = True
            else:
                is_active = False

            if type:
                liste_users = liste_users.filter(type=type)
            if (ville):
                liste_users = liste_users.filter(ville=int(ville))
            if (region):
                liste_users = liste_users.filter(region=region)
            if (active):
                liste_users = liste_users.filter(is_active=is_active)

            for user in liste_users:
                user.permission_ids = ",".join(map(str, user.user_permissions.values_list('codename', flat=True)))
                # user.permission_ids = list(user.user_permissions.values_list('codename', flat=True))

            users_select = CustomUser.objects.filter(
                Q(type="Agent", is_active=True) |
                Q(type='Admin', is_active=True)
            ).order_by('id')
            # return render(request, "Utilisateur.html", {'liste_users': liste_users,'users_select': users_select})
            return render(request, "Pumal/Utilisateur.html", {
                'liste_users': liste_users,
                'users_select': users_select,
                'listeauth': listeauth,
                "listmodules": listmodules,
                "listville": listville
            })
    else:
        return render(request,"access.html", {"listmodules": listmodules})


def test2(request):
    user = CustomUser.objects.get(id=1)
    user.set_password("123456")
    user.save()
    return HttpResponse("Done")

@login_required
def test(request):

    user = CustomUser.objects.all()
    for elem in user:
        elem.set_password('123456')
        elem.save()



    liste_type = TypeProduit.objects.all()
    liste_couleur = Couleur.objects.all()
    liste_mesure = Mesure.objects.all()
    liste_distributeur = Distributeur.objects.all()

    lise_prod = []

    # Initialize the base SQL query
    query = """SELECT id, code, distributeur, ville, date_ajout, total, etat, total_blivraison, taxedtotal, taxedtotal_blivraison FROM cmdlist WHERE 1=1"""
    params = []  # This will hold the parameters for the SQL query

    filters = []  # This will hold the filter conditions

    # Extract filter values from request parameters
    code = request.GET.get('code')
    date_ajout_min = request.GET.get('date_ajout_min')
    date_ajout_max = request.GET.get('date_ajout_max')
    etat = request.GET.get('etat')

    # Add filters to the query based on the provided values
    if code:
        filters.append("code = %s")
        params.append(code)
    if date_ajout_min:
        filters.append("date_ajout >= %s")
        params.append(date_ajout_min)
    if date_ajout_max:
        filters.append("date_ajout <= %s")
        params.append(date_ajout_max)
    if etat:
        filters.append("etat = %s")
        params.append(etat)

    # Append the filters to the query if there are any
    if filters:
        query += " AND " + " AND ".join(filters)

    with connection.cursor() as cursor:
        # Execute the SQL query with parameters
        cursor.execute(query, params)

        rows = cursor.fetchall()

        for row in rows:
            lise_prod.append({
                "id": row[0],
                "code": row[1],
                "distributeur": row[2],
                "ville": row[3],
                "date_ajout": row[4],
                "total": row[5],
                "etat": row[6],
                "total_blivraison": row[7],
                "taxedtotal": row[8],
                "taxedtotal_blivraison": row[9],
            })

    return render(request, "Html.html", {
        'liste_type': liste_type,
        'liste_couleur': liste_couleur,
        'liste_mesure': liste_mesure,
        'liste_distributeur': liste_distributeur,
        'liste_cmd': lise_prod
    })



@login_required
def LandingPage(request):
    #listeauth = list(request.user.user_permissions.values_list('codename', flat=True))
    listeauth = list(
        set(request.user.user_permissions.values_list('content_type__model', flat=True))
    )

    return render(request, "homelanding.html", {
        'listeauth': listeauth
    })


@login_required
def custom_logout(request):

    logout(request)
    return redirect('login')

@login_required
def ProfilePage(request):
    if(request.user.type == "Distributeur"):
        listeville = Ville.objects.all()
        return render(request, 'Dist/Profile.html', {
            'listeville': listeville
        })
    else:
        listmodules  = list(
            set(request.user.user_permissions.values_list('content_type_id', flat=True))
        )

        return render(request, 'Pumal/Profile.html', {
            'listmodules': listmodules
        })



class Historynotif(APIView):
    #permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        listcmd = []

        query = """SELECT id, elem_id, user_representative, action_flag, old_msg, new_msg, content_type, "user", vue, viewer_id, 
        creation_date, url, msg, urllink FROM historyview where vue=false and viewer_id="""+str(request.user.id) + """ limit 10"""

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                listcmd.append({
                    "id": row[0],
                    "url": row[13],
                    "msg": row[12],
                    "action": row[3],
                    "id_elem": row[1]
                })


        return JsonResponse(listcmd, safe=False)

@login_required
def HistoryDatadisp(request):
    print("here")
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    if(request.user.type == "Admin"):
        print("ici")
        print(request.user.id)
        listhistory = History.objects.filter(user=request.user.id)


        return render(request, "Pumal/Historique.html", {
            "listmodules": listmodules,
            "listhistory": listhistory,
        })
    else:
        print("la")
        listhistory = History.objects.filter(user=request.user.id)

        return render(request, "Pumal/Historique.html", {
            "listmodules": listmodules,
            "listhistory": listhistory,
        })
        #return render(request,"access.html", {"listmodules": listmodules})