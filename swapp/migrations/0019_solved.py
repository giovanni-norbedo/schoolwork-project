# Generated by Django 3.1.1 on 2020-10-01 02:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('swapp', '0018_remove_bad_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='swapp.bad')),
            ],
        ),
    ]
