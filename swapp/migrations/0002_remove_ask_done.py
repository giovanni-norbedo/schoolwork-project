# Generated by Django 3.1.1 on 2020-09-24 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ask',
            name='done',
        ),
    ]
