from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls), #后台管理
    path('login/',include('login.urls')) #主要模块入口，包括登录，主界面等等
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root = settings.MEDIA_ROOT)
