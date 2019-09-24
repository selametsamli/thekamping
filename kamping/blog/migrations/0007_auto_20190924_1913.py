# Generated by Django 2.2.4 on 2019-09-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_blog_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]