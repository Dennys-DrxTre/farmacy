# Generated by Django 4.0.2 on 2024-03-14 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiado',
            name='c_residencia',
            field=models.FileField(blank=True, null=True, upload_to='constancias_residencias/'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='c_residencia',
            field=models.FileField(blank=True, null=True, upload_to='constancias_residencias/'),
        ),
    ]