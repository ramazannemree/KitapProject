from django.db.models import fields
from rest_framework import serializers
from products.models import Category, Product,ProductImages


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name','keywords','description','image','slug']


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','user','categories','product_name','keywords','description','slug','created_time','updated_time','price','amount','detail','images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        categoriess = validated_data.pop(['categories'][0])
        product = Product.objects.create(**validated_data)

        for category in categoriess:
            product.categories.add(category)

        for image in images_data:
            ProductImages.objects.create(product=product,**image)
        return product
    

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['categories','product_name','keywords','description','price','amount','detail']
    
