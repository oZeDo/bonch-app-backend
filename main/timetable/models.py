from django.db import models
from core.models import User


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=16, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    # probably !TODO: move time to date. Make start_time and end_time as DateTime
    # probably !TODO: remove pair number
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    pair = models.PositiveIntegerField()
    place = models.CharField(max_length=64, null=True)
    subject = models.CharField(max_length=256)
    subject_type = models.CharField(max_length=48)
    time = models.CharField(max_length=32)  # "10:45-12:20"
    tutor = models.CharField(max_length=128, null=True)
    tutor_fullname = models.CharField(max_length=128, null=True)
    created = models.DateTimeField(auto_now_add=True)

    unique_together = ['date', 'faculty', 'group', 'pair', 'place', 'subject', 'subject_type', 'time',
                       'tutor', 'tutor_fullname']
