
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os
from django.db.models.signals import post_save

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    keywords = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    slug = models.CharField(max_length=100,editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    def get_slug(self):
        slug = slugify(self.category_name.replace("ı","i"))
        unique = slug
        number = 1

        while Category.objects.filter(slug = unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1

        return unique
    
    def save(self,*args,**kwargs):
        self.slug = self.get_slug()
        return super(Category,self).save(*args,**kwargs)

def product_name_validator(value):
    if len(value) < 5 or len(value) > 100 :
        raise ValidationError("Ürün adı 5 karakterden kısa 100 karakterden uzun olamaz")

def keywords_validator(value):
    if len(value) < 5 or len(value) > 100 :
        raise ValidationError("Anahtar kelimeler adı 5 karakterden kısa 100 karakterden uzun olamaz")

def description_validator(value):
    if len(value) < 5 or len(value) > 100 :
        raise ValidationError("Açıklama adı 5 karakterden kısa 100 karakterden uzun olamaz")

def integer_validator(value):
    if not isinstance(value,int):
        raise ValidationError("Bu Alan Sadece sayıdan oluşmalıdır")

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    product_name = models.CharField(max_length=100,validators=[product_name_validator])
    keywords = models.CharField(max_length=100,validators=[keywords_validator])
    description = models.CharField(max_length=100,validators=[description_validator])
    detail = models.TextField()
    slug = models.CharField(max_length=150,editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    price = models.IntegerField(validators=[integer_validator])
    amount = models.IntegerField(validators=[integer_validator])
    author = models.CharField(max_length=100,validators=[product_name_validator])

    def first_image(self):
        images = ProductImages.objects.filter(product_id = self.id)
        return images[0].image.url

    def __str__(self):
        return self.product_name

    def get_slug(self):
        slug = slugify(self.product_name.replace("ı","i"))
        unique = slug
        number = 1

        while Product.objects.filter(slug = unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1

        return unique
    
    def save(self,*args,**kwargs):
        self.slug = self.get_slug()
        return super(Product,self).save(*args,**kwargs)
    
    class Meta:
        ordering = ["-updated_time"]

def get_upload_path(instance, filename):
    return os.path.join("user_%d" % instance.product.user.id, "product_%d" % instance.product.id, filename)

class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return self.product.product_name

#Create slug new product
def create_slug(sender,instance,created,**kwargs):
    if created:
        slug = slugify(instance.product_name.replace("ı","i"))
        unique = slug
        number = 1
        while Product.objects.filter(slug = unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        urun = Product.objects.get(id=instance.id)
        urun.slug = unique
        urun.save()
        
post_save.connect(create_slug,sender=Product)
