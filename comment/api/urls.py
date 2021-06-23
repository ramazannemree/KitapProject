from django.urls import path
from .views import CommentListAPIView,CommentCreateAPIView


urlpatterns = [
    path('list',CommentListAPIView.as_view(), name='list' ),
    path('create',CommentCreateAPIView.as_view(), name='create' )
]