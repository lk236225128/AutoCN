from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="male")
    department = models.CharField(max_length=100, default='')
    project = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = "用戶信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
