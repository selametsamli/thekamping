from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from camp.forms import CampForm
from camp.models import Camp


def camp_list(request):
    camps = Camp.objects.all()
    context = {'camps': camps}
    return render(request, 'camp/camp-list.html', context)


@login_required(login_url=reverse_lazy('user-login'))
def camp_create(request):
    form = CampForm()
    if request.method == 'POST':
        form = CampForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.user = request.user
            camp.save()
            return redirect('/')
    return render(request, 'camp/camp-create.html', context={'form': form})


def camp_detail(request, slug):
    form = CampForm()
    camp = get_object_or_404(Camp, slug=slug)
    return render(request, 'Camp/camp-detail.html', context={'camp': camp, 'form': form})


@login_required(login_url=reverse_lazy('user-login'))
def camp_remove(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    camp.delete()
    return redirect('')


@login_required(login_url=reverse_lazy('user-login'))
def camp_update(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    form = CampForm(instance=camp, data=request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(camp.get_absolute_url())
    context = {'form': form, 'camp': camp}

    return render(request, 'camp/camp-update.html', context)


@login_required(login_url='/user/login/')
def camp_remove(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    camp.delete()
    return redirect('camp-list')
