from django.shortcuts import render
from django.http import HttpResponse
from.forms import LoginForm,RegisterForm
from.models import UserLogin,UserRegister

#用户登录
def login(request):
    if request.method == "POST":
        objPOST = LoginForm(request.POST) #验证表单
        ret = objPOST.is_valid() #判断是否有效
        if ret: #表单有效时候
            username = request.POST.get("username")
            password = request.POST.get("password")
            record = UserLogin.objects.get(username=username,password=password) #获取数据库数据
            if record.DoesNotExist: #没找到数据
                warn_login_str = "用户名或密码错误"
                return render(request,"login/login.html",{"login_other_error":warn_login_str}) #返回用户名或密码错误信息
            else:
                return render(request,"main/main.html") #登录成功，进入主界面
        else:
            error = LoginForm.errors
            return render(request,"login/login.html",{"login_error":error}) #返回验证有效错误信息
    return render(request,"login/login.html") #登录界面

#用户注册
def register(request):
    if request.POST:
        objPOST = RegisterForm(request.POST)
        ret = objPOST.is_valid() #先进行表单的验证；判断格式等问题是否有出错
        if ret:#表单有效时候
            username = request.POST.get("username")
            password = request.POST.get("password")
            idcard = request.POST.get("idcard")
            rentaddress = request.POST.get("rentaddress")
            record = UserRegister.objects.get(username=username) #判断是否已经注册账号
            if record.DoesNotExist:#当没注册时：添加账号信息
                obj = UserRegister(username=username,password=password,idcard=idcard,rentaddress=rentaddress)
                obj_login = UserLogin(username=username,password=password) #保存一份到登录数据库
                obj.save() #添加数据到注册数据库
                obj_login.save() #同步数据到登录数据库
                return render(request,"login/login.html") #注册成功，进入登录界面
            else:
                warn_str = "当前用户已注册" #返回当前用户已注册信息到前端
                return render(request,"login/register.html",{"warn_login":warn_str}) #返回当前账号已注册信息到前端界面
        else:
            error = RegisterForm.errors
            return render(request,"login/register.html",{"register_error":error}) #返回注册信息有误：根据表单验证情况
    return render(request,"login/register.html") #在没有POST请求时，进入注册主界面

#主界面
def main(request):
    return render(request,"main/main.html") #返回主界面