# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class AccountManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_active, **extra_fields):
        if username:
            raise ValueError("the input username is error")
        if password:
            raise ValueError("the input password is error")
        user = self.model(username=username, password=password, is_staff=is_staff, is_active=False, **extra_fields)
        user.save(self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(self, username=username, password=password, is_staff=False, is_active=False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(self, username=username, password=password, is_staff=True, is_active=True,
                                 **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    # 用户名称
    username = models.CharField(unique=True, max_length=30)
    # password = models.CharField(max_length=20, null=False, default='123456')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []
    objects = AccountManager()

    class Meta(object):
        db_table = 'account'
        abstract = True

    def get_short_name(self):
        return self.get_username()

    def get_full_name(self):
        return self.get_username()


class Account(AbstractUser):
    nick_name = models.CharField(max_length=30, default='')

    # login_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

    class Meta(AbstractUser.Meta):
        permissions = (
            ('person:info', '我的面板:个人信息'),
            ('person:modify-pwd', '我的面板:修改密码'),
            ('user:list', '平台用户管理:用户帐号管理'),
            ('user:score-manage', '用户管理:积分账户管理'),
        )

        swappable = 'AUTH_USER_MODEL'


class Article(models.Model):
    content = models.TextField(max_length=300)
    head = models.CharField(max_length=50)
    author = models.OneToOneField(Account)
    title = models.CharField(max_length=50)
    create_date = models.DateTimeField()

    class Meta:
        db_table = 'article'


class Course(models.Model):
    classify = models.CharField(max_length=40)
    course_desc = models.CharField(max_length=100)
    students = models.ManyToManyField(Account)

    class Meta:
        db_table = 'course'
