#这个模块主要是数据库模块，用于数据库的数据类型设计
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

#租房信息
class RentHouseInfo(models.Model):
    rental_name = models.CharField(max_length=20) #业主姓名
    phone_number = models.CharField(max_length=20) #手机号
    cur_address = models.CharField(max_length=30) #当前住址
    write_interview = models.CharField(max_length=50) #文字介绍
    house_image = models.ImageField(upload_to='img') #房屋图片
    house_price = models.IntegerField() #房屋价格

#房东设置部分
class LandloadInfo(models.Model):
    landload_name = models.CharField(max_length=20) #房东姓名
    phone_number = models.CharField(max_length=20) #房东电话
    landload_address = models.CharField(max_length=30) #房东住址
    rent_date = models.DateField() #租房时间
    rent_price = models.IntegerField() #设置房租
    electric_price = models.DecimalField(decimal_places=2,max_digits=7) #设置电费
    water_price = models.DecimalField(decimal_places=2,max_digits=7) #设置水费
    network_price = models.DecimalField(decimal_places=2,max_digits=7) #设置网费
    key_number = models.IntegerField() #钥匙数量
    air_condition = models.BooleanField() #是否有空调
    washing_machine = models.BooleanField() #是否有洗衣机
    rental_name = models.CharField(max_length=20) #租户手机号（相当于选择租户，设置完进行绑定）

#租户部分
class RentalInfo(models.Model):
    rent_phone = models.CharField(max_length=20) #租户手机号，用于关联
    rent_Date = models.DateField() #租房日期
    rent_price = models.IntegerField() #房租
    electric_price = models.DecimalField(decimal_places=2,max_digits=7) #设置电费
    water_price = models.DecimalField(decimal_places=2,max_digits=7) #设置水费
    network_price = models.DecimalField(decimal_places=2,max_digits=7) #设置网费
    key_number = models.IntegerField() #钥匙数量
    air_condition = models.BooleanField() #是否有空调
    washing_machine = models.BooleanField() #是否有洗衣机
    pay_date = models.DateField()#这个是用户设置部分，支付日期

