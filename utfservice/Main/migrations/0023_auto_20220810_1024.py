# Generated by Django 3.2.3 on 2022-08-10 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0022_auto_20220810_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Полное имя'),
        ),
        migrations.AddField(
            model_name='profile',
            name='name_organization',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название организации'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, default=False, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_date_load_2gis',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 9, 21, 24, 36, 194333)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_date_load_google',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 9, 21, 24, 36, 194294)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_date_load_yandex',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 9, 21, 24, 36, 194361)),
        ),
    ]
