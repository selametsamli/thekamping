from django.db import models


# Create your models here.


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
