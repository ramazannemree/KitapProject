from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from direct.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'chat', views.ChatViewset, basename='chat'),
router.register(r'mesaj/(?P<id>\d+)', views.MessageViewset, basename='mesaj'),



urlpatterns = [ path('',include(router.urls))]