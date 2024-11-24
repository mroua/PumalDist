from .models import UserURLHistory

class UserURLHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Ensure the user is authenticated through the session
            if request.user.is_authenticated:
                urlelem = '/api' + request.build_absolute_uri().split('/api')[1]
                #print(urlelem)
                listeelem = [
                    '/api/user/', '/api/distributeur/', '/api/payeur/', '/api/produit/', '/api/account/',
                    '/api/facture/', '/api/encaissement/', '/api/commandelines/', '/api/commande/', '/api/commandedetail/',
                    '/api/commande/', '/api/commandedetail/', '/api/blivraisonlines/', '/api/blivraisondetail/'
                ]

                for elem in listeelem:
                    if elem in urlelem and len(elem) < len(urlelem):
                        urlhistory = UserURLHistory.objects.create(
                            user=request.user,
                            url='/api' + request.build_absolute_uri().split('/api')[1],
                        )
                        urlhistory.save()
                        break  # Exit the loop once a match is found
        except Exception as e:
            # Optionally, log the exception for debugging
            print(f"Error in UserURLHistoryMiddleware: {e}")

        response = self.get_response(request)
        return response
