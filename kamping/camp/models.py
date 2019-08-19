from uuid import uuid4

from django.db import models

# Create your models here.
from django.urls import reverse
from django.template.defaultfilters import slugify, safe
from unidecode import unidecode


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

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            camp = Camp.objects.get(slug=self.slug)
            if camp.title != self.title:
                self.slug = self.get_unique_slug()

        super(Camp, self).save(*args, **kwargs)
