from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('video/<int:pk>', views.video, name='video'),
    path('host_channel/<int:pk>', views.host_channel, name='host_channel'),
    path('create_channel/', views.create_channel, name='create_channel'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('create_video/', views.create_video, name='create_video'),
]
