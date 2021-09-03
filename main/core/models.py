import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователей для кастомизации стандартной модели пользователя."""

    use_in_migrations = True

    def create_user(self, email, password):
        """Создать и сохранить пользователя с указанным email и паролем."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Создать и вернуть объект пользователя с правами суперпользователя(админа)."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    """Модель пользователя."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Cookie(models.Model):
    """Модель с куки файлами пользователей"""
    user = models.OneToOneField(
        User, related_name='auth_cookie',
        on_delete=models.CASCADE, verbose_name="User"
    )
    uid = models.CharField("Uid", max_length=40)
    miden = models.CharField("Miden", max_length=40)
    created = models.DateTimeField("Created", auto_now=True)
