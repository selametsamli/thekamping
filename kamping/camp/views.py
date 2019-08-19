from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from camp.forms import CampForm
from camp.models import Camp


def camp_list(request):
    camps = Camp.objects.all()
    context = {'camps': camps}
    return render(request, 'camp/camp-list.html', context)


def camp_create(request):
    form = CampForm()
    if request.method == 'POST':
        form = CampForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('/camp')
    return render(request, 'camp/camp-create.html', context={'form': form})


def camp_remove(request, slug):
    event = get_object_or_404(Camp, slug=slug)
    if request.user != event.user:
        return HttpResponseForbidden
    event.delete()
    return redirect('')


def camp_update(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    form = CampForm(instance=camp, data=request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(camp.get_absolute_url())
    context = {'form': form, 'event': camp}

    return render(request, 'camp/camp-update.html', context)
