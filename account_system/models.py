from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class User_Manager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.country = "Myanmar"
        user.gender = "Male"
        user.DOB = "2003-03-30"
        user.save(using=self._db)
        return user

class User_Account(AbstractUser):
    #first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=9)
    DOB = models.DateField(null=True,blank=True)

    objects = User_Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
