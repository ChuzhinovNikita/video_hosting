from django.shortcuts import render, redirect
from .models import *
from video_hosting.models import *
from users.models import *
from django.contrib.auth.decorators import login_required


def admin(request):
    complaints = ComplaintAboutThePost.objects.all()
    pk = request.GET.get('pk')
    action = request.GET.get('action')

    if action == 'delete':
        ComplaintAboutThePost.objects.get(pk=pk).delete()
        return redirect('staff:admin')

    return render(request, 'admin.html', {'complaints': complaints})


def complaint(request, pk):
    complaint_post = ComplaintAboutThePost.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'delete':
        complaint_post.delete()
        return redirect('staff:admin')

    if action == 'strike':
        if complaint_post.self_video:
            channel = HostingСhannel.objects.get(pk=complaint_post.self_video.channel.pk)
            if channel.strike < 3:
                channel.strike += 1
                channel.save()
            else:
                channel.blocked = True
                channel.save()
            Video.objects.get(pk=complaint_post.self_video.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')
        elif complaint_post.self_comment:
            user = UsersProfile.objects.get(user=complaint_post.self_comment.user)
            if user.strike < 3:
                user.strike += 1
                user.save()
            else:
                user.blocked = True
                user.save()
            Comment.objects.get(pk=complaint_post.self_comment.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')
        elif complaint_post.self_comment_parent:
            user = UsersProfile.objects.get(user=complaint_post.self_comment_parent.user)
            if user.strike < 3:
                user.strike += 1
                user.save()
            else:
                user.blocked = True
                user.save()
            CommentParent.objects.get(pk=complaint_post.self_comment_parent.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')

    if action == 'blocked':
        if complaint_post.self_video:
            channel = HostingСhannel.objects.get(pk=complaint_post.self_video.channel.pk)
            channel.blocked = True
            channel.save()
            Video.objects.get(pk=complaint_post.self_video.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')
        elif complaint_post.self_comment:
            user = UsersProfile.objects.get(user=complaint_post.self_comment.user)
            user.blocked = True
            user.save()
            Comment.objects.get(pk=complaint_post.self_comment.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')
        elif complaint_post.self_comment_parent:
            user = UsersProfile.objects.get(user=complaint_post.self_comment_parent.user)
            user.blocked = True
            user.save()
            CommentParent.objects.get(pk=complaint_post.self_comment_parent.pk).delete()
            complaint_post.delete()
            return redirect('staff:admin')

    return render(request, 'complaint.html', {'complaint': complaint_post})
