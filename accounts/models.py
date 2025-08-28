from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User


class CustomUserManager(BaseUserManager):
    def create_user(self, university_email, password=None, **extra_fields):
        if not university_email:
            raise ValueError("The Email must be set")
        university_email = self.normalize_email(university_email)
        user = self.model(university_email=university_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, university_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(university_email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    university_email = models.EmailField(unique=True)
    university_roll_no = models.CharField(max_length=50, unique=True)
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Enter your WhatsApp number with country code (e.g., +923001234567)"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'university_email'
    REQUIRED_FIELDS = ['full_name', 'father_name', 'department', 'university_roll_no']

    def __str__(self):
        return self.university_email
