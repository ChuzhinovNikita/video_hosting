from django.shortcuts import render, redirect
from .models import *
from .forms import CreateChannelForm, CreateVideoForm, EditVideoForm
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Video.objects.all().order_by('-date')
    return render(request, 'home.html', {'posts': posts})


def video(request, pk):
    post = Video.objects.get(pk=pk)
    posts = Video.objects.all().order_by('-date')

    pk_v = request.COOKIES.get('pk')
    print(pk_v)

    return render(request, 'video.html', {'post': post, 'posts': posts})


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
        return redirect('video_hosting:host_channel', pk=pk_channel)

    return render(request, 'create_video.html', {'form': form})


def edit_video(request, pk):
    form = EditVideoForm(request.POST or None, request.FILES or None, instance=Video.objects.get(pk=pk))

    if form.is_valid():
        form.save()
        return redirect('video_hosting:video', pk=pk)

    return render(request, 'edit_video.html', {'form': form})


def delete(request):
    pk = request.GET.get('pk')
    post = Video.objects.get(pk=pk)
    delete_video = request.GET.get('delete')

    if delete_video:
        print(pk)
        post.delete()

    return render(request, 'delete.html', {})


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
    my_subscriptions = HostingСhannel.objects.filter(saved_channel=request.user)
    return render(request, 'subscriptions.html', {'my_subscriptions': my_subscriptions})


@login_required(login_url='/users/log_in/')
def saved_channel(request, pk):
    data_channel = HostingСhannel.objects.get(pk=pk)

    if request.user not in data_channel.saved_channel.all():
        data_channel.saved_channel.add(request.user)
    elif request.user in data_channel.saved_channel.all():
        data_channel.saved_channel.remove(request.user)

    return redirect('video_hosting:host_channel', pk=pk)


@login_required(login_url='/users/log_in')
def like(request, pk):
    post = Video.objects.get(pk=pk)

    if request.user not in post.likes.all():
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
    elif request.user in post.likes.all():
        post.likes.remove(request.user)

    return redirect('video_hosting:video', pk=pk)


@login_required(login_url='/users/log_in')
def dislike(request, pk):
    post = Video.objects.get(pk=pk)

    if request.user not in post.dislikes.all():
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    elif request.user in post.dislikes.all():
        post.dislikes.remove(request.user)

    return redirect('video_hosting:video', pk=pk)


@login_required(login_url='/users/log_in')
def saved_video(request, pk):
    post = Video.objects.get(pk=pk)

    if request.user not in post.saved_video.all():
        post.saved_video.add(request.user)
    elif request.user in post.saved_video.all():
        post.saved_video.remove(request.user)

    return redirect('video_hosting:video', pk=pk)


def channel_all(request):
    data_channel = HostingСhannel.objects.all()
    return render(request, 'channel_all.html', {'channels': data_channel})


def library(request):
    posts = Video.objects.all()
    action = request.GET.get('action')
    print(action)

    posts = posts.filter(saved_video=request.user) if action == 'saved_video' else posts

    return render(request, 'library.html', {'posts': posts})
