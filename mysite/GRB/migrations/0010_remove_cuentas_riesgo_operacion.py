# Generated by Django 3.2.8 on 2023-06-30 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GRB', '0009_cuentas_riesgo_operacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas',
            name='riesgo_operacion',
        ),
    ]
