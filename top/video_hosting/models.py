from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    preview = models.ImageField(default='default-video-image.png', blank=True)
    video = models.FileField(default='default-video.MP4', blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
