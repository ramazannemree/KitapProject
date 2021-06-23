from rest_framework.mixins import DestroyModelMixin
from .permissions import IsOwner
from .serializers import CategorySerializer, ProductListSerializer,ProductUpdateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from products.models import Category, Product
from rest_framework.permissions import IsAuthenticated


class MyProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'slug'


class ProductUptadeAPIView(DestroyModelMixin,RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()