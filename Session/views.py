from django.contrib.auth import authenticate, login as dj_login, logout
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from Distributeur.models import Distributeur
from Produits.models import TypeProduit, Couleur, Mesure
from .models import *
from .Serializers import VilleSerializer, CustomUserSerializer
from django.contrib.auth.decorators import login_required


class LoginView(APIView):
    http_method_names = ['post', 'get']

    def post(self, request):
        print("post")
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
        print("get")
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

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



@login_required
def Utilisateurs(request):
    liste_users = CustomUser.objects.filter(
        Q(type="Agent")|
        Q(type='Admin')
    ).order_by('id').prefetch_related('user_permissions__content_type')

    for user in liste_users:
        user.permission_ids = ",".join(map(str, user.user_permissions.values_list('id', flat=True)))
        print(user.permission_ids)

    users_select = CustomUser.objects.filter(
        Q(type="Agent", is_active=True)|
        Q(type='Admin', is_active=True)
    ).order_by('id')
    #return render(request, "Utilisateur.html", {'liste_users': liste_users,'users_select': users_select})
    return render(request, "Pumal/Utilisateur.html", {'liste_users': liste_users,'users_select': users_select})


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

    return render(request, "homelanding.html", {
    })


@login_required
def custom_logout(request):

    logout(request)
    return redirect('login')