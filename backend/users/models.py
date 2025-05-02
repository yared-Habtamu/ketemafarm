from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    ROLES = (
        ('FARMER', 'Farmer'),
        ('LANDOWNER', 'Landowner'),
        ('BUYER', 'Buyer'),
    )

    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r'^\+251\d{9}$', 'Ethiopian phone format: +251XXXXXXXXX')]
    )
    role = models.CharField(max_length=10, choices=ROLES)

    # Make username optional and non-unique
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)

    # Use phone for authentication instead of username
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['role']  # For createsuperuser command

    objects = UserManager()  # Use our custom manager

    def __str__(self):
        return self.phone
