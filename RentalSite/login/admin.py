from django.contrib import admin
from.models import UserLogin,UserRegister,RentalInfo,RentHouseInfo,LandloadInfo

#注册模型到后台，可以直接在admin后台进行增删改查
admin.site.register(UserLogin)
admin.site.register(UserRegister)
admin.site.register(RentHouseInfo)
admin.site.register(RentalInfo)
admin.site.register(LandloadInfo)
