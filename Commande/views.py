import requests
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from rest_framework import viewsets, status
# Create your views here.
from Distributeur.models import Distributeur, Payeur
from Produits.models import TypeProduit, Couleur, Mesure
from Session.models import Ville, CustomUser
from .Serializers import Dist_CommandeLinesSerializer, Dist_CommandeSerializer, Dist_BonLivraisonSerializer, \
    Dist_BonLivraisonLineSerializer, Dist_CommandeSerializerDetail, Dist_BonLivraisonDetailSerializer, \
    Dist_BonLivraisonNormalSerializer
from .models import Dist_CommandeLines, Dist_Commande, Dist_BonLivraison, Dist_BonLivraisonLine
from rest_framework.views import APIView
from django.db import connection
from django.contrib.auth.decorators import login_required

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Dist_CommandeLinesSerializer
# Dist_CommandeSerializer

class Dist_CommandeLinesViewSet(viewsets.ModelViewSet):
    queryset = Dist_CommandeLines.objects.all()
    serializer_class = Dist_CommandeLinesSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_CommandeViewSet(viewsets.ModelViewSet):
    queryset = Dist_Commande.objects.all()
    serializer_class = Dist_CommandeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_CommandeDetailViewSet(viewsets.ModelViewSet):
    queryset = Dist_Commande.objects.all()
    serializer_class = Dist_CommandeSerializerDetail

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_BonLivraisonViewSet(viewsets.ModelViewSet):
    queryset = Dist_BonLivraison.objects.all()
    serializer_class = Dist_BonLivraisonSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['commandes']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_BonLivraisonLineViewSet(viewsets.ModelViewSet):
    queryset = Dist_BonLivraisonLine.objects.all()
    serializer_class = Dist_BonLivraisonLineSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_BonLivraisonDetailViewset(viewsets.ModelViewSet):
    queryset = Dist_BonLivraison.objects.all()
    serializer_class = Dist_BonLivraisonDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class Dist_BonLivraisonNormalViewset(viewsets.ModelViewSet):
    queryset = Dist_BonLivraison.objects.all()
    serializer_class = Dist_BonLivraisonNormalSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


@login_required
def CommandeView(request):
    listmodules = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    if ('dist_commande' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(Q(user=request.user, content_type__model='dist_bonlivraison') |
                                          Q(user=request.user, content_type__model='dist_commande')).values_list(
                    'codename', flat=True)
            )
        )

        liste_type = TypeProduit.objects.all()
        liste_couleur = Couleur.objects.all()
        liste_mesure = Mesure.objects.all()
        liste_distributeur = CustomUser.objects.filter(type__in=["Distributeur", "Employé"], is_active=True)

        lise_prod = []
        if (request.user.type in ["Distributeur", "Employé"]):
            dist = Distributeur.objects.get(user=request.user)
            liste_distributeur = [Distributeur.objects.get(user=request.user)]
            query = """SELECT id, code, distributeur, ville, date_ajout, total, etat, total_blivraison, taxedtotal, taxedtotal_blivraison 
            FROM cmdlist WHERE user_id = """ + str(request.user.id)
            params = []  # This will hold the parameters for the SQL query

            filters = []  # This will hold the filter conditions

            # Extract filter values from request parameters
            code = request.GET.get('code')
            date_ajout_min = request.GET.get('date_ajout_min')
            date_ajout_max = request.GET.get('date_ajout_max')
            etat = request.GET.get('etat', None)

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
                print('ici')
                filters.append("etat = %s")
                params.append(etat)

            # Append the filters to the query if there are any
            if filters:
                query += " AND " + " AND ".join(filters)

            with connection.cursor() as cursor:
                print(query, params)
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

            liste_ville = Ville.objects.all()

            # return render(request, "Commande.html", {
            return render(request, "Dist/Commande.html", {
                'liste_type': liste_type,
                'liste_couleur': liste_couleur,
                'liste_mesure': liste_mesure,
                'liste_distributeur': liste_distributeur,
                'liste_cmd': lise_prod,
                'listeauth': listeauth,
                'liste_ville': liste_ville
            })
        else:
            query = """SELECT id, code, distributeur, ville, date_ajout, total, etat, total_blivraison, taxedtotal, 
            taxedtotal_blivraison FROM cmdlist WHERE 1=1"""


            params = []  # This will hold the parameters for the SQL query
            filters = []  # This will hold the filter conditions

            # Extract filter values from request parameters
            code = request.GET.get('code')
            date_ajout_min = request.GET.get('date_ajout_min')
            date_ajout_max = request.GET.get('date_ajout_max')
            distributeur = request.GET.get('distributeur', None)
            ville = request.GET.get('ville', None)
            etat = request.GET.get('etat', None)

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

            # Default behavior: Exclude `etat = 'brouillons'` unless it belongs to the logged-in user
            if not etat:  # Apply the default filter only if no specific `etat` is provided
                filters.append("(etat <> 'Brouillon' OR distributeur = %s)")
                params.append(request.user.id)

            # Append the filters to the query if there are any
            if filters:
                query += " AND " + " AND ".join(filters)

            # Execute the query
            with connection.cursor() as cursor:
                print(query)
                print(params)
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Process the result
                lise_prod = [
                    {
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
                    }
                    for row in rows
                ]

            # Fetch additional data
            liste_ville = Ville.objects.all()

            # Render the template with the data
            return render(request, "Pumal/Commande.html", {
                'liste_type': liste_type,
                'liste_couleur': liste_couleur,
                'liste_mesure': liste_mesure,
                'liste_distributeur': liste_distributeur,
                'liste_cmd': lise_prod,
                'listeauth': listeauth,
                'listmodules': listmodules,
                'liste_ville': liste_ville,
            })

    else:
        return render(request, "access.html", {"listmodules": listmodules})


