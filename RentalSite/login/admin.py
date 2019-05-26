from django.contrib import admin
from.models import UserLogin,UserRegister,Rental_Info,RentHouseInfo,LandloadInfo
admin.site.register(UserLogin)
admin.site.register(UserRegister)
admin.site.register(RentHouseInfo)
admin.site.register(Rental_Info)
admin.site.register(LandloadInfo)
# Register your models here.
