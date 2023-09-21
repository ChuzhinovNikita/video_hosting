from django.db import models
from django.contrib.auth.models import User


class HostingСhannel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(default='user.png', blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_channel = models.ManyToManyField(User, related_name='saved_channel')

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
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')
    saved_video = models.ManyToManyField(User, related_name='saved_video')

    def __str__(self):
        return self.name

    def likes_counter(self):
        return self.likes.count()


class History(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.video.name


class ViewingQueue(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.video.name
