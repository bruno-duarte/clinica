# Generated by Django 3.0.4 on 2020-05-10 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200506_0951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesettings',
            old_name='support',
            new_name='suport',
        ),
    ]