# Generated by Django 3.2.8 on 2023-12-07 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRB', '0007_remove_trades_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='trades',
            name='estado',
            field=models.CharField(default='activo', max_length=20),
        ),
    ]
