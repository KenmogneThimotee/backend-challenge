from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.contrib.auth.models import UserManager
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> 'User':
        """
        Creates a new user with the specified email, password, first name, and last name.
        Returns the created user object.
        """
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first_name")
        if not last_name:
            raise ValueError("User must have a last)name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user



SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user in a web application.
    Inherits from AbstractBaseUser and PermissionsMixin.
    Includes fields for first name, last name, date of birth, and sex.
    Specifies email as the username field.
    Requires first_name and last_name fields.
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True, default='1900-01-01')

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ('email',)


    def save(self, *args, **kwargs):
        """
        Saves any changes made to the user's fields.
        """
        super().save(*args, **kwargs)
