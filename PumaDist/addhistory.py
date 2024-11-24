from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from Distributeur.models import Distributeur, Payeur
from Session.models import History, CustomUser


def addhistory(old, new, contenttype, action, user):
    print("coucou")
    print("*****************************************")
    print(old)
    print("*****************************************")
    print(new)
    print("*****************************************")

    username = user.username
    listelem = []
    id = user.id
    if(contenttype == 8):
        if(new['responsable'] == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=new['region'], is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(id=new['responsable']['id'], is_active=True)
            )

        urlelem = "/api/user/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 10):
        if (new['user']['responsable'] == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=new['user']['region'], is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True)|
                Q(type="Admin Régional", region=new['user']['region'], is_active=True) |
                Q(id=new['user']['responsable'], is_active=True)
            ).distinct()

        urlelem = "/api/distributeur/"

        for elem in listelem:
            if (elem.id != new['user']['id']):
                    history = History.objects.create(
                        elem_id=new['user']['id'],
                        user_representative=username,
                        action_flag=action,
                        old_msg=old,
                        new_msg=new,
                        content_type=contenttype,
                        user=id,
                        viewer_id=elem.id,
                        url=urlelem + str(new['user']['id']) + '/'
                    )
                    history.save()

    elif (contenttype == 11):
        dist = Distributeur.objects.get(id = int(new['distributeur']))
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=new['user']['region'], is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True)
            ).distinct()

        urlelem = "/api/payeur/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 15):
        content_type = ContentType.objects.get(id=15)

        permissions = Permission.objects.filter(content_type=content_type)

        listelem = CustomUser.objects.filter(user_permissions__in=permissions).distinct()

        urlelem = "/api/produit/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 18):
        dist = Distributeur.objects.get(id=int(new['distributeur']['id']))
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()

        urlelem = "/api/commandedetail/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 16):
        dist = Distributeur.objects.get(id=int(new['commandes']['distributeur']['id']))
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin") |
                Q(type="Admin Régional", region=dist.user.ville.region) |
                Q(type="Admin Wilaya", ville=dist.user.ville) |
                Q(id=dist.user.id)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()

        urlelem = "/api/blivraisondetail/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 22):
        payeur = Payeur.objects.get(id=int(new['payeur']))
        dist = payeur.distributeur
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()

        urlelem = "/api/encaissement/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 23):
        payeur = Payeur.objects.get(id=int(new['payeur']))
        dist = payeur.distributeur
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()

        urlelem = "/api/facture/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 20):
        payeur = Payeur.objects.get(id=int(new['payeur']))
        dist = payeur.distributeur
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()

        urlelem = "/api/account/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 25):
        listelem = CustomUser.objects.filter(is_active=True)

        urlelem = "/api/formation/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 27):
        payeur = Payeur.objects.get(id=int(new['payeur']))
        dist = payeur.distributeur
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()


        urlelem = "/api/formationsingup/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()

    elif (contenttype == 26):
        payeur = Payeur.objects.get(id=int(new['profile']))
        dist = payeur.distributeur
        if (dist.user.responsable == None):
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            )
        else:
            listelem = CustomUser.objects.filter(
                Q(type="Admin", is_active=True) |
                Q(type="Admin Régional", region=dist.user.ville.region, is_active=True) |
                Q(type="Admin Wilaya", ville=dist.user.ville, is_active=True) |
                Q(id=dist.user.responsable.id, is_active=True) |
                Q(id=dist.user.id, is_active=True)
            ).distinct()


        urlelem = "/api/problematique/"

        for elem in listelem:
            if (elem.id != new['id']):
                history = History.objects.create(
                    elem_id=new['id'],
                    user_representative=username,
                    action_flag=action,
                    old_msg=old,
                    new_msg=new,
                    content_type=contenttype,
                    user=id,
                    viewer_id=elem.id,
                    url=urlelem + str(new['id']) + '/'
                )
                history.save()



    """content_type = ContentType.objects.get(id=contenttype)
    print(dict)

    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=content_type.pk,
        object_id=dict['id'],  # Use the object being acted upon
        object_repr=user.username,  # Representation of the object
        action_flag=action,
        change_message=dict
    )"""