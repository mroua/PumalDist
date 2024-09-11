from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import *
from .Serializers import ProduitSerializer


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['type', 'mesure', 'couleur', 'active']



@login_required
def ProduitView(request):
    liste_type = TypeProduit.objects.all()
    liste_couleur = Couleur.objects.all()
    liste_mesure = Mesure.objects.all()

    produit = Produit.objects.filter(active = True)

    return render(request, "Produit.html", {
        'liste_type': liste_type,
        'liste_couleur': liste_couleur,
        'liste_mesure': liste_mesure,
        'produit': produit
    })




class ProductList(APIView):
    #permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        print('coucou')
        lise_prod = []

        # Retrieve filter parameters from the request
        couleur_produit = request.GET.get('couleur_produit')
        mesure_id = request.GET.get('mesure_id')
        typeproduit_id = request.GET.get('typeproduit_id')
        mesure_type = request.GET.get('mesure_type')
        active = request.GET.get('active')
        reference = request.GET.get('reference')

        # Build the base SQL query
        query = """SELECT produit_id, designation, image, prix_publique, prix_gros, active, reference, couleur, couleur_produit, 
                          mesure_id, mesure_designation, mesure_type, typeproduit_id, typeproduit_designation 
                   FROM products
                   WHERE 1=1"""

        # Add filters to the query if the corresponding filter parameter is provided
        filters = []
        params = []

        if couleur_produit:
            filters.append("couleur_produit = %s")
            params.append(couleur_produit)

        if mesure_id:
            filters.append("mesure_id = %s")
            params.append(mesure_id)

        if typeproduit_id:
            filters.append("typeproduit_id = %s")
            params.append(typeproduit_id)

        if mesure_type:
            filters.append("mesure_type = %s")
            params.append(mesure_type)

        if active:
            filters.append("active = %s")
            params.append(active)

        if reference:
            filters.append("reference = %s")
            params.append(reference)

        # If there are any filters, append them to the query
        if filters:
            query += " AND " + " AND ".join(filters)
        print(query)
        print(params)

        formatted_query = query.replace('%s', '{}').format(*params)

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(formatted_query)

            rows = cursor.fetchall()
            print(rows)
            for row in rows:
                print(row)
                lise_prod.append({
                    "produit_id": row[0],
                    "designation": row[1],
                    "image": row[2],
                    "prix_publique": row[3],
                    "prix_gros": row[4],
                    "active": row[5],
                    "reference": row[6],
                    "couleur": row[7],
                    "couleur_produit": row[8],
                    "mesure_id": row[9],
                    "mesure_designation": row[10],
                    "mesure_type": row[11],
                    "typeproduit_id": row[12],
                    "typeproduit_designation": row[13],
                })


        return JsonResponse(lise_prod, safe=False)


