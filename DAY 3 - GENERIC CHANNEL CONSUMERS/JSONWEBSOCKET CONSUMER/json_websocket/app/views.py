from django.shortcuts import render,HttpResponse
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.


def index(request,group_name):
    group = Group.objects.filter(name=group_name).first()
    chats=[]
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group.objects.create(name=group_name)

    return render(request,'index.html',{'group_name':group_name,'chats':chats})



# How to send anmessage to client from outside consumer 

def MsgFromOutside(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'railway',
        {
            'type':'chat.message',
            'message':'I am from Outside'
        }
    )

    return HttpResponse('Msg has been sent !')