# Generated by Django 4.2.10 on 2024-03-16 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movimientos", "0002_alter_detalleingreso_ingreso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detallesolicitud",
            name="solicitud",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detalle",
                to="movimientos.solicitud",
            ),
        ),
    ]
