#全局变量模块，保存登录信息认证等东西

#使用前必须先调用该方法，创建一个全局变量集合
def initParams():
    global g_login_info #设置登录信息
    g_login_info = {}

#设置登录数据信息
#params:1.key 2.value
def setLoginInfo(key,value):#设置登录信息参数
    g_login_info[key]=value

#得到登录信息，
#return:""：说明未获取到信息
def getLoginInfo(key):
    #先判断是否被定义，即是否调用initParams方法
    try:
        return g_login_info[key]
    except Exception: #捕获所有异常都返回空
        return ""

#清空登录信息：用于在退出登陆时候调用
def clearLoginInfo():
    g_login_info.clear() #清空登录信息字典

