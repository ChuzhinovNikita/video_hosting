# Generated by Django 4.1.7 on 2023-09-04 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video_hosting', '0003_rename_сhannel_hostingсhannel_remove_video_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='chanel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='video_hosting.hostingсhannel'),
        ),
    ]
