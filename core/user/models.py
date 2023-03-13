import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# create user and superuser
class UserManager(BaseUserManager):
    
    def get_object_by_public_id(self, public_id):
        try:
           instance = self.get(public_id=public_id)
           return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self,username,email, password=None, **kwargs):
        if username is None:
            raise TypeError("User must have a username") #validation
        if email is None:
            raise TypeError("User must have an email")
        if password is None:
            raise TypeError("User must have an email")
        user = self.model(username=username, email=self.normalize_email(email),**kwargs) #call the model
        user.set_password(password) #set the password
        user.save(using=self._db) #save the user
        return user

    def create_superuser(self, username, email, password, **kwargs):

        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")

        user = self.create_user(username, email, password,**kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create User models here.
class User(AbstractBaseUser, PermissionsMixin):
   public_id = models.UUIDField(db_index=True, unique=True,
       default=uuid.uuid4, editable=False)
   username = models.CharField(db_index=True,
       max_length=255, unique=True)
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   email = models.EmailField(db_index=True, unique=True)
   is_active = models.BooleanField(default=True)
   is_superuser = models.BooleanField(default=False)
   created = models.DateTimeField(auto_now=True)
   updated = models.DateTimeField(auto_now_add=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   objects = UserManager()
   def __str__(self):
       return f"{self.email}"
   @property
   def name(self):
       return f"{self.first_name} {self.last_name}"
   

