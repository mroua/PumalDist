from django.urls import path

from .views import FormView, ProbView

urlpatterns = [
    path('', FormView, name='formation'),
    path('problematique', ProbView, name='problematique'),

]
