# Generated by Django 3.2.2 on 2022-05-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0003_auto_20220504_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='talle',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='talle_elegido',
            field=models.CharField(default='', max_length=10, verbose_name='talle_elegido'),
        ),
    ]
