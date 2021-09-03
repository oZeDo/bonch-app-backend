from django.db import models
from core.models import User


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    group = models.CharField(max_length=32)
    faculty = models.CharField(max_length=128)
    headman = models.BooleanField()
    course = models.IntegerField()
    birth_date = models.DateTimeField()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    subject = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    destination = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    read = models.BooleanField(default=True)
    message_id = models.IntegerField()
    addressed_id = models.IntegerField(null=True)
    deleted = models.BooleanField(default=False)


class File(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.IntegerField()
    semester = models.IntegerField()
    subject = models.CharField(max_length=255)
    mark = models.CharField(max_length=32)


class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.IntegerField()
    semester = models.IntegerField()
    subject = models.CharField(max_length=255)
    subject_type = models.CharField(max_length=64)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=32)
    mark = models.CharField(max_length=32)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    send_to = models.IntegerField()

