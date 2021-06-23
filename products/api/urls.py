from .view import CategoryListAPIView, MyProductListAPIView,ProductDetailAPIView,ProductUptadeAPIView, ProductCreateAPIView
from django.urls import path
from django.urls.conf import include
urlpatterns = [
    path('list',MyProductListAPIView.as_view(),name='list'),
    path('detail/<slug>',ProductDetailAPIView.as_view(),name='detail'),
    path('update/<slug>',ProductUptadeAPIView.as_view(),name='update'),
    path('create',ProductCreateAPIView.as_view(),name='create'),
    path('category_list',CategoryListAPIView.as_view(),name='category_list'),
] 