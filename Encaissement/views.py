from django.contrib.auth.models import Permission
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection

from Distributeur.models import Distributeur, Payeur
from .Serializers import BanqueSerializer, AccountSerializer, FacturesSerializer, EncaissementSerializer
from .models import Banque, Account, Factures, Encaissement
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from datetime import date


# Create your views here.
@login_required
def EncaissementView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    if (request.user.type == "Distributeur"):
        distrib = Distributeur.objects.get(user =request.user)

        # Base SQL query
        query = """
                SELECT id, code, total, date_ajout, date_echeance, fc_file, complete, 
                       code_payeur, payeur, code_distributeur, distributeur, ville_id, total_encaissement, 
                       total_validation_depot_false, total_validation_depot_true, montant_echue, plafonnement, distributeur_id
                FROM creance
                WHERE distributeur_id = """ + str(distrib.id)

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
        return render(request, "Dist/Encaissement.html", {
            "lise_fact": lise_fact,
            "somme_total": somme_total,
            "somme_encai": somme_encai,
            "somme_circu": somme_circu,
            "somme_depot": somme_depot,
            "somme_echue": somme_echue,
            "distrib_id": distrib.id
        })

    else:

        if ('encaissement' in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type__model='encaissement').values_list('codename', flat=True)
                )
            )
            # Get the list of distributeurs and payeurs
            listedist = Distributeur.objects.filter(bloquer=False).order_by('id')
            listebanque = Banque.objects.all().order_by('designation')
            listepayeur = Payeur.objects.filter(distributeur=listedist.first())
            listefacture = Factures.objects.filter(bl__payeur = listepayeur.first(), complete=False)

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
                "somme_echue": somme_echue,
                "listeauth": listeauth,
                "listmodules": listmodules
            })
        else:
            return render(request,"access.html", {"listmodules": listmodules})




@login_required
def EncaissementDetailView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    if ('encaissement' in listmodules):
        listeauth = list(
            set(
                Permission.objects.filter(user=request.user, content_type__model='encaissement').values_list('codename', flat=True)
            )
        )

        sqlcdm = """
                        SELECT id, distributeur, payeur, montant, "type", validation_depot, validation, date_ajout, date_cheque, date_depot, type_validation 
                        FROM creancevalidation where validation = false order by  date_ajout desc
                     """

        with connection.cursor() as cursor:
            # Execute the SQL query with the applied filters
            cursor.execute(sqlcdm)
            rows = cursor.fetchall()

        list_elems = []
        for row in rows:
            list_elems.append({
                "id": row[0],
                "distributeur": row[1],
                "payeur": row[2],
                "montant": row[3],
                "type": row[4],
                "validation_depot": row[5],
                "validation": row[6],
                "date_ajout": row[7],
                "date_cheque": row[8],
                "date_depot": row[9],
                "type_validation": row[10],

            })
        encaissement = Encaissement.objects.all()


        return render(request, "Pumal/EncaissementDetail.html", {
            "encaissement": list_elems,
            "listeauth": listeauth,
            "listmodules": listmodules
        })
    else:
        return render(request,"access.html", {"listmodules": listmodules})




def FactureView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    if ('encaissement' in listmodules):
        return render(request, "Facture.html")
    else:
        return render(request,"access.html", {"listmodules": listmodules})


@login_required
def AccompteView(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )

    if(request.user.type == "Distributeur"):
        listeaccompte = Account.objects.filter(montant__gt=0, payeur__distributeur__user=request.user)
        return render(request, "Dist/Accompte.html", {
            "listeaccompte": listeaccompte

        })
    else:
        if ('encaissement' in listmodules):
            listeauth = list(
                set(
                    Permission.objects.filter(user=request.user, content_type__model='encaissement').values_list('codename', flat=True)
                )
            )

            listedist = Distributeur.objects.filter(bloquer=False).order_by('id')
            listebanque = Banque.objects.all().order_by('designation')
            listepayeur = Payeur.objects.filter(distributeur=listedist.first())

            listeaccompte = Account.objects.filter(montant__gt=0)
            return render(request, "Pumal/Accompte.html", {
                "listedist": listedist,
                "listebanque": listebanque,
                "listepayeur": listepayeur,
                "listeaccompte": listeaccompte,
                "listeauth": listeauth,
                "listmodules": listmodules
            })
        else:
            return render(request,"access.html", {"listmodules": listmodules})





'''


'''


class BanqueViewSet(viewsets.ModelViewSet):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        date_validation = request.data["date_validation"]
        validation = request.data["validation"]
        date_depot = request.data["date_depot"]
        validation_depot = request.data["validation_depot"]

        if (date_validation and date_validation != ""):
            instance.date_validation = date_validation
        if (date_depot and date_depot != ""):
            instance.date_depot = date_depot
        if(validation):
            instance.validation = validation
            instance.date_validation = date.today()
        if(validation_depot):
            instance.validation = validation
            instance.date_depot = date.today()


        instance.validation_depot = validation_depot
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FacturesViewSet(viewsets.ModelViewSet):
    queryset = Factures.objects.all()
    serializer_class = FacturesSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


class EncaissementViewSet(viewsets.ModelViewSet):
    queryset = Encaissement.objects.all()
    serializer_class = EncaissementSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        date_validation = request.data["date_validation"]
        validation = request.data["validation"]
        date_depot = request.data["date_depot"]
        validation_depot = request.data["validation_depot"]

        if (date_validation and date_validation != ""):
            instance.date_validation = date_validation
        if (date_depot and date_depot != ""):
            instance.date_depot = date_depot
        if(validation):
            instance.validation = validation
            instance.date_validation = date.today()
            listeaccompt = Account.objects.filter(encaissement = instance)
            for el in listeaccompt:
                el.validation = validation
                el.date_validation = date.today()
                el.save()
        if(validation_depot):
            instance.validation = validation
            instance.date_depot = date.today()
            listeaccompt = Account.objects.filter(encaissement = instance)
            for el in listeaccompt:
                el.validation_depot = validation_depot
                el.date_depot = date.today()
                el.save()


        instance.validation_depot = validation_depot
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def AccompteDist(request):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    if ('encaissement' in listmodules):
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
    else:
        return render(request,"access.html", {"listmodules": listmodules})




@login_required
def get_factures(request, payeur_id):
    listmodules  = list(
        set(request.user.user_permissions.values_list('content_type_id__model', flat=True))
    )
    if ('encaissement' in listmodules):
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
    else:
        return render(request,"access.html", {"listmodules": listmodules})
