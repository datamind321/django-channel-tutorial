from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
from channels.db import database_sync_to_async

class MyJSONWebSocket(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']



        
        await self.channel_layer.group_add(
           self.group_name,
           self.channel_name,
        )

        await self.accept()      
       
    
    async def receive_json(self, content,**kwargs):
        print('received from client',content)

       
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        print('My group Name is: ',group) 
        msg = content['msg']


        if self.scope['user'].is_authenticated:
            chat = Chat(msg = msg , group=group )
            await database_sync_to_async(chat.save)() 


            await self.channel_layer.group_send(self.group_name,{
                'type':'chat.message',
                'message':content['msg'],
            })

        else:
            await self.send_json({'msg':"login required !"})



    async def chat_message(self,event):
        print('msg: ',event['message']) 
        await self.send_json({'msg':event['message']})   

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        return super().disconnect(code)
    