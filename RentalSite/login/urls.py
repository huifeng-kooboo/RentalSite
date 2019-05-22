from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login,name='login'), #登录页面
    path('register',views.register,name= 'register') #注册界面
]