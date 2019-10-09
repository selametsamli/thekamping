from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.functions import datetime
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

from camp.forms import CampForm, PhotoForm, CommentForm, SearchForm, FeedbackForm
from camp.models import Camp, CampParticipants, Photo, Comment, Feedback
from django.db.models import Q

from kamping import settings
from auths.decorators import is_user_active
from camp.decorators import user_feedback_status


def camp_list(request):
    camps = Camp.objects.all()
    search_form = SearchForm(data=request.GET or None)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search', None)
        if search:
            camps = camps.filter(
                Q(content__icontains=search) | Q(title__icontains=search) | Q(
                    user__username__icontains=search)).distinct()

    context = {'camps': camps, 'search_form': search_form}
    return render(request, 'camp/camp-list.html', context)


@is_user_active
@login_required(login_url=reverse_lazy('user-login'))
def camp_create(request):
    form = CampForm()
    if request.method == 'POST':
        form = CampForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.user = request.user
            camp.save()
            slug = camp.slug
            url = reverse('basic-upload', kwargs={'slug': slug})
            return HttpResponseRedirect(url)
    return render(request, 'camp/camp-create.html', context={'form': form})


@is_user_active
@login_required(login_url=reverse_lazy('user-login'))
def upload_photo(request, slug):
    if request.user != get_object_or_404(Camp, slug=slug).user:
        raise Http404("Bu gönderiyi fotoğraf ekleyemezsiniz.")
    else:
        if request.method == 'GET':
            camp = get_object_or_404(Camp, slug=slug)
            photos_list = Photo.objects.filter(camp=camp)
            return render(request, 'camp/camp-create_step2.html', {'photos': photos_list, 'slug': slug})

        elif request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            camp = get_object_or_404(Camp, slug=slug)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.camp = camp
                photo.save()
                if camp.cover_photo == None:
                    camp.cover_photo = photo.file.url
                    camp.save()
                data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)


def camp_detail(request, slug):
    currentDT = datetime.datetime.now()
    currentDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    camp = get_object_or_404(Camp, slug=slug)
    starter_date = str(camp.starter_date) + " " + str(camp.starter_time)
    camp_image = Photo.objects.filter(camp=camp)
    comment_form = CommentForm(data=request.POST)

    if currentDT > starter_date:
        camp.status = 'başladı'
        camp.save()

    url = 'https://www.google.com/maps/search/'
    for i in Camp.objects.all():
        address = i.location
    url = url + str(address)
    form = CampForm()
    return render(request, 'Camp/camp-detail.html',
                  context={'camp': camp, 'form': form, 'url': url, 'camp_image': camp_image,
                           'comment_form': comment_form})


@is_user_active
@login_required(login_url=reverse_lazy('user-login'))
def camp_remove(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    camp.delete()
    return redirect('')


@is_user_active
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


@is_user_active
@login_required(login_url='/user/login/')
def camp_remove(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    if request.user != camp.user:
        return HttpResponseForbidden
    camp.delete()
    return redirect('camp-list')


@is_user_active
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


@is_user_active
def new_add_comment(request, pk, model_type):
    data = {'is_valid': True, 'camp_comment_html': '', 'model_type': model_type}

    nesne = None
    all_comment = None
    comment_form = CommentForm(data=request.POST)

    if model_type == 'camp':
        nesne = get_object_or_404(Camp, pk=pk)
    elif model_type == 'comment':
        nesne = get_object_or_404(Comment, pk=pk)
    else:
        raise Http404

    if comment_form.is_valid():
        icerik = comment_form.cleaned_data.get('icerik')
        Comment.add_comment(nesne, model_type, request.user, icerik)

    if model_type == "comment":
        nesne = nesne.content_object

    comment_html = render_to_string('camp/include/comment/comment-list-partial.html', context={'camp': nesne})

    data.update({
        'camp_comment_html': comment_html
    })

    return JsonResponse(data=data)


def get_child_comment_form(request):
    data = {'form_html': ''}
    pk = request.GET.get('comment_pk')
    comment = get_object_or_404(Comment, pk=pk)
    comment_form = CommentForm()
    form_html = render_to_string('camp/include/comment/comment-child-comment-form.html', context={
        'comment_form': comment_form,
        'comment': comment,
    }, request=request)

    data.update({
        'form_html': form_html
    })

    return JsonResponse(data=data)


@user_feedback_status
def feedback_create(request, slug):
    camp = get_object_or_404(Camp, slug=slug)
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.camp = camp
            feedback.user = request.user
            feedback.save()

    context = {'form': form, 'camp': camp}
    return render(request, 'feedback/feedback-create.html', context=context)
