from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)

from django.db.models import(
    EmailField,
    CharField,
    BooleanField,
)


# class UserManager(BaseUserManager):





# class User(AbstractBaseUser, PermissionsMixin): 

    # email = EmailField(max_length=150, unique=True, )