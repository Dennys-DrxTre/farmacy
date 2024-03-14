# Generated by Django 4.0.2 on 2024-03-14 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona_residencia', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(max_length=2)),
                ('cedula', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=11)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino')], max_length=2)),
                ('f_nacimiento', models.DateField()),
                ('embarazada', models.BooleanField()),
                ('c_residencia', models.FileField(upload_to='constancias_residencias/')),
                ('direccion', models.TextField()),
                ('rol', models.CharField(choices=[('AD', 'Administrador'), ('AL', 'Almacenista'), ('AT', 'Atención al Cliente'), ('JC', 'Jefe de Comunidad'), ('PA', 'Paciente')], default='PA', max_length=2)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidades.zona')),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
        migrations.CreateModel(
            name='Beneficiado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(max_length=2)),
                ('cedula', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=11)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino')], max_length=2)),
                ('f_nacimiento', models.DateField()),
                ('embarazada', models.BooleanField()),
                ('c_residencia', models.FileField(upload_to='constancias_residencias/')),
                ('direccion', models.TextField()),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidades.perfil')),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidades.zona')),
            ],
            options={
                'verbose_name': 'Beneficiado',
                'verbose_name_plural': 'Beneficiados',
            },
        ),
    ]
