from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, admin=False):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        user = self.model(username=username, email=email, admin=admin)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        return self.create_user(username, email, password, admin=True)
    

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin