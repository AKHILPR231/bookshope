from django.db import models

from accounts.models import UserProfile
from bookapp.models import Book


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
