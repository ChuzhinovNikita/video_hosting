from django.shortcuts import render, redirect
from .models import *
from users.models import *
from .forms import CreateChannelForm, CreateVideoForm, EditVideoForm, CommentForm, ParentForm, ComplaintAboutThePostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    search = request.GET.get('search')
    posts = Video.objects.all().order_by('-date')
    user_prof = UsersProfile.objects.get(user=request.user)

    # ================== ПОИСК ==========================
    if search:
        posts = Video.objects.filter(Q(name__icontains=search))

    # ================== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ===========
    if request.user in [i.user for i in UsersProfile.objects.all()]:
        prof_user = UsersProfile.objects.get(user=request.user)
    else:
        prof_user = False

    return render(request, 'home.html', {'posts': posts, 'prof_user': prof_user, 'user_prof': user_prof})


@login_required(login_url='/users/log_in/')
def video(request, pk):
    post = Video.objects.get(pk=pk)
    posts = ViewingQueue.objects.filter(user=request.user)
    action = request.GET.get('action')

    # ========== УДАЛЕНИЕ ===========
    if action == 'delete':
        post.delete()
        return redirect('video_hosting:home')

    #  =============== СОХРАНИЕ В ИСТОРИЮ ======

    if post.name in [i.__str__() for i in History.objects.all()]:
        if request.user not in [i.user for i in History.objects.filter(video=post)]:
            History.objects.create(
                video=post,
                user=request.user
            )
    else:
        History.objects.create(
            video=post,
            user=request.user
        )

    #     =========== СМОТРЕТЬ ПОЗЖЕ ===========
    page_home = request.GET.get('page_home')

    if action == 'viewing_queue':
        if post.name in [i.__str__() for i in ViewingQueue.objects.all()]:
            if request.user not in [i.user for i in ViewingQueue.objects.filter(video=post)]:
                ViewingQueue.objects.create(
                    video=post,
                    user=request.user
                )
        else:
            ViewingQueue.objects.create(
                video=post,
                user=request.user
            )

        if page_home:
            return redirect('video_hosting:home')

    viewing = request.GET.get('viewing')

    if viewing:
        ViewingQueue.objects.get(video=post, user=request.user).delete()

    # ===================== ПРОСМОТРЫ ====================

    if action == 'views':
        post.views.add(request.user)

    # ==================== КОММЕНТАРИИ ====================
    comments = Comment.objects.filter(video=Video.objects.get(pk=pk))
    form_comment = CommentForm(request.POST or None)

    if form_comment.is_valid() and request.method == 'POST':
        instance = form_comment.save(commit=False)
        instance.video = Video.objects.get(pk=pk)
        instance.user = request.user
        instance.save()

        return redirect('video_hosting:video', pk=pk)
    #  ОТВЕТЫ НА КОММЕНТЫ
    parent = request.GET.get('parent')
    parent_form = ParentForm(request.POST or None)
    parent_comments = CommentParent.objects.all()
    self = request.GET.get('self')

    if self:
        if parent_form.is_valid() and request.method == 'POST':
            instance = parent_form.save(commit=False)
            instance.parent = Comment.objects.get(pk=parent)
            instance.user = request.user
            instance.self = CommentParent.objects.get(pk=self)
            instance.save()

            return redirect('video_hosting:video', pk=pk)
    else:
        if parent_form.is_valid() and request.method == 'POST':
            instance = parent_form.save(commit=False)
            instance.parent = Comment.objects.get(pk=parent)
            instance.user = request.user
            instance.save()

            return redirect('video_hosting:video', pk=pk)

    return render(request, 'video.html',
                  {'post': post, 'posts': posts, 'comments': comments, 'form_comment': form_comment,
                   'parent_form': parent_form, 'parent_comments': parent_comments})


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
    video_pk = request.GET.get('pk')
    page_video = request.GET.get('page_video')

    if request.user not in data_channel.saved_channel.all():
        data_channel.saved_channel.add(request.user)
    elif request.user in data_channel.saved_channel.all():
        data_channel.saved_channel.remove(request.user)

    if page_video:
        return redirect('video_hosting:video', pk=video_pk)
    else:
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
def com_like(request, pk):
    comment_data = Comment.objects.get(pk=pk)

    if request.user not in comment_data.com_likes.all():
        comment_data.com_likes.add(request.user)
        comment_data.com_dislikes.remove(request.user)
    elif request.user in comment_data.com_likes.all():
        comment_data.com_likes.remove(request.user)

    return redirect('video_hosting:video', pk=comment_data.video.pk)


