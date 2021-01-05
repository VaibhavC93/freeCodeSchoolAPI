from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_student=False):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_student=is_student,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, prem, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app 'app_label'?"""
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile-images')
    discord_name = models.CharField(max_length=100)
    git_username = models.CharField(max_length=100)
    codepen_username = models.CharField(max_length=100)
    fcc_profile_url = models.CharField(max_length=255)

    LEVELS = (
        (1, 'Level 1'),
        (2, 'Level 2'),
    )

    current_level = models.IntegerField(choices=LEVELS)
    phone = models.CharField(max_length=10)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
