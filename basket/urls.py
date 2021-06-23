from django.urls import path
from . import views

urlpatterns = [
    path('',views.basket_list,name='basket_list'),
    path('add_basket/<str:id>',views.add_basket,name='add_basket'),
    path('basket_details',views.basket_details,name='basket_details'),
    path('basket_payment',views.basket_payment,name='basket_payment'),
    path('basket_review',views.basket_review,name='basket_review'),
    path('basket_complete',views.basket_complete,name='basket_complete'),
]