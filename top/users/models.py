from django.db import models
from django.contrib.auth.models import User


class UsersProfile(models.Model):
    image = models.ImageField(default='user.png', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

