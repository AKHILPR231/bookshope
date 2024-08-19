from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    name=models.CharField(max_length=200)
    address= models.TextField()
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    def __str__(self):
        return '{}'.format(self.user.username)
