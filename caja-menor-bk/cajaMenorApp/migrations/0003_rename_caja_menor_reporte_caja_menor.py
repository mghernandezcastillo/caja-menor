# Generated by Django 4.0.2 on 2022-04-19 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cajaMenorApp', '0002_rename_cajamenor_reporte_caja_menor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporte',
            old_name='Caja_menor',
            new_name='caja_menor',
        ),
    ]
