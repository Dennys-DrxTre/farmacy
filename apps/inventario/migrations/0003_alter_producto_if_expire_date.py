# Generated by Django 4.2.10 on 2024-03-17 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_inventario_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='if_expire_date',
            field=models.BooleanField(verbose_name='Si caduca'),
        ),
    ]