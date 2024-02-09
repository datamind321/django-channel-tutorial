from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import *



class MyWebSocketConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        return super().connect()
    
    def receive(self, text_data=None, bytes_data=None):
        print('Received Message from client: ',text_data)
        print('Type Received Message from client: ',type(text_data))
        data = json.loads(text_data)  # convert to python dict 
        message = data['msg']


        

        group = Group.objects.get(name=self.group_name)

        if self.scope['user'].is_authenticated:
            chat = Chat(msg=message,group=group)
            chat.save()  


            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                'message':message,
            }) 

        else:
             self.send(json.dumps({'msg':'login required'}))
             


            

    def chat_message(self,event):
            print('hi this msg received: ',event['message'])
            
            self.send(json.dumps({
                'msg':event['message'],
            })) 
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        return super().disconnect(code)