import os
from uuid import uuid4

from vote.models import VoteModel
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.urls import reverse
from unidecode import unidecode


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('blog', unique_id, new_name)


class Blog(VoteModel, models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='Yazar', default=1)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')
    cover_photo = models.ImageField(verbose_name='Kapak fotoğrafı', upload_to=upload_to,
                                    help_text='Kapak Fotoğrafı Yükleyiniz', blank=True)

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def __str__(self):
        return "%s %s" % (self.title, self.author)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Blog.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)

        slug = new_slug
        return slug

    def get_image(self):
        return self.cover_photo.url

    def save(self, *args, **kwargs):
        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id
            self.slug = self.get_unique_slug()
        else:
            blog = Blog.objects.get(slug=self.slug)
            if blog.title != self.title:
                self.slug = self.get_unique_slug()

        super(Blog, self).save(*args, **kwargs)
