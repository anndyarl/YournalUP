# Generated by Django 3.2.8 on 2023-06-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRB', '0006_auto_20230601_1556'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DESCUENTOS',
        ),
        migrations.AddField(
            model_name='cuentas',
            name='resultado_cuenta',
            field=models.CharField(max_length=100, null=True, verbose_name='Selecciona una resultado'),
        ),
    ]
