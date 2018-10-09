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
