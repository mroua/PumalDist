from django.shortcuts import render
from rest_framework.views import APIView


class DashView(APIView):
    http_method_names = ['get']
    def get(self, request):
        return render(request, 'Dashboard.html')