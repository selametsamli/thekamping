import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from vote.models import VoteModel
from django.shortcuts import get_object_or_404


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('camp', unique_id, new_name)


class Camp(models.Model):
    CATEGORY = (
        (None, 'Lütfen Seçiniz'), ('diğer', 'DİĞER'), ('yazılım', 'YAZILIM'), ('grafik tasarım', 'GRAFIK TASARIM'))

    STATUS = ((None, 'Lütfen Seçiniz'), ('yayında', 'Yayında'), ('başladı', 'Başladı'), ('bitti', 'Bitti'))

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar", blank=True)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    starter_time = models.TimeField(null=True, verbose_name='Başlangıç saati')

    starter_date = models.DateField(null=True, blank=True,
                                    verbose_name='Başlangıç günü')
    cover_photo = models.CharField(max_length=250, verbose_name='cover_photo', null=True)

    size = models.IntegerField(verbose_name='Katılımcı sayısı', null=True, default=0)
    location = models.CharField(null=True, max_length=255, verbose_name='Lokasyon')
    status = models.CharField(choices=STATUS, default='yayında', blank=True, null=True, max_length=53,
                              verbose_name='Status')

    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')

    def get_absolute_url(self):
        return reverse('camp-detail', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Camp.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    def get_participant_count(self):
        participant_count = self.camp_participants.count()
        return participant_count

    def get_come_camp_object(self):
        data_list = []
        qs = self.camp_participants.all()
        for obj in qs:
            data_list.append(obj.user)
        return data_list

    def get_added_camp_participants_user(self):
        return self.camp_participants.values_list('user__username', flat=True)

    def kalan_katilimci(self):
        katilimci_sayisi = self.get_participant_count()
        return self.size - katilimci_sayisi

    def get_status(self):
        return self.status

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            camp = Camp.objects.get(slug=self.slug)
            if camp.title != self.title:
                self.slug = self.get_unique_slug()

        super(Camp, self).save(*args, **kwargs)

        return self.title

    def __str__(self):
        return self.title

    def get_camp_new_comment(self):
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.id
        all_comment = Comment.objects.filter(content_type=content_type, object_id=object_id)
        return all_comment

    def get_camp_comment_count(self):
        return len(self.get_camp_new_comment())


class CampParticipants(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='camp_participants', on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, null=True, on_delete=models.CASCADE, related_name='camp_participants')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)

    class Meta:
        verbose_name_plural = 'Kampa gelen katılımcılar'

    def __str__(self):
        return "{} {}".format(self.user, self.camp)


class Photo(models.Model):
    camp = models.ForeignKey(Camp, null=True, on_delete=models.CASCADE, related_name='photo')
    file = models.FileField(upload_to='camp/', default='IMG_4029.JPG', verbose_name='resim', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.camp)

    def get_image(self):
        if self.file:
            return self.file.url


class Comment(VoteModel, models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='+', on_delete=True)
    is_parent = models.BooleanField(default=False)
    content_type = models.ForeignKey(to=ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    icerik = models.TextField(verbose_name='Yorum', max_length=1000, blank=False, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    # camp = models.ForeignKey(Camp, null=True, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        username = self.user.username
        text = "{0} {1}".format(username, self.content_type.model)
        return text

    class Meta:
        verbose_name_plural = "Questions"

    @classmethod
    def add_comment(cls, nesne, model_type, user, icerik):
        content_type = ContentType.objects.get_for_model(nesne.__class__)
        cls.objects.create(user=user, icerik=icerik, content_type=content_type, object_id=nesne.pk)
        if model_type == 'comment':
            nesne.is_parent = True
            nesne.save()

    def get_child_comment(self):
        if self.is_parent:
            content_type = ContentType.objects.get_for_model(self.__class__)
            all_child_comment = Comment.objects.filter(content_type=content_type, object_id=self.pk)
            return all_child_comment
        return None


class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='feedback', on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, null=True, on_delete=models.CASCADE, related_name='feedback')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    point = models.SmallIntegerField(verbose_name="Puan")
    content = models.TextField()

    def __str__(self):
        username = self.user.username
        return "{0} {1}".format(username, self.content)

    @classmethod
    def user_feedback_count(cls, user):
        count = cls.objects.filter(user=user).count()
        return count
