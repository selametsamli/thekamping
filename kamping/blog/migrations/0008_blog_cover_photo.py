# Generated by Django 2.2.4 on 2019-09-27 21:58

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190924_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='cover_photo',
            field=models.ImageField(blank=True, help_text='Kapak Fotoğrafı Yükleyiniz', upload_to=blog.models.upload_to, verbose_name='Kapak fotoğrafı'),
        ),
    ]
