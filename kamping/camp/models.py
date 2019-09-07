import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.template.defaultfilters import slugify, safe
from unidecode import unidecode


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('camp', unique_id, new_name)


class Camp(models.Model):
    CATEGORY = (
        (None, 'Lütfen Seçiniz'), ('diğer', 'DİĞER'), ('yazılım', 'YAZILIM'), ('grafik tasarım', 'GRAFIK TASARIM'))

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar", default=1)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    starter_time = models.TimeField(null=True, verbose_name='Başlangıç saati')

    starter_date = models.DateField(null=True, blank=True, verbose_name='Başlangıç günü')

    size = models.IntegerField(verbose_name='Katılımcı sayısı', null=True, default=0)
    location = models.CharField(null=True, max_length=255, verbose_name='Lokasyon')
    category = models.CharField(choices=CATEGORY, blank=True, null=True, max_length=53, verbose_name='Kategori')

    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')

    image = models.ImageField(default='default/default.jpg', verbose_name='Resim', upload_to=upload_to,
                              null=True, help_text='Kapak Fotoğrafı Yükleyiniz', blank=True)

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

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/default.jpg'

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            camp = Camp.objects.get(slug=self.slug)
            if camp.title != self.title:
                self.slug = self.get_unique_slug()

        super(Camp, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CampParticipants(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='camp_participants', on_delete=True)
    camp = models.ForeignKey(Camp, null=True, on_delete=True, related_name='camp_participants')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)

    class Meta:
        verbose_name_plural = 'Kampa gelen katılımcılar'

    def __str__(self):
        return "{} {}".format(self.user, self.camp)
