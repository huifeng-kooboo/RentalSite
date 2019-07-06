from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from.forms import LoginForm,RegisterForm
from.models import UserLogin,UserRegister,RentalInfo,RentHouseInfo,LandloadInfo
from.globalvariant import initParams,setLoginInfo,getLoginInfo,clearLoginInfo
from django.views.decorators.csrf import ensure_csrf_cookie

#添加检查错误信息功能（待完善）
def checkErrorType():
    return 0

#用户登录
@ensure_csrf_cookie
def login(request):
    if request.method == "POST":
        objPOST = LoginForm(request.POST) #验证表单
        ret = objPOST.is_valid() #判断是否有效
        flag_href = 0 #0不跳转，1跳转
        error_info = '' #默认情况下错误信息为空
        postdata={
            'flag_href':flag_href,
            'error_info':error_info,
        }
        if ret: #表单有效时候
            username = request.POST.get("username")
            password = request.POST.get("password")
            record = UserLogin.objects.filter(username=username,password=password) #获取数据库数据
            if len(record) < 1: #没找到数据
                warn_login_str = "用户名或密码错误"
                postdata['error_info'] = warn_login_str
                return JsonResponse(postdata) #返回用户名或密码错误信息
            else:
                #记录用户登录信息
                initParams()
                setLoginInfo("flag_login","1")
                setLoginInfo("username",username)
                main_href = 1
                postdata['flag_href'] = main_href
                return JsonResponse(postdata) #进入主界面
        else:
            error = objPOST.errors
            error_tips = ''
            #error是字典形式，以下是字典的遍历
            for key in error:
                error_tips += error[key] #保存错误信息
            #遍历表单错误,保存到字符串数组error_tips
            postdata['error_info'] = error_tips
            return JsonResponse(postdata)
    return render(request,"login/login.html") #登录界面

#用户注册
@ensure_csrf_cookie
def register(request):
    if request.POST:
        flag_href = 0  #flag_href 用于跳转url。0表示保持register界面，1表示跳转到login界面
        error_info = '' #默认错误信息为空
        data = {'flag_href':flag_href,
                'error_info':error_info,}
        objPOST = RegisterForm(request.POST)
        ret = objPOST.is_valid()  # 先进行表单的验证；判断格式等问题是否有出错
        if ret:  # 表单有效时候
            username = request.POST.get("username")
            password = request.POST.get("password")
            idcard = request.POST.get("idcard")
            rentaddress = request.POST.get("rentaddress")
            record = UserRegister.objects.filter(username=username)  # 判断是否已经注册账号
            if len(record) < 1:  # 当没注册时：添加账号信息
                obj = UserRegister.objects.create(username=username, password=password, idcard=idcard,
                                                  rentaddress=rentaddress)  # 保存到数据库当中
                obj_login = UserLogin.objects.create(username=username, password=password)  # 保存一份到登录数据库
                flag_href_login = 1 #跳转到login界面
                data['flag_href'] = flag_href_login
                return JsonResponse(data) # 使用JsonResponse方法，传递json字符串到前端
            else:
                warn_str = "当前用户已注册"  # 返回当前用户已注册信息到前端
                data['error_info'] = warn_str
                return JsonResponse(data)
        else:
            error = objPOST.errors
            error_tips = ''
            #error是字典形式，以下是字典的遍历
            for key in error:
                error_tips += error[key] #保存错误信息
            #遍历表单错误,保存到字符串数组error_tips
            data['error_info'] = error_tips
            return JsonResponse(data)
    return render(request,"login/register.html")

#主界面主要是展示数据库房屋信息
def main(request):
    username = getLoginInfo("username")
    house_info_list = RentHouseInfo.objects.all() #获得房屋信息集合
    return render(request,"main/main.html",{"UserName":username,"HouseInfo":house_info_list}) #返回主界面

