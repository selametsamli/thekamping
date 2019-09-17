from django.contrib.auth.decorators import login_required
from django.db.models.functions import datetime
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.template import RequestContext

from camp.forms import CampForm
from camp.models import Camp, CampParticipants


def camp_list(request):
    camps = Camp.objects.all()
    context = {'camps': camps}
    return render(request, 'camp/camp-list.html', context)


@login_required(login_url=reverse_lazy('user-login'))
def camp_create(request):
    data = {'html': ''}
    form = CampForm(data=request.POST, files=request.FILES)

    step = request.POST.get('step')
    if step == 'step1' and request.method == 'POST':
        form = CampForm(data=request.POST, files=request.FILES)
        print(form.is_valid())
        if form.is_valid():
            camp = form.save(commit=False)
            camp.user = request.user
            camp.save()

            html = render_to_string('camp/include/camp-create/form-2-include.html', context={'form': form},
                                    request=request)
            data.update({'html': html})
            return JsonResponse(data=data)

    if request.is_ajax() and step == None:
        html = render_to_string('camp/include/camp-create/form-1-include.html', context={'form': form},
                                request=request)
        data.update({'html': html})
        return JsonResponse(data=data)

    return render(request, 'camp/camp-create.html', context={'form': form})


def camp_detail(request, slug):
    currentDT = datetime.datetime.now()
    currentDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    camp = get_object_or_404(Camp, slug=slug)
    starter_date = str(camp.starter_date) + " " + str(camp.starter_time)
    if currentDT > starter_date:
        camp.status = 'başladı'
        camp.save()

    url = 'https://www.google.com/maps/search/'
    for i in Camp.objects.all():
        address = i.location
    url = url + str(address)
    form = CampForm()
    return render(request, 'Camp/camp-detail.html', context={'camp': camp, 'form': form, 'url': url})


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


@login_required(login_url=reverse_lazy('user-login'))
def add_or_remove_camp(request, slug):
    data = {'count': 0, 'status': 'deleted'}
    camp = get_object_or_404(Camp, slug=slug)

    full_or_null = camp.size - camp.get_participant_count()
    if camp.status != 'yayında':
        msg = "Bu Kampa çoktan başladı geç kaldınız!! katılamazsınız!"
        durum = 'katilamaz'
        data.update({'msg': msg, 'durum': durum})
    else:
        participating_camp = CampParticipants.objects.filter(camp=camp, user=request.user)
        if participating_camp.exists():
            participating_camp.delete()
        elif full_or_null > 0:
            CampParticipants.objects.create(camp=camp, user=request.user)
            data.update({'status': 'added'})

    count = camp.get_participant_count()
    data.update({'count': count})
    return JsonResponse(data=data)
