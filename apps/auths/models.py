from django.db import models

from django.core.exceptions import ValidationError
from typing import Any
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)

from django.db.models import(
    EmailField,
    CharField,
    BooleanField,
    ForeignKey,
    OneToOneField
)


class UserManager(BaseUserManager):
    def __obtain_user_instance(
            self,
            email: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'User':
        if not email:
            raise ValidationError(message='Email field is required', code='email_empty')

        new_user: 'User' = self.model(
            email = self.normalize_email(email),
            password=password,
            **kwargs,
        )
        return new_user


    def create_user(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'User':
        
        new_user: 'User' = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'User':
        """Create super user. Used by manage.py createsuperuser."""
        new_user: 'User' = self.__obtain_user_instance(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user






class User(AbstractBaseUser, PermissionsMixin): 

    email = EmailField(max_length=150, unique=True, db_index=True, null=False)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    password = CharField(null=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    oobjects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return super().__str__()


class UserProfile(models.Model):

    user = OneToOneField( User, on_delete=models.CASCADE, related_name='profile')
    bio = CharField(max_length=500)
    phone = CharField(max_length=15)
    avatar_url = CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Organization(models.Model):

    name = CharField(max_length=50, unique=True, null=False)
    description = CharField(max_length=500, null=False)
    owner = ForeignKey( User, on_delete=models.PROTECT, related_name='owned_organizations')
    contact_email = EmailField(max_length=50, null=False)
    website = CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)