#实现房东添加房子照片等信息到前端界面中
def UpdateHouseInfo(request):
    #进来先判断是否已经登录
    username = getLoginInfo("username")
    if username == "":
       return redirect('ErrorInfo') #定位到错误界面，说明并未登录
    if request.POST:
        #获取前端传送过来的值
        rental_name = request.POST.get('rental_name')
        phone_number = request.POST.get('phone_number')
        cur_address = request.POST.get('cur_address')
        write_interview = request.POST.get('write_interview')
        house_image = request.POST.get('house_image')
        house_price = request.POST.get('house_price')
        #保存到数据库当中去
        obj = RentHouseInfo.objects.create(rental_name=rental_name,phone_number=phone_number,cur_address=cur_address,
                                           write_interview=write_interview,house_image=house_image,house_price=house_price)
        return redirect('main') #转回主界面
    return render(request,"landload/addhouseinfo.html") #添加租房信息到数据库当中

#租户设置:租户只负责显示数据,无法进行改动
def renterSetting(request):
    #获取租户信息
    rent_phone = getLoginInfo("username") #获取租户手机号
    rent_info_list = RentalInfo.objects.filter(rent_phone=rent_phone) #找到对应的租户信息，传到前端
    #说明房东未设置，直接报错即可  后期优化
    if len(rent_info_list) < 1:
        return redirect('ErrorInfo')
    #找到则返回正确界面
    return render(request,"rent/rentsetting.html",{"rent_info":rent_info_list[0]}) #进入租户设置界面

#房东设置部分（房东这边先设置）
def landloadSetting(request):
    cur_name = getLoginInfo('username') #获取登录名 #判断是否为房东---防止租户设置bug
    if not cur_name == 'admin':
        return redirect('ErrorInfo') #跳转至错误页面,不让进主界面
    renter_List = UserRegister.objects.all() #获取所有用户信息
    landload_name = 'admin' #设置管理员默认为admin
    if request.POST:
        #获取界面输入的信息
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
        pay_date = request.POST.get('pay_date') #用户交付房租日期
        record = LandloadInfo.objects.filter(rental_name=rental_name)
        if len(record) < 1:
            #数据库导入
            obj = LandloadInfo.objects.create(landload_name=landload_name,phone_number=phone_number,landload_address=landload_address,rent_date=rent_date,
                                              rent_price=rent_price,electric_price=electric_price,water_price=water_price,network_price=network_price,
                                              key_number=key_number,air_condition=air_condition,washing_machine=washing_machine,
                                              rental_name=rental_name)#保存信息到数据库当中
            obj_rental = RentalInfo.objects.create(rent_phone=rental_name,rent_Date=rent_date,rent_price=rent_price,
                                                  electric_price=electric_price,water_price=water_price,network_price=network_price,
                                                  key_number=key_number,air_condition=air_condition,washing_machine=washing_machine,pay_date=pay_date) #先保存这些信息到租户部分，剩余那个支付时间留给租户来设置。
            return redirect("main") #转到主界面
        else:
            #数据库更新(因为存在原先数据)
            LandloadInfo.objects.filter(rental_name=rental_name).update(landload_name=landload_name,phone_number=phone_number,landload_address=landload_address,rent_date=rent_date,
                                        rent_price=rent_price,electric_price=electric_price,water_price=water_price,network_price=network_price,
                                        key_number=key_number,air_condition=air_condition,washing_machine=washing_machine)
            RentalInfo.objects.filter(rent_phone=rental_name).update(rent_Date=rent_date, rent_price=rent_price,
                                     electric_price=electric_price, water_price=water_price,
                                     network_price=network_price,key_number=key_number, air_condition=air_condition,
                                     washing_machine=washing_machine,pay_date=pay_date)
            return redirect('main') #跳转至主界面
    return render(request,"landload/landloadsetting.html",{'renter_list':renter_List}) #进入房东设置界面

