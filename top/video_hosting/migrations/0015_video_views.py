# Generated by Django 4.1.7 on 2023-09-21 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video_hosting', '0014_viewingqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.ManyToManyField(related_name='views', to=settings.AUTH_USER_MODEL),
        ),
    ]
