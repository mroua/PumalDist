from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required


@login_required
class DashView(APIView):
    http_method_names = ['get']
    def get(self, request):
        return render(request, 'Dashboard.html')