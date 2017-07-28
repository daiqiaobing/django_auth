# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from account.models import Account


class AccountBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = Account.objects.get(Q(username=username))
            if user.password == password:
                return user
        except Account.DoesNotExist:
            return None
