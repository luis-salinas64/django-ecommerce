# Generated by Django 3.2.2 on 2021-10-21 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0003_auto_20211020_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talle',
            name='talle',
        ),
        migrations.AddField(
            model_name='talle',
            name='talles',
            field=models.CharField(choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')], default='xs', max_length=3),
        ),
        migrations.AlterField(
            model_name='talle',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
