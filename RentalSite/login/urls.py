from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login,name='login'), #登录页面
    path('register',views.register,name= 'register'), #注册界面
    path('main',views.main,name='main'),#登录主界面
    path('landloadSetting',views.landloadSetting,name = 'landloadSetting'), #房东设置界面
    path('renterSetting',views.renterSetting,name = 'renterSetting'), #租户设置界面
    path('PaySetting',views.PaySetting,name='PaySetting'), #支付设置界面
    path('ErrorInfo',views.ErrorInfo,name='ErrorInfo'), #返回错误信息界面
    path('ModifyPassword',views.modifyPassword,name='modifyPassword'), #修改密码界面
    path('UpdateHouseInfo',views.UpdateHouseInfo,name='UpdateHouseInfo') #更新租房信息
]