@login_required(login_url='/users/log_in')
def com_dislike(request, pk):
    comment_data = Comment.objects.get(pk=pk)

    if request.user not in comment_data.com_dislikes.all():
        comment_data.com_dislikes.add(request.user)
        comment_data.com_likes.remove(request.user)
    elif request.user in comment_data.com_dislikes.all():
        comment_data.com_dislikes.remove(request.user)
    return redirect('video_hosting:video', pk=comment_data.video.pk)


@login_required(login_url='/users/log_in')
def com_like_parent(request, pk):
    comment_data = CommentParent.objects.get(pk=pk)

    if request.user not in comment_data.com_likes_parent.all():
        comment_data.com_likes_parent.add(request.user)
        comment_data.com_dislikes_parent.remove(request.user)
    elif request.user in comment_data.com_likes_parent.all():
        comment_data.com_likes_parent.remove(request.user)

    return redirect('video_hosting:video', pk=comment_data.parent.video.pk)


@login_required(login_url='/users/log_in')
def com_dislike_parent(request, pk):
    comment_data = CommentParent.objects.get(pk=pk)

    if request.user not in comment_data.com_dislikes_parent.all():
        comment_data.com_dislikes_parent.add(request.user)
        comment_data.com_likes_parent.remove(request.user)
    elif request.user in comment_data.com_dislikes_parent.all():
        comment_data.com_dislikes_parent.remove(request.user)
    return redirect('video_hosting:video', pk=comment_data.parent.video.pk)


@login_required(login_url='/users/log_in')
def saved_video(request, pk):
    post = Video.objects.get(pk=pk)

    if request.user not in post.saved_video.all():
        post.saved_video.add(request.user)
    elif request.user in post.saved_video.all():
        post.saved_video.remove(request.user)

    return redirect('video_hosting:video', pk=pk)


def channel_all(request):
    search = request.GET.get('search')
    data_channel = HostingСhannel.objects.all()

    # ============== ПОИСК ====================
    if search:
        data_channel = HostingСhannel.objects.filter(Q(name__icontains=search))

    return render(request, 'channel_all.html', {'channels': data_channel})


@login_required(login_url='/users/log_in')
def library(request):
    posts = Video.objects.all()
    action = request.GET.get('action')

    posts = posts.filter(saved_video=request.user) if action == 'saved_video' else posts
    posts = posts.filter(likes=request.user) if action == 'favorite' else posts

    return render(request, 'library.html', {'posts': posts})


@login_required(login_url='/users/log_in')
def history(request):
    history_user = History.objects.filter(user=request.user).order_by('-date')

    if history_user.count() > 10:
        history_user[10].delete()

    return render(request, 'history.html', {'history_user': history_user})


@login_required(login_url='/users/log_in')
def viewing_queue(request):
    viewing_queue_posts = ViewingQueue.objects.filter(user=request.user)

    return render(request, 'viewing_queue.html', {'viewing_queue_posts': viewing_queue_posts})


def complaint_form(request):
    form = ComplaintAboutThePostForm(request.POST or None)
    self = request.GET.get('self')
    pk = request.GET.get('pk')
    video_page_pk = request.GET.get('video_page')
    home_page = request.GET.get('home_page')

    if self == 'video':
        if form.is_valid():
            ComplaintAboutThePost.objects.create(
                user=request.user,
                self_video=Video.objects.get(pk=pk),
                violation=request.POST.get('violation'),
                text_violation=request.POST.get('text_violation')
            )

            if video_page_pk:
                return redirect('video_hosting:video', pk=video_page_pk)
            elif home_page:
                return redirect('video_hosting:home')

    elif self == 'comment':
        if form.is_valid():
            ComplaintAboutThePost.objects.create(
                user=request.user,
                self_comment=Comment.objects.get(pk=pk),
                violation=request.POST.get('violation'),
                text_violation=request.POST.get('text_violation')
            )

            return redirect('video_hosting:video', pk=video_page_pk)

    elif self == 'parent':
        if form.is_valid():
            ComplaintAboutThePost.objects.create(
                user=request.user,
                self_comment_parent=CommentParent.objects.get(pk=pk),
                violation=request.POST.get('violation'),
                text_violation=request.POST.get('text_violation')
            )

            return redirect('video_hosting:video', pk=video_page_pk)

    return render(request, 'complaint_form.html', {'form': form})
