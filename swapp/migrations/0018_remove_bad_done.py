# Generated by Django 3.1.1 on 2020-10-01 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0017_auto_20201001_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bad',
            name='done',
        ),
    ]
