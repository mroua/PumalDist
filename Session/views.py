from django.contrib.auth import authenticate, login as dj_login
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .Serializers import VilleSerializer, CustomUserSerializer

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
            return redirect('/dashboard')  # Redirect to the dashboard or another page
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
    return render(request, "Utilisateur.html", {'liste_users': liste_users,
                                                'users_select': users_select})