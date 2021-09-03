# Generated by Django 3.1.6 on 2021-06-03 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=20)),
                ('faculty', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=100)),
                ('long', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('faculty', models.CharField(max_length=64)),
                ('group', models.CharField(max_length=20)),
                ('pair', models.CharField(max_length=5)),
                ('place', models.CharField(max_length=64, null=True)),
                ('subject', models.CharField(max_length=256)),
                ('subject_type', models.CharField(max_length=48)),
                ('time', models.CharField(max_length=20)),
                ('tutor', models.CharField(max_length=100, null=True)),
                ('tutor_full', models.CharField(max_length=256, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
