# Generated by Django 3.2.3 on 2022-07-19 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_alter_filial_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='filial',
            name='qr_url',
            field=models.CharField(default='', max_length=300, verbose_name='Ссылка для QR Кода'),
        ),
    ]
