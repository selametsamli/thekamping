from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from vote import *

from blog.forms import BlogForm
from blog.models import Blog
from django.http import JsonResponse
from auths.decorators import is_user_active


def post_list(request):
    posts = Blog.objects.all()
    return render(request, 'blog/post_list.html', context={'posts': posts})


@is_user_active
@login_required
def post_create(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return HttpResponseRedirect(blog.get_absolute_url())
    return render(request, 'blog/post_create.html', context={'form': form})


def post_detail(request, slug):
    data = {'score': ''}
    post = Blog.objects.get(slug=slug)
    user = request.user
    if request.is_ajax():
        status = request.GET.get('status')
        if status == 'vote_up':
            post.votes.up(user.id)
        else:
            post.votes.down(user.id)
        data.update({'score': post.vote_score})
        return JsonResponse(data=data)

    return render(request, 'blog/post_detail.html', context={'post': post})


@login_required(login_url=reverse_lazy('user-login'))
def post_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user != blog.author:
        return HttpResponseForbidden()
    form = BlogForm(instance=blog, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect(blog.get_absolute_url())
    context = {'form': form, 'blog': blog}
    return render(request, 'blog/post_update.html', context=context)



@login_required(login_url=reverse_lazy('user-login'))
def post_remove(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden
    post.delete()
    return HttpResponseRedirect(reverse('post-list'))
