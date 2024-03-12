from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(
                {"Email": "이미 이메일이 존재하거나, 이메일 형식이 아닙니다"}
            )

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True, max_length=100)
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)

    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
