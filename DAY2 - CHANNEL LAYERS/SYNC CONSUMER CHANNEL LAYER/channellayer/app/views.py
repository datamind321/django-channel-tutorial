from django.shortcuts import render,HttpResponse
from .models import *


# Create your views here.


def index(request,group_name):
    print('Group Name: ',group_name)
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name=group_name)
        group.save() 
    return render(request,'index.html',{'group_name':group_name,'chats':chats})



