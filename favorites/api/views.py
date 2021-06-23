from django.db.models import query
from .pagination import FavoritePagination
from favorites.models import Favorites
from .serializers import FavoritesSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from .permission import IsOwner
from rest_framework.permissions import IsAuthenticated

class FavoritesListAPIView(ListAPIView):
    serializer_class = FavoritesSerializer
    pagination_class = FavoritePagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Favorites.objects.filter(user=self.request.user)
        return queryset

class FavoritesCreateAPIView(CreateAPIView):
    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteDeleteAPIView(DestroyAPIView):
    queryset = Favorites.objects.all() 
    serializer_class = FavoritesSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated,IsOwner]
