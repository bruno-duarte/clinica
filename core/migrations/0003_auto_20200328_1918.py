# Generated by Django 3.0.4 on 2020-03-28 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200328_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Nascimento'),
        ),
    ]
