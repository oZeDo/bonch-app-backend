from django.db import models
from core.models import User


# Create your models here.
class Group(models.Model):
    group = models.CharField(max_length=20)
    faculty = models.CharField(max_length=64)


class Tutor(models.Model):
    short = models.CharField(max_length=100)
    long = models.CharField(max_length=128)


class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    faculty = models.CharField(max_length=64)
    group = models.CharField(max_length=20)
    pair = models.CharField(max_length=5)
    place = models.CharField(max_length=64, null=True)
    subject = models.CharField(max_length=256)
    subject_type = models.CharField(max_length=48)
    time = models.CharField(max_length=20)
    tutor = models.CharField(max_length=100, null=True)
    tutor_full = models.CharField(max_length=256, null=True)
