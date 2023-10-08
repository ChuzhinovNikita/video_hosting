from django.shortcuts import render, redirect
from .models import *
from video_hosting.models import *
from django.contrib.auth.decorators import login_required


def admin(request):
    complaints = ComplaintAboutThePost.objects.all()

    return render(request, 'admin.html', {'complaints': complaints})



