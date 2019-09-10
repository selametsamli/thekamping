# Generated by Django 2.2.4 on 2019-09-10 18:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Hakkımda')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Profil Fotoğrafı')),
                ('birth_day', models.DateTimeField(blank=True, null=True, verbose_name='Doğum Tarihi')),
                ('sex', models.CharField(blank=True, choices=[(None, 'Cinsiyet Seçiniz'), ('diğer', 'DİĞER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN')], max_length=6, null=True, verbose_name='Cinsiyet')),
                ('user', models.OneToOneField(null=True, on_delete=True, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Kullanici Profilleri',
            },
        ),
    ]
