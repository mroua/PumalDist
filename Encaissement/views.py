from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.db import connection

from Distributeur.models import Distributeur, Payeur
from .Serializers import BanqueSerializer, AccountSerializer, FacturesSerializer, EncaissementSerializer
from .models import Banque, Account, Factures, Encaissement
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def EncaissementView(request):
    # Get the list of distributeurs and payeurs
    listedist = Distributeur.objects.filter(bloquer=True).order_by('id')
    listebanque = Banque.objects.all().order_by('designation')
    listepayeur = Payeur.objects.filter(distributeur=listedist.first())
    listefacture = Factures.objects.filter(payeur = listepayeur.first(), complete=False)

    # Base SQL query
    query = """
    SELECT id, code, total, date_ajout, date_echeance, fc_file, complete, 
           code_payeur, payeur, code_distributeur, distributeur, ville_id, total_encaissement, 
           total_validation_depot_false, total_validation_depot_true, montant_echue, plafonnement, distributeur_id
    FROM creance
    WHERE 1=1
    """

    # Filters and their corresponding parameters
    filters = []
    params = []

    # Apply filters based on the request parameters
    ville_id = request.GET.get('ville_id')
    if ville_id:
        filters.append("AND ville_id = %s")
        params.append(ville_id)

    code = request.GET.get('code')
    if code:
        filters.append("AND code LIKE %s")
        params.append(f"%{code}%")

    distributeur = request.GET.get('distributeur')
    if distributeur:
        filters.append("AND distributeur LIKE %s")
        params.append(f"%{distributeur}%")

    payeur = request.GET.get('payeur')
    if payeur:
        filters.append("AND payeur LIKE %s")
        params.append(f"%{payeur}%")

    date_ajout_debut = request.GET.get('date_ajout_debut')
    if date_ajout_debut:
        filters.append("AND date_ajout >= %s")
        params.append(date_ajout_debut)

    date_ajout_fin = request.GET.get('date_ajout_fin')
    if date_ajout_fin:
        filters.append("AND date_ajout <= %s")
        params.append(date_ajout_fin)

    complete = request.GET.get('complete')
    if complete:
        filters.append("AND complete = %s")
        params.append(complete)

    # Combine base query with filters
    if filters:
        query += " ".join(filters)

    with connection.cursor() as cursor:
        # Execute the SQL query with the applied filters
        cursor.execute(query, params)
        rows = cursor.fetchall()

    somme_total = 0
    somme_encai = 0
    somme_circu = 0
    somme_depot = 0
    somme_echue = 0

    lise_fact = []
    for row in rows:
        print(row)
        somme_total = somme_total + row[2]
        somme_encai = somme_encai + row[12]
        somme_circu = somme_circu + row[13]
        somme_depot = somme_depot + row[14]
        somme_echue = somme_echue + row[15]

        lise_fact.append({
            "id": row[0],
            "code": row[1],
            "total": row[2],
            "date_ajout": row[3],
            "date_echeance": row[4],
            "fc_file": row[5],
            "complete": row[6],
            "code_payeur": row[7],
            "payeur": row[8],
            "code_distributeur": row[9],
            "distributeur": row[10],
            "total_encaissement": row[12],
            "total_validation_depot_false": row[13],
            "total_validation_depot_true": row[14],
            "montant_echue": row[15],
            "plafonnement": row[16],
            "distributeur_id": row[17]
        })

    # Pass the results and lists to the template
    return render(request, "Pumal/Encaissement.html", {
        "listedist": listedist,
        "listebanque": listebanque,
        "listepayeur": listepayeur,
        "listefacture": listefacture,
        "lise_fact": lise_fact,
        "somme_total": somme_total,
        "somme_encai": somme_encai,
        "somme_circu": somme_circu,
        "somme_depot": somme_depot,
        "somme_echue": somme_echue
    })


@login_required
def EncaissementDetailView(request):
    encaissement = Encaissement.objects.all()

    print(encaissement)

    return render(request, "Pumal/EncaissementDetail.html", {
        "encaissement": encaissement,
    })


def FactureView(request):

    return render(request, "Facture.html")

def AccompteView(request):
    listedist = Distributeur.objects.filter(bloquer=True).order_by('id')
    listebanque = Banque.objects.all().order_by('designation')
    listepayeur = Payeur.objects.filter(distributeur=listedist.first())

    listeaccompte = Account.objects.filter(montant__gt=0)


    return render(request, "Accompte.html", {
        "listedist": listedist,
        "listebanque": listebanque,
        "listepayeur": listepayeur,
        "listeaccompte": listeaccompte
    })

'''


'''


class BanqueViewSet(viewsets.ModelViewSet):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class FacturesViewSet(viewsets.ModelViewSet):
    queryset = Factures.objects.all()
    serializer_class = FacturesSerializer

class EncaissementViewSet(viewsets.ModelViewSet):
    queryset = Encaissement.objects.all()
    serializer_class = EncaissementSerializer

@login_required
def AccompteDist(request):
    payeur = request.GET.get('payeur_id')

    total_amount = Account.objects.filter(
        validation=True,
        payeur=payeur,
        montant__gt=0
    ).aggregate(
        total_montant=Sum('montant')
    )


    accompte = total_amount['total_montant'] or 0
    return HttpResponse(accompte)


@login_required
def get_factures(request, payeur_id):
    factures = Factures.objects.filter(payeur_id=payeur_id, complete=False)
    facture_data = [
        {
            'id': facture.id,
            'code': facture.code,
            'montant': facture.restant,  # Use the restant property directly
            'date_echeance': facture.date_echeance.strftime('%Y-%m-%d') if facture.date_echeance else None
        }
        for facture in factures
    ]
    return JsonResponse({'factures': facture_data})