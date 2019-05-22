from django.shortcuts import render
from django.http import HttpResponse
from.forms import LoginForm,RegisterForm

#用户登录
def login(request):
    return render(request,"login/login.html")

#用户注册
def register(request):
    return render(request,"login/register.html")