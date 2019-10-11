from django.http import HttpResponseBadRequest
from django.shortcuts import reverse, HttpResponseRedirect, get_object_or_404
from camp.models import Camp, CampParticipants


def user_feedback_status(func):
    def wrap(request, *args, **kwargs):
        camp = get_object_or_404(Camp, slug=kwargs['slug'])
        camp_joined_list = CampParticipants.objects.filter(camp=camp, user=request.user)
        if camp.status == 'yayında' or not camp_joined_list:
            return HttpResponseRedirect(reverse('camp-list'))
       # elif CampParticipants.objects.filter(camp=camp, user=request.user).exists():
        #    return HttpResponseRedirect(reverse('camp-list'))

        return func(request, *args, **kwargs)

    return wrap
