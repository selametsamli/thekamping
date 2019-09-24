from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Blog(models.Model):
    CATEGORY = (
        (None, 'Lütfen Seçiniz'), ('diğer', 'DİĞER'), ('yazılım', 'YAZILIM'), ('grafik tasarım', 'GRAFIK TASARIM'))

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Yazar', default=1)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def __str__(self):
        return "%s %s" % (self.title, self.author)
