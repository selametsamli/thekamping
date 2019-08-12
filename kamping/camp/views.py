from django.shortcuts import render, redirect

# Create your views here.
from camp.forms import CampForm
from camp.models import Camp


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


def camp_list(request):
    events = Camp.objects.all()
    context = {'events': events}
    return render(request, 'camp/camp-list.html', context)
