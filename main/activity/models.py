import uuid
from core.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Модель профиля организации."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(blank=True)
    members = models.ManyToManyField(User, through='ProfileMembers')
    social_vk = models.URLField(blank=True)
    social_inst = models.URLField(blank=True)

    def __str__(self):
        return self.name


class ProfileMembers(models.Model):
    """Модель для хранения пользователей в организации"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined = models.DateField()


class Event(models.Model):
    """Модель мероприятия."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    picture = models.ImageField()
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return u'%s' % self.name


# Форма мероприятия состоит из полей с вопросами. Для некоторых типов полей (мультивыбор/выбор) нужно заполнить
# модель Extra.
class Field(models.Model):
    """Модель для поля формы."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    required = models.BooleanField()
    order = models.PositiveIntegerField()  # Порядок отображения
    FieldTypes = (('T', 'Текст'), ('S', 'Строка'), ('B', 'Чек-бокс'), ('C', 'Выбор'), ('M', 'Мультивыбор'))
    type = models.CharField(max_length=1, choices=FieldTypes)

    def __str__(self):
        return u'%s - %s' % (self.event.name, self.name)


class Extra(models.Model):
    """Модель для дополнительных вариантов ответа."""
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)


class Participant(models.Model):
    """Модель участников которые записались """
    joined = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Answer(models.Model):
    """"""
    user = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True)
    answer = models.TextField()
    key = models.UUIDField()

