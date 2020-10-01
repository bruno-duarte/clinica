# Generated by Django 3.0.4 on 2020-04-26 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_sitesettings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'Configuração do Site', 'verbose_name_plural': 'Configurações do Site'},
        ),
        migrations.AlterField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Paciente', verbose_name='Comentário'),
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criada', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paciente_notificacao_set', to='core.Paciente', verbose_name='Notificação')),
            ],
        ),
    ]
