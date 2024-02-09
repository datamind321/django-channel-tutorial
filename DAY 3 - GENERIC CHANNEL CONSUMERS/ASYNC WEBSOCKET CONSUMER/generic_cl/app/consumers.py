from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import *



class MyWebSocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        print('Received Message from client: ',text_data)
        print('Type Received Message from client: ',type(text_data))
        data = json.loads(text_data)  # convert to python dict 
        message = data['msg']


        

        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)

        if self.scope['user'].is_authenticated:
            chat = Chat(msg=message,group=group)
            await database_sync_to_async(chat.save)()  


            await self.channel_layer.group_send(self.group_name,{
                'type':'chat.message',
                'message':message,
            }) 

        else:
             await self.send(json.dumps({'msg':'login required'}))
             


            

    async def chat_message(self,event):
            print('hi this msg received: ',event['message'])
            
            await self.send(json.dumps({
                'msg':event['message'],
            })) 
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        print('Disconnected...',code)
        