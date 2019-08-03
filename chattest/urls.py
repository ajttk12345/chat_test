#-*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

import chat.views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', chat.views.home, name='home'),
    url(r'^chat/(?P<room_name>[^/]+)/(?P<user_name>[^/]+)/$', chat.views.room, name='room'),
]
