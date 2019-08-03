#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def home(request):
    return render(request, 'chat/home.html')


def room(request, room_name, user_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user_name': mark_safe(json.dumps(user_name))
    })