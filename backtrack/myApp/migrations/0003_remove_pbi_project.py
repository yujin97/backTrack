# Generated by Django 2.1.8 on 2019-10-30 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_auto_20191030_0431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pbi',
            name='project',
        ),
    ]
