from django.db import models
from django.conf import settings
from shop.models import Product  

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    favorite_products = models.ManyToManyField(Product, blank=True, related_name='favorited_by')
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_favorites_count(self):
        return self.favorite_products.count()