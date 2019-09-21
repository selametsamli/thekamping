from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse

from auths.forms import LoginForm, RegisterForm, UserProfileUpdateForm
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

    data = {'html': ''}

    page = request.GET.get('page1', 1)
    camp_list = Camp.objects.filter(user=user)
    camp_list_count = camp_list.count()
    camp_list = joined_camp_and_created_camp_paginate(camp_list, page)

    page2 = request.GET.get('page2', 1)
    camp_joined_list = CampParticipants.objects.filter(user=user)
    camp_joined_list_count = camp_joined_list.count()
    camp_joined_list = joined_camp_and_created_camp_paginate(camp_joined_list, page2)

    context = {'user': user, 'camp_list': camp_list, 'camp_list_count': camp_list_count,
               'camp_joined_list': camp_joined_list, 'camp_joined_list_count': camp_joined_list_count,
               'page': 'user-profile'

               }

    if request.is_ajax():
        html_camps = render_to_string('auths/profile/include/profile_camps_list.html', context=context)
        html_joined = render_to_string('auths/profile/include/profile_joined_camps_list.html', context=context)
        data.update({'html': html_camps, 'html_joined': html_joined})

        return JsonResponse(data=data)

    return render(request, 'auths/profile/userprofile.html', context=context)


def profile_update(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    birth_day = request.user.userprofile.birth_day

    initial = {'sex': sex, 'bio': bio, 'profile_photo': profile_photo, 'birth_day': birth_day}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=True)
            bio = form.cleaned_data.get('bio', None)
            sex = form.cleaned_data.get('sex', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)
            birth_day = form.cleaned_data.get('birth_day', None)

            user.userprofile.sex = sex
            user.userprofile.profile_photo = profile_photo
            user.userprofile.bio = bio
            user.userprofile.birth_day = birth_day
            user.userprofile.save()
            return HttpResponseRedirect(reverse('user-profile', kwargs={'username': user.username}))

    return render(request, 'auths/profile/profile-update.html', context={'form': form})


def joined_camp_and_created_camp_paginate(queryset, page):
    paginator = Paginator(queryset, 2)
    try:
        queryset = paginator.page(page)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        queryset = paginator.page(2)

    return queryset
