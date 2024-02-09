from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *

class MyJSONWebSocket(JsonWebsocketConsumer):

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']



        
        async_to_sync(self.channel_layer.group_add)(
           self.group_name,
           self.channel_name,
        )

        self.accept()      
       
    
    def receive_json(self, content,**kwargs):
        print('received from client',content)

       
        group = Group.objects.get(name=self.group_name)
        print('My group Name is: ',group) 
        msg = content['msg']


        if self.scope['user'].is_authenticated:
            chat = Chat(msg = msg , group=group )
            chat.save() 


            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                'message':content['msg'],
            })

        else:
            self.send_json({'msg':"login required !"})

    def chat_message(self,event):
        print('msg: ',event['message']) 
        self.send_json({'msg':event['message']})   

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard(self.group_name,self.channel_name))
        return super().disconnect(code)
    