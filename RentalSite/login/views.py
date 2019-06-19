from django.shortcuts import render,redirect
from django.http import HttpResponse
from.forms import LoginForm,RegisterForm
from.models import UserLogin,UserRegister,Rental_Info,RentHouseInfo,LandloadInfo
from.globalvariant import initParams,setLoginInfo,getLoginInfo,clearLoginInfo
from alipay import AliPay #调用支付宝接口

#用户登录
def login(request):
    if request.method == "POST":
        objPOST = LoginForm(request.POST) #验证表单
        ret = objPOST.is_valid() #判断是否有效
        if ret: #表单有效时候
            username = request.POST.get("username")
            password = request.POST.get("password")
            record = UserLogin.objects.filter(username=username,password=password) #获取数据库数据
            if len(record) < 1: #没找到数据
                warn_login_str = "用户名或密码错误"
                return render(request,"login/login.html",{"login_other_error":warn_login_str}) #返回用户名或密码错误信息
            else:
                #记录用户登录信息
                initParams()
                setLoginInfo("flag_login","1")
                setLoginInfo("username",username)
                return redirect("main") #进入主界面
        else:
            error = objPOST.errors
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
            record = UserRegister.objects.filter(username=username) #判断是否已经注册账号
            if len(record) < 1:#当没注册时：添加账号信息
                obj = UserRegister.objects.create(username=username,password=password,idcard=idcard,rentaddress=rentaddress) #保存到数据库当中
                obj_login = UserLogin.objects.create(username=username,password=password) #保存一份到登录数据库
                return redirect("login") #使用redirect方法，保证url跳转，而非只是界面跳转
            else:
                warn_str = "当前用户已注册" #返回当前用户已注册信息到前端
                return render(request,"login/register.html",{"warn_login":warn_str}) #返回当前账号已注册信息到前端界面,用js弹窗显示
        else:
            error = objPOST.errors
            return render(request,"login/register.html",{"register_error":error})
            #返回注册信息有误：根据表单验证情况
            #前端错误信息表示方法{{register_error.username}}
    return render(request,"login/register.html") #在没有POST请求时，进入注册主界面

#主界面
#应该有两个界面，第一个界面是房屋照片以及房屋名字，点进去第二个界面可以看到它的具体房屋信息
def main(request):
    username = getLoginInfo("username")
    house_info_list = RentHouseInfo.objects.all() #获得房屋信息集合
    #这个部分由房东在后台手动添加信息，前端负责展示信息即可。
    #当未登录账号时，返回错误界面
    if username == "":
        return redirect('ErrorInfo') #返回错误信息界面。重定向
    return render(request,"main/main.html",{"UserName":username,"HouseInfo":house_info_list}) #返回主界面


#租户设置页面(前端先判断数据是否为空)
def renterSetting(request):
    #获取租户信息
    rent_phone_number = getLoginInfo("username") #获取租户手机号
    rent_info_list = Rental_Info.objects.filter(rent_phone_number=rent_phone_number) #找到对应的租户信息，传到前端
    #租户部分，只负责一小部分
    if request.POST:
        #获取前端数据保存到前端界面当中
        return redirect("main") #进入主界面
    return render(request,"rent/rentsetting.html",{"rent_info":rent_info_list}) #进入租户设置界面

#房东设置部分（房东这边先设置）
def landloadSetting(request):
    renter_List = UserRegister.objects.all() #获取所有用户信息
    if request.POST:
        #获取界面输入的信息
        landload_name = request.POST.get("landload_name")
        phone_number = request.POST.get("phone_number")
        landload_address = request.POST.get("landload_address")
        rent_date = request.POST.get("rent_date")
        rent_price = request.POST.get("rent_price")
        water_price = request.POST.get("water_price")
        electric_price = request.POST.get("electric_price")
        network_price = request.POST.get("network_price")
        key_number = request.POST.get("key_number")
        air_condition = request.POST.get("air_condition")
        washing_machine = request.POST.get("washing_machine")
        rental_name = request.POST.get("rental_name") #用于关联到租户的那个表当中去
        record = LandloadInfo.objects.filter(rental_name=rental_name)
        if len(record) < 1:
            obj = LandloadInfo.objects.create(landload_name=landload_name,phone_number=phone_number,landload_address=landload_address,rent_date=rent_date,
                                              rent_price=rent_price,electric_price=electric_price,water_price=water_price,network_price=network_price,
                                              key_number=key_number,air_condition=air_condition,washing_machine=washing_machine,
                                              rental_name=rental_name)#保存信息到数据库当中
            obj_rental = Rental_Info.objects.create(rent_phone_number=rental_name,rent_Date=rent_date,rent_price=rent_price,
                                                    electric_price=electric_price,water_price=water_price,network_price=network_price,
                                                    key_number=key_number,air_condition=air_condition,washing_machine=washing_machine) #先保存这些信息到租户部分，剩余那个支付时间留给租户来设置。
            return redirect("main") #转到主界面
        #保存到数据库中
        return redirect("errormsg") #进入错误界面
    return render(request,"landload/landloadsetting.html",{'lanloadsetting':renter_List}) #进入房东设置界面

#价格费用界面由前端获取并计算
def PaySetting(request):
    if request.POST:
        return render(request,"rent/rentpay.html")
    return render(request,"rent/rentpay.html") #待完善

#错误信息界面
def ErrorInfo(request):
    return render(request,"errormsg.html") #直接返回错误界面