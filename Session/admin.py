from django.contrib import admin

from .models import Ville, Localite, CustomUser



class VilleAdmin(admin.ModelAdmin):
    list_display = ('id', 'designation')

class LocaliteAdmin(admin.ModelAdmin):
    list_display = ('id', 'ville', 'designation', 'ville_get')
    search_fields = ('ville',)

    def ville_get(self, obj):
        return obj.ville.designation

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'type', 'is_active')

admin.site.register(Ville, VilleAdmin)
admin.site.register(Localite, LocaliteAdmin)
admin.site.register(CustomUser, CustomUserAdmin)