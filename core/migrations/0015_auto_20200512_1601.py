# Generated by Django 3.0.4 on 2020-05-12 19:01

import core.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200510_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusuario',
            name='imagem',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=core.models.get_file_path, verbose_name='Imagem'),
        ),
    ]
