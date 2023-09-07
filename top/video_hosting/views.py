from django.shortcuts import render, redirect
from .models import *
from .forms import CreateChannelForm, CreateVideoForm
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Video.objects.all().order_by('-date')
    return render(request, 'home.html', {'posts': posts})


def video(request, pk):
    post = Video.objects.get(pk=pk)
    posts = Video.objects.all().order_by('-date')
    return render(request, 'video.html', {'post': post, 'posts': posts})


def host_channel(request, pk):
    data_channel = HostingСhannel.objects.get(pk=pk)
    posts = Video.objects.filter(channel=data_channel)
    return render(request, 'host_channel.html', {'data': data_channel, 'posts': posts})


@login_required(login_url='/users/log_in/')
def create_channel(request):
    form = CreateChannelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        HostingСhannel.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            author=request.user,
            image=request.FILES.get('image'),
            slug='@' + str(request.POST.get('name')).lower()
        )
        return redirect('video_hosting:home')

    return render(request, 'create_channel.html', {'form': form})


def subscriptions(request):
    my_subscriptions = HostingСhannel.objects.all()
    return render(request, 'subscriptions.html', {'my_subscriptions': my_subscriptions})


def create_video(request):
    form = CreateVideoForm(request.POST or None, request.FILES or None)
    pk_channel = request.GET.get('pk_channel')
    channel = HostingСhannel.objects.get(pk=pk_channel)

    if form.is_valid():
        Video.objects.create(
            preview=request.FILES.get('preview'),
            video=request.FILES.get('video'),
            name=request.POST.get('name'),
            slug='@' + str(request.POST.get('name')).lower(),
            description=request.POST.get('description'),
            channel=channel
        )

    return render(request, 'create_video.html', {'form': form})
