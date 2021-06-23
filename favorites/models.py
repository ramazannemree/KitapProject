from django.db import models
from products.models import Product
from django.conf import settings


class Favorites(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta():
        ordering = ['-id']

    def __str__(self):
        return self.user.username

