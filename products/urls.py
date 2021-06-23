from django.urls import path
from . import views
from favorites.views import add_favorite,favorite_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name='home'),
    path('add_product',views.add_product,name='add_product'),
    path('view_products',views.view_products,name='view_products'),
    path('edit_product/<str:id>/',views.edit_product,name='edit_product'),
    path('add_favorite/<str:id>/',add_favorite,name='add_favorite'),
    path('delete_product/<str:id>/',views.delete_product,name='delete_product'),
    path('detail_product/<str:id>/',views.detail_product,name='detail_product'),
    path('category_page/<slug>',views.category_page,name='category_page'),
    path('favorite_list/', favorite_list,name="favorite_list"),
    path('search/', views.search,name="search"),
    path('auto_complete/', views.auto_complete,name="auto_complete"),
]
