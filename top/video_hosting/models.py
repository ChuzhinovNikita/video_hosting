from django.db import models
from django.contrib.auth.models import User


class HostingСhannel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(default='user.png', blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Video(models.Model):
    preview = models.ImageField(default='default-video-image.png', blank=True)
    video = models.FileField(default='default-video.MP4', blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(HostingСhannel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
