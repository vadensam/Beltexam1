# Generated by Django 2.2.4 on 2020-05-22 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='desc',
            field=models.CharField(default='description', max_length=100),
            preserve_default=False,
        ),
    ]
