"""
URL configuration for novel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include, re_path
from django.views.static import  serve


from novel.settings import MEDIA_ROOT
from user import views

appname="novel"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('regsvr/', include('user.urls')),
    # path('logout/', include('user.urls')),
    path('index/',  include('index.urls')),
     # path('',  include('index.urls')),
     # path('', views.index, name='index'),
    path('xsfl/', views.basetest),
    path('comment/', include('purchase.urls')),
    path('search/',include('search.urls')),
    path('rank/',include('ranking.urls')),
    # path('novread/', include('purchase.urls')),
    path('', include('login.urls')),  # 登录
    path('login/', include('login.urls')),  # 登录

    path('wlgj/',include('wlgjxx.urls')),# 物流轨迹
    path('wlgl/', include('wlglmain.urls')),  # 物流轨迹
    path('wlsz/', include('wlgjsz.urls')),  # 物流设置
    path('wlxg/', include('wlgjxg.urls')),  # 物流修改
    path('wlgj_tree/', include('wlgjxg.urls')),  # 物流修改
    path('wlyhgl/', include('wlyhgl.urls')),  # 物流用户管理

    path('purchase/', include('purchase.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
