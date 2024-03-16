# Generated by Django 4.2.10 on 2024-03-16 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventario",
            name="producto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inventario",
                to="inventario.producto",
                verbose_name="Producto",
            ),
        ),
    ]