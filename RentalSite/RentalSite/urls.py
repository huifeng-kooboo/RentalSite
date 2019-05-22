from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls), #后台管理
    path('login/',include('login.urls')) #登录、注册模块
]
