from favorites.models import Favorites
from django.contrib import admin

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['user','product']

admin.site.register(Favorites,FavoritesAdmin)
