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
    strike = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def saved_channel_counter(self):
        return self.saved_channel.count()


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
    views = models.ManyToManyField(User, related_name='views')

    def __str__(self):
        return self.name

    def likes_counter(self):
        return self.likes.count()

    def views_counter(self):
        return self.views.count()


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    com_likes = models.ManyToManyField(User, related_name='com_likes')
    com_dislikes = models.ManyToManyField(User, related_name='com_dislikes')

    def __str__(self):
        return f"{self.user} - {self.video} - {self.date}"

    def com_likes_counter(self):
        return self.com_likes.count()


class CommentParent(models.Model):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    self = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.parent} - {self.date}"


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


VIOL_CHOICES = [
    ('Контент сексуального характера', 'Контент сексуального характера'),
    ('Жестокие или отталкивающие сцены', 'Жестокие или отталкивающие сцены'),
    ('Оскорбления или проявления нетерпимости', 'Оскорбления или проявления нетерпимости'),
    ('Домогательства или издевательства', 'Домогательства или издевательства'),
    ('Вредные или опасные действия', 'Вредные или опасные действия'),
    ('Ложная информация', 'Ложная информация'),
    ('Жестокое обращение с детьми', 'Жестокое обращение с детьми'),
    ('Пропаганда терроризма', 'Пропаганда терроризма'),
    ('Спам или ложная информация', 'Спам или ложная информация'),
    ('Нарушение законодательства', 'Нарушение законодательства'),
]


class ComplaintAboutThePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    self_video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE)
    self_comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    self_comment_parent = models.ForeignKey(CommentParent, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    violation = models.CharField(choices=VIOL_CHOICES, null=True, max_length=255)
    text_violation = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.violation}"
