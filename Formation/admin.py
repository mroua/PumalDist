from django.contrib import admin

from .models import Formation, FormationSingup, Problematique, ImagesFormation

admin.site.register(Formation)
admin.site.register(FormationSingup)
admin.site.register(Problematique)
admin.site.register(ImagesFormation)