@login_required
def BlivraisonView(request):
    listmodules = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    if ('dist_bonlivraison' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(Q(user=request.user, content_type__model='dist_bonlivraison') |
                                          Q(user=request.user, content_type__model='dist_commande')).values_list(
                    'codename', flat=True)
            )
        )

        commandes = request.GET.get('commandes', None)

        if (commandes):
            blist = Dist_BonLivraison.objects.filter(commandes=commandes)
        else:
            blist = Dist_BonLivraison.objects.all()


        ville = request.GET.get('ville', None)
        distributeur = request.GET.get('distributeur', None)
        payeur = request.GET.get('payeur', None)
        validate = request.GET.get('validate', 'false')

        if (validate == "true"):
            is_validate = True
        else:
            is_validate = False


        if (ville):
            blist = blist.filter(payeur__distributeur__user__ville__id=ville)
        if (distributeur):
            blist = blist.filter(payeur__distributeur__id=int(distributeur))
        if (payeur):
            blist = blist.filter(payeur__id=int(payeur))

        blist = blist.filter(validate=is_validate)

        blist = blist.values(
            'id',
            'commandes__user__id',
            'facture',
            'date_ajout',
            'date_facturation',
            'date_echeance',
            'fc_file',
            'bl_file',
            'total'
        )

        listedist = Distributeur.objects.filter(user__is_active=True)
        listepaye = Payeur.objects.filter(distributeur__in=listedist)
        liste_ville = Ville.objects.all()

        return render(request, "Pumal/Blivraison.html", {
            "blist": blist,
            "cmd": commandes,
            "listeauth": listeauth,
            "listmodules": listmodules,
            'listedist': listedist,
            'listepaye': listepaye,
            'liste_ville': liste_ville
        })
    else:
        return render(request, "access.html", {"listmodules": listmodules})


@login_required
def EtatViewChange(request):
    try:
        commande = Dist_Commande.objects.get(id=int(request.GET.get('commande')))
        etat = request.GET.get('etat')

        commande.etat = etat
        commande.save()


    except Exception:
        pass

    return HttpResponse("Done")


class CMDList(APIView):
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        lise_prod = []

        # Initialize the base SQL query
        query = """SELECT id, code, distributeur, ville, date_ajout, total, etat, total_blivraison FROM cmdlist WHERE 1=1"""
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
                    "total_blivraison": row[7]
                })

        return JsonResponse(lise_prod, safe=False)
