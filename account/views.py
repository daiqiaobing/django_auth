# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from account.models import Account


@login_required
def index(request):
    """
    跳转主页面
    :param request:
    :return:
    """
    return render(request, 'index.html', locals())


def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        info = {}
        if user:
            auth.login(request, user)
            return render(request, 'index.html', locals())
        else:
            info['msg'] = 'the user or password is wrong!'
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html')


@login_required
@require_POST
@permission_required('add_permission', raise_exception=True)
def add_account(request):
    """
    添加帐号信息
    :param request:
    :return:
    """

    username = request.POST.get('username')
    password = request.POST.get('password')
    info = {}
    try:
        Account.objects.create(username=username, password=password)
        info['msg'] = 'the user %s is added!' % username
    except Exception:
        info['msg'] = 'the user %s add fail!' % username
    return render(request, 'index.html', locals())


def user_logout(request):
    """
    用户退出
    :param request:
    :return:
    """

    logout(request)
    return render(request, 'login.html')
