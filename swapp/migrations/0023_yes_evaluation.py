# Generated by Django 3.1.1 on 2020-10-01 11:23

from django.db import migrations, models
import swapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0022_auto_20201001_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='yes',
            name='evaluation',
            field=models.IntegerField(blank=True, null=True, validators=[swapp.models.val]),
        ),
    ]
