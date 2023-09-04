from django.shortcuts import render, redirect
from .models import *


def home(request):
    posts = Video.objects.all()
    return render(request, 'home.html', {'posts': posts})


def video(request, pk):
    post = Video.objects.get(pk=pk)
    posts = Video.objects.all()
    return render(request, 'video.html', {'post': post, 'posts': posts})