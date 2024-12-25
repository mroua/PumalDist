from django.contrib import admin

from .models import Formation, FormationSingup, Problematique, ImagesFormation, ImagesProblematique

admin.site.register(Formation)
admin.site.register(FormationSingup)
admin.site.register(Problematique)
admin.site.register(ImagesFormation)
admin.site.register(ImagesProblematique)
