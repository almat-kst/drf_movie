# Generated by Django 3.2.6 on 2021-08-20 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описания'),
        ),
    ]