# Generated by Django 3.1.1 on 2020-09-24 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0002_remove_ask_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='ask',
            name='done',
            field=models.BooleanField(default=True),
        ),
    ]
