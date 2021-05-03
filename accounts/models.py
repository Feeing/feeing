from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.models import Group

from .manager import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser):
    name = models.CharField('이름', max_length=20)
    username = models.CharField('ID', max_length = 30, unique = True)
    email = None
    password = models.CharField('비밀번호', max_length = 128)

    USERNAME_FIELD = 'username'
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    phone = models.CharField('휴대폰번호', max_length = 100)
    bank_account = models.CharField('환급 계좌번호', max_length = 20, null = True)
    in_groups = models.ManyToManyField(Group, blank=True, null=True)

    REQUIRED_FIELDS = ['name', 'phone', 'bank_account']

    def __str__(self) :
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self) :
        return self.is_admin