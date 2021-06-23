from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter
from kullanici.api.views import UserViewSet,RegisterApiView,TestApiView,ProfileAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register',RegisterApiView.as_view(),name="aregister"),

    path('api-auth/',include('rest_framework.urls')),
    path('api/rest-auth/',include('rest_auth.urls')),
    path('test',TestApiView.as_view()),
    path('guncelle',ProfileAPIView.as_view(),name='profile-update')

]
