from django.db import models

#用户登录
class UserLogin(models.Model):
    username = models.CharField(max_length=20) #用户名
    password = models.CharField(max_length=20) #密码

#用户注册
class UserRegister(models.Model):
    username = models.CharField(max_length=20)  #用户名
    password = models.CharField(max_length=20)  #密码
    idcard = models.CharField(max_length=20)  #身份证
    rentaddress=models.CharField(max_length=30) #租户地址
