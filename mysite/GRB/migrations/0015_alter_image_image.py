# Generated by Django 3.2.8 on 2023-07-14 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GRB', '0014_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to='imagenes', verbose_name='Imagen'),
        ),
    ]
