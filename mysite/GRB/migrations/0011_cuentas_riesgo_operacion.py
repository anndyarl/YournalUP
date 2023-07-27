# Generated by Django 3.2.8 on 2023-06-30 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRB', '0010_remove_cuentas_riesgo_operacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentas',
            name='riesgo_operacion',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Riesgo por operación'),
        ),
    ]