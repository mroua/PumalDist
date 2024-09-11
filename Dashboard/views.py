from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required

from Commande.models import Dist_Commande
from Distributeur.models import Distributeur
from django.db import connection
import datetime

@login_required
def DashView(request):
    print(request)
    listedist = Distributeur.objects.all()
    if(request.user.type != "Distributeur"):
        dist_id = request.GET.get('distributeur', None)
        if(dist_id):
            first_dist = listedist.get(id=dist_id)
        else:
            first_dist = listedist.first()
    else:
        first_dist = Distributeur.objects.get(user=request.user)
    ristourn_a = first_dist.ristourn_a
    ristourn_na = first_dist.ristourn_na
    objectif_a = first_dist.objectif_a
    objectif_m = first_dist.objectif_m
    plafonnement = first_dist.plafonnement
    echeance_j = first_dist.echeance_jour

    sqlcmd = """SELECT "month", "year", total FROM Total_BL WHERE distributeur_id="""+str(first_dist.id)
    #params = []

    this_month = float(datetime.datetime.today().month)
    this_year = float(datetime.datetime.today().year)
    achat_annuelle = 0
    achat_menssuelle = 0
    achat_menssuelle_m = []
    mois = []
    val = []

    with connection.cursor() as cursor:
        # Execute the SQL query with parameters
        cursor.execute(sqlcmd)#, params

        rows = cursor.fetchall()

        for row in rows:
            achat_annuelle += row[2]

            achat_menssuelle_m.append({
                int(row[1]): row[2]
            })
            mois.append(int(row[1]))
            val.append(row[2])

    graphe1 = {
        "mois": mois,
        "valeur": val,
    }

    listecmd = Dist_Commande.objects.filter(
        distributeur=first_dist,
        date_ajout__year=this_year,
        date_ajout__month=this_month
    )

    nbr_cmd_reception = listecmd.filter(etat="Reception")
    nbr_cmd_traitement = listecmd.filter(etat="Traitement")
    nbr_cmd_preparation = listecmd.filter(etat="Preparation")
    nbr_cmd_encours = listecmd.filter(etat="En cours")

    sqlcmd = """SELECT sum(total), code_payeur, payeur, payeur_id, distributeur, sum(CreanceG), 
    sum(CreanceE), sum(nbrfacture), sum(nbrfactureEc), sum(EM), 
    sum(EA) FROM creancedash where distributeur = """+str(first_dist.id) + """ group by payeur_id """

    with connection.cursor() as cursor:
        # Execute the SQL query with parameters
        cursor.execute(sqlcmd)  # , params

        rows = cursor.fetchall()
        listedata = []

        for row in rows:
            listedata.append({
                'payeur': row[2],
                'nbrfacture': int(row[7]),
                'nbrfactureEc': int(row[2]),
                'CreanceG2': row[3],
                'CreanceG': row[4],
                'CreanceE': row[5],
                'EM': row[6],
                'EA': row[7],
                'payeur_id': row[8],

            })

    TotalCre = sum(d['CreanceG'] for d in listedata)
    TotalCreE = sum(d['CreanceE'] for d in listedata)

    if objectif_a != 0:
        obj_annuel_p = (achat_annuelle / objectif_a) * 100
    else:
        obj_annuel_p = 0

    if objectif_m != 0:
        obj_menssuel_p = (achat_menssuelle / objectif_m) * 100
    else:
        obj_menssuel_p = 0

    if plafonnement != 0:
        en_cour_p = (TotalCre / plafonnement) * 100
    else:
        en_cour_p = 0

    en_cour = (plafonnement * en_cour_p) / 100

    sqlcmd = """select sum(quantite) as quantite_cmd, cdc.produit_id, cdc2.distributeur_id, p.typeproduit_designation, p.designation 
        from Commande_dist_commandelines cdc 
        join Commande_dist_commande cdc2 
        join products p on p.produit_id = cdc.produit_id
        where cdc2.etat <> 'Annule' and strftime('%Y', cdc2.date_ajout) = strftime('%Y', 'now') 
        and cdc2.distributeur_id="""+str(first_dist.id)+"""
        group by cdc.produit_id, p.typeproduit_designation, cdc2.distributeur_id 
        order by sum(quantite) desc limit 5
    """

    with connection.cursor() as cursor:
        # Execute the SQL query with parameters
        cursor.execute(sqlcmd)

        rows = cursor.fetchall()

        produit = []
        prod_qte = []
        for row in rows:
            produit.append(row[4])
            prod_qte.append(row[0])

        graph_5_famille = {
            "produit": produit,
            "valeur": prod_qte,
        }

    sqlcmd = """WITH all_months AS (
    SELECT 1 AS month UNION ALL
    SELECT 2 UNION ALL
    SELECT 3 UNION ALL
    SELECT 4 UNION ALL
    SELECT 5 UNION ALL
    SELECT 6 UNION ALL
    SELECT 7 UNION ALL
    SELECT 8 UNION ALL
    SELECT 9 UNION ALL
    SELECT 10 UNION ALL
    SELECT 11 UNION ALL
    SELECT 12
),
all_years AS (
    SELECT DISTINCT strftime('%Y', date_ajout) AS year
    FROM creance
),
distributeur_ids AS (
    SELECT DISTINCT distributeur_id
    FROM creance
),
year_month_distributeur_combinations AS (
    SELECT am.month, ay.year, di.distributeur_id
    FROM all_months am
    CROSS JOIN all_years ay
    CROSS JOIN distributeur_ids di
)
SELECT 
    ym.month,
    COALESCE(SUM(c.total), 0) AS total_sum,
    COALESCE(SUM(c.total_encaissement), 0) AS total_encaissement_sum,
    ym.year,
    ym.distributeur_id
FROM 
    year_month_distributeur_combinations ym
LEFT JOIN 
    creance c ON strftime('%m', c.date_ajout) = printf('%02d', ym.month)
    AND strftime('%Y', c.date_ajout) = ym.year
    AND c.distributeur_id = ym.distributeur_id
where ym.distributeur_id = """+ str(first_dist.id) +"""
        GROUP BY 
            ym.month, ym.year, ym.distributeur_id
        ORDER BY 
            ym.distributeur_id, ym.year, ym.month;
            """

    cre_enc = []
    mois = []
    creance_list = []
    encaiss = []

    with connection.cursor() as cursor:
        # Execute the SQL query with parameters
        cursor.execute(sqlcmd)

        rows = cursor.fetchall()
        for row in rows:
            cre_enc.append({
                "mois": int(row[0]),
                "creance": row[1],
                "enccaissements": row[2],
            })
            mois.append(int(row[0]))
            creance_list.append(row[1])
            encaiss.append(row[2])

    graph_bar = {
        "mois": mois,
        "encaissement": encaiss,
        "creance": creance_list
    }

    print(graph_bar)

    context = {
        "en_cour": en_cour,
        "en_cour_p": en_cour_p,
        "obj_menssuel_p": obj_menssuel_p,
        "obj_annuel_p": round(obj_annuel_p, 2),
        'TotalCreE': TotalCreE,
        'TotalCre': TotalCre,
        'graphe1': graphe1,
        'plafonnement': plafonnement,
        'echeance_jour': echeance_j,
        'ristourn_a': ristourn_a,
        'ristourn_na': ristourn_na,
        'objectif_a': objectif_a,
        'objectif_m': objectif_m,
        'achat_annuelle': achat_annuelle,
        'achat_menssuelle': achat_menssuelle,
        'achat_menssuelle_m': achat_menssuelle_m,
        'r_e': len(nbr_cmd_reception),
        'v_t': len(nbr_cmd_traitement),
        'prep': len(nbr_cmd_preparation),
        'e_c': len(nbr_cmd_encours),
        'graph_5_famille': graph_5_famille,
        'top_famille': produit,
        'graph_bar': graph_bar,
        'cre_enc': cre_enc,
        'rc_nbr': 0,
        'int_nbr': 0,
        'first_dist': first_dist,
        'listedist': listedist
    }

    #return render(request, 'DashboardPuma.html', context)
    return render(request, 'Pumal/Dashboard.html', context)