#价格费用界面
def PaySetting(request):
    #获取当前租户的账户
    cur_username = getLoginInfo('username')
    #判断是否账户登录
    if cur_username =="":
        return redirect('ErrorInfo')
    #计算租户需要支付的价格（不能用前端计算，考虑安全性问题）
    rent_Data = RentalInfo.objects.filter(rent_phone=cur_username)
    # >0:说明房东设置过租户房费，电费等信息了
    if len(rent_Data) > 0:
        #获取需要支付的价格
        str_rentprice =rent_Data[0].rent_price
        str_electricprice = rent_Data[0].electric_price
        str_waterprice = rent_Data[0].water_price
        str_netprice = rent_Data[0].network_price
        cur_pay_price = float(str_rentprice) + float(str_electricprice) + float(str_netprice) +float(str_waterprice)
        #cur_pay_price为本月需要支付的金额 包含水电费网费--
        data = {'str_paymoney':cur_pay_price}
        print(type(cur_pay_price)) #cur_pay_price 类型是float
        return render(request, "rent/rentpay.html",data)
    return render(request,"rent/rentpay.html") #待完善

#错误信息界面：所有错误界面都放在这
def ErrorInfo(request):
    #获取用户是否登录
    username = getLoginInfo("username")
    #如果不是管理员或者未登录
    if username == "" or not username == 'admin':
        error_info = '当前用户未登录'
        return render(request, "errormsg.html", {'error_info': error_info})
    return render(request,"errormsg.html") #直接返回错误界面

#修改密码界面
#待定，主要是因为个人信息设置部分已经可以实现修改密码的需求了
def modifyPassword(request):
    return render(request,"login/modifypassword.html") #定向到修改密码界面

#用户信息个人设置部分
def personInfo(request):
    cur_username = getLoginInfo("username") #获得登录的用户名
    if cur_username == "":
        error_info = '当前用户未登录'
        return render(request, "errormsg.html", {'error_info': error_info})
    else:
        personalData = UserRegister.objects.filter(username=cur_username)  # 获取指定数据[0]表示取第一个数据
        if request.POST:
            #获取前端输入的数据,其中password和rentaddress需要判断是否符合要求
            password = request.POST.get("password")
            rentaddress = request.POST.get("rentaddress")
            #更新数据库(只针对输入的值disabled获取的值为null)
            UserRegister.objects.filter(username=cur_username).update(password=password,rentaddress=rentaddress)
            UserLogin.objects.filter(username=cur_username).update(password=password)
            return redirect('main') #转到主界面
        return render(request, "main/personsetting.html",{'personal':personalData[0]})

#主要是用于展示房屋详细信息页面
def proInfo(request):
    username = getLoginInfo("username")
    #context = request.session.get('housename')
    house_info_list = RentHouseInfo.objects.all() #获得房屋信息集合
    #bug:调用两次get请求。 解决办法1：javascript中判断值是否为空，为空情况下调用get请求。（明早测试用下）
    if request.method == 'GET':
        house_name = request.GET.get('cur_title')
        #查找数据库
        #bug:为何第一次的时候house_name为none 猜测原因：第一次直接找的是name为cur_title的值(第二阶段的时候解决)
        #当 house_name不为空时候，获取数据库信息
        if not house_name == None:
            house_data = RentHouseInfo.objects.filter(rental_name=str(house_name))
            rental_name = house_data[0].rental_name #业主姓名
            house_price = house_data[0].house_price #价格
            #house_image = house_data[0].house_image #房子照片
            write_interview =house_data[0].write_interview #房屋介绍
            cur_address = house_data[0].cur_address #当前住址
            phone_number = house_data[0].phone_number #联系手机号
            data = {'rental_name':rental_name,'house_price':house_price,
                    'write_interview':write_interview,'cur_address':cur_address,'phone_number':phone_number}
            return JsonResponse(data)
    return render(request,'main/proinfo.html',{'UserName':username,'':house_info_list})