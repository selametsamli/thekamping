from django.shortcuts import reverse, HttpResponseRedirect, get_object_or_404
from camp.models import Camp, CampParticipants, Feedback
from django.http import HttpResponse


def user_feedback_status(func):
    def wrap(request, *args, **kwargs):
        camp = get_object_or_404(Camp, slug=kwargs['slug'])
        camp_joined_list = CampParticipants.objects.filter(camp=camp, user=request.user)
        if camp.status == 'yayında':
            return HttpResponse('Değerlendirme yapmak için kampın başlamasını veya bitmesini beklemelisiniz.')
        elif Feedback.objects.filter(camp=camp, user=request.user).exists():
            return HttpResponse('Zaten bir değerlendirme yapmışsınız.')
        elif not camp_joined_list:
            return HttpResponse('Bu kampa katılmadığınız için değerlendirme yapamazsınız.')
        return func(request, *args, **kwargs)

    return wrap
