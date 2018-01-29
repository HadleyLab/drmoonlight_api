from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from apps.accounts.fields import AvatarField
from .choices import TIMEZONES


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email address',
        unique=True
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=30
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=30
    )
    timezone = models.CharField(
        verbose_name='Time zone',
        max_length=32,
        choices=TIMEZONES,
        default=settings.TIME_ZONE
    )
    avatar = AvatarField(
        blank=True, null=True)

    # Remove username field from AbstractUser
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @property
    def full_name(self):
        name = self.last_name + ' ' + self.first_name
        return name.strip() if name != ' ' else self.email

    @property
    def is_scheduler(self):
        return hasattr(self, 'scheduler')

    @property
    def is_resident(self):
        return hasattr(self, 'resident')

    @property
    def is_account_manager(self):
        return hasattr(self, 'accountmanager')

    @property
    def role(self):
        if self.is_account_manager:
            return 'account_manager'
        if self.is_scheduler:
            return 'scheduler'
        if self.is_resident:
            return 'resident'

        return 'user'
