from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from auths.forms import LoginForm, RegisterForm
from camp.models import Camp, CampParticipants


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


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    camp_list = Camp.objects.filter(user=user)
    camp_joined_list = CampParticipants.objects.filter(user=user)
    camp_list_count = camp_list.count()

    context = {'user': user, 'camp_list': camp_list, 'camp_list_count': camp_list_count,
               'camp_joined_list': camp_joined_list

               }

    return render(request, 'auths/profile/userprofile.html', context=context)
