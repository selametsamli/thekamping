from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from auths.forms import LoginForm, RegisterForm


def user_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('camp-list'))

    return render(request, 'auths/login.html', context={'form': form})


def user_register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('camp-list'))

    return render(request, 'auths/register.html', context={'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('camp-list'))
