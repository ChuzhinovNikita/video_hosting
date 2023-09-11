from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


def admin(request):
    return render(request, 'admin.html', {})
