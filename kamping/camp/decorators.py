from django.http import HttpResponseBadRequest
from django.shortcuts import reverse, HttpResponseRedirect


def is_user_active(func):
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.email_confirmed == False:
            return HttpResponseRedirect(reverse('email-verification'))
        return func(request, *args, **kwargs)

    return wrap


