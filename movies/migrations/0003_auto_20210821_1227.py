# Generated by Django 3.2.6 on 2021-08-21 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='movies.movie', verbose_name='фильм'),
        ),
        migrations.AlterField(
            model_name='review',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='movies.review', verbose_name='Родители'),
        ),
    ]