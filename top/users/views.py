from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth import login, logout
from video_hosting.models import *
from .models import *
from django.contrib.auth import update_session_auth_hash


def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:log_in')
    return render(request, 'register.html', {'form': form})


def log_in(request):
    valid_user = True

    if request.method == 'POST':
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('video_hosting:home')
        valid_user = False
    form = LoginForm()
    return render(request, 'log_in.html', {'form': form, 'valid_user': valid_user})


def log_out(request):
    logout(request)
    return redirect('users:log_in')


def edit_profile(request):
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        UsersProfile.objects.create(
            image=request.FILES.get('image'),
            user=request.user
        )
        form.save()
        return redirect('video_hosting:home')

    return render(request, 'edit_profile.html', {'form': form})
