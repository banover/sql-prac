# Generated by Django 4.1 on 2022-09-05 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(default=None, max_length=64, unique=True),
        ),
    ]
