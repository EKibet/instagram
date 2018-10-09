from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from annoying.decorators import ajax_request
from .forms import PhotoUploadModelForm,CommentForm,ProfileEditForm
from friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required

from .models import Image,Comment
from user.models import User,Profile


def home(request):
    posts= Image.objects.all(),
    commentform= CommentForm()
    
    return render(request, 'index.html', locals())

class PostListView(ListView):
    model=Image
    template_name= 'instagram/image_list.html' # <app>/<model>_<view_type>.html
    
    context_object_name = 'posts'
    ordering = ['-time_created']


def follow(request,user_id):
    res = AjaxFollow(request.Get,request.user)
    # context = { 'ajax_output': ajax_output()}
    context = { 'ajax_output': ajax_output()}
    return render(request,'instagram/profile.html',context)

class PostCreateView(CreateView):
    form_class = PhotoUploadModelForm
    template_name = 'instagram/image_upload.html'
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user_profile= self.request.user.profile
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    fields = ['title', 'content']

class create_comment(CreateView):
    model=Comment
    template_name= 'instagram/image_list.html' # <app>/<model>_<view_type>.html
    
    context_object_name = 'comments'
    ordering = ['-posted_on']

def signout(request):
    logout(request)
    return redirect('login')



def add_comment(request,post_id):
    post = get_object_or_404(Image, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('home')

@ajax_request

def add_like(request):
    post_pk = request.POST.get('post_pk')
    post = Image.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }








def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('home')

    profile = Profile.objects.get(user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile
    }
    print(profile.user.username)
    print(profile.image)
    return render(request, 'instagram/profile.html', context)

def post(request, pk):
    post = Image.objects.get(pk=pk)
    try:
        like = Like.objects.get(post=post, user=request.user)
        liked = 1
    except:
        like = None
        liked = 0

    context = {
        'post': post,
        'liked': liked
    }
    return render(request, 'instagram/post.html', context)


def likes(request, pk):
    #likes = IGPost.objects.get(pk=pk).like_set.all()
    #profiles = [like.user.userprofile for like in likes]

    post = Image.objects.get(pk=pk)
    profiles = Like.objects.filter(post=post)

    context = {
        'header': 'Likes',
        'profiles': profiles
    }
    return render(request, 'instagram/follow_list.html', context)


def followers(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.followers.all

    context = {
        'header': 'Followers',
        'profiles': profiles,
    }

    return render(request, 'instagram/follow_list.html', context)


def following(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.following.all

    context = {
        'header': 'Following',
        'profiles': profiles
    }
    return render(request, 'instagram/follow_list.html', context)

def profile_settings(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('index')

    if request.method == 'POST':
        print(request.POST)
        form = ProfileEditForm(request.POST, instance=user.profile, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        form = ProfileEditForm(instance=user.profile)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'instagram/profile_settings.html', context)