# Generated by Django 3.1.6 on 2021-06-03 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20210603_0457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='icon',
            new_name='picture',
        ),
    ]
