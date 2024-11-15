from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fields = ['id', 'password','last_login','is_active','username','email','phone','date_joined','gender','role']  # 设定字段顺序
    first_name = None

    last_name = None
    gender = models.CharField(max_length=8, choices=(
        ('male', '男'), ('female', '女')), default='male')
    phone = models.CharField(max_length=11)
    # 用户角色，可以是'普通用户'，'景点管理员'，'总管理员'
    role = models.CharField(max_length=20, choices=(
        ('user', '普通用户'),
        ('attraction_manager', '景点管理员'),
        ('super_admin', '总管理员'),
    ), default='user')

    def __str__(self):
        return f"{self.username} ({self.id})"

    def save(self, *args, **kwargs):
        # 检查密码是否已加密
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)