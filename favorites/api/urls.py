from django.urls import path
from .views import FavoritesListAPIView,FavoritesCreateAPIView,FavoriteDeleteAPIView


urlpatterns = [
    path('list',FavoritesListAPIView.as_view(), name='list' ),
    path('create',FavoritesCreateAPIView.as_view(), name='create' ),
    path('delete/<id>',FavoriteDeleteAPIView.as_view(), name='delete' )
]