# Generated by Django 2.2.4 on 2019-09-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0011_auto_20190919_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='cover_photo',
            field=models.CharField(max_length=250, null=True, verbose_name='cover_photo'),
        ),
    ]
