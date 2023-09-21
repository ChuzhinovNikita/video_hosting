from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('video/<int:pk>', views.video, name='video'),
    path('host_channel/<int:pk>', views.host_channel, name='host_channel'),
    path('create_channel/', views.create_channel, name='create_channel'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('create_video/', views.create_video, name='create_video'),
    path('saved_channel/<int:pk>', views.saved_channel, name='saved_channel'),
    path('channel_all/', views.channel_all, name='channel_all'),
    path('like/<int:pk>', views.like, name='like'),
    path('dislike/<int:pk>', views.dislike, name='dislike'),
    path('saved_video/<int:pk>', views.saved_video, name='saved_video'),
    path('library/', views.library, name='library'),
    path('edit_video/<int:pk>', views.edit_video, name='edit_video'),
    path('history/', views.history, name='history'),
    path('viewing_queue/', views.viewing_queue, name='viewing_queue'),
]
