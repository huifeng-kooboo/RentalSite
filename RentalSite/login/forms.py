#表单，用于认证用户信息
from django import forms

#登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(label="手机号",
                               max_length=11,
                               min_length=11,
                               error_messages={'required':'手机号不能为空','max_length':'手机号长度输入有误'},
                               required=True)
    password = forms.CharField(label="密码",
                               max_length=16,
                               min_length=6,
                               error_messages={'required': '密码不能为空','max_length':'密码长度为6-16位'},
                               required=True)

#注册表单验证
class RegisterForm(forms.Form):
    username = forms.CharField(label="手机号",
                               max_length=11,
                               min_length=11,
                               error_messages={'required': '手机号不能为空','max_length':'手机号长度输入有误'},
                               required=True)
    password = forms.CharField(label="密码",
                               max_length=16,
                               min_length=6,
                               error_messages={'required': '密码不能为空','max_length':'密码长度为6-16位'},
                               required=True)
    idcard = forms.CharField(label="身份证",
                             max_length=18,
                             min_length=18,
                             error_messages={'required': '身份证不能为空'},
                             required=True)
    rentaddress = forms.CharField(label="租户地址",
                                  max_length=30,
                                  min_length=8,
                                  error_messages={'required': '地址不能为空'},
                                  required=True)