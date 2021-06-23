from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import LoginView, KayitView,CreateChatView ,SingleTicketView, ActivateView, password_reset_request,LogoutView,ProfileView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', KayitView, name='register'),
    path('login', LoginView, name='login'),
    path("logout",LogoutView,name="logout"),
    path('api/', include('kullanici.api.urls')),    
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'), # üyelik aktifleştirme
    path("profile/",ProfileView,name="profile"),
    path("destek/",CreateChatView,name="destek"),
    path("destek/talep/<int:id>/",SingleTicketView,name="single-ticket"),
    ###################### ŞİFRE SIFIRLAMA ###########################
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", password_reset_request, name="password_reset")

]
