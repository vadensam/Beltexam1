# Generated by Django 2.2.4 on 2020-05-22 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_wish_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='granted',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
