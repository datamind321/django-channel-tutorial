from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
import json
from .models import *
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async




class ChatAppSyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print('websocket connected....',event)
        print('Channel Layer: ',self.channel_layer)
        print('Channel Name: ',self.channel_name)
        print('Group Name: ',self.scope['url_route']['kwargs']['groupkname'])
        self.group_name = self.scope['url_route']['kwargs']['groupkname']
        # add the channel to group 
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,   # group-name
            self.channel_name   # channel name
            )
        
        self.send({
            'type':'websocket.accept',
        })

    def websocket_receive(self,event):
        print('message reeived from client',event)
        print('message is: ',event['text'])
        print('message is: ',type(event['text']))    # string type data 
        
        # for chat save in databse first convert to text data into python object

        data = json.loads(event['text'])
        print('Data.....',data) 
        print('Type Of Data...',type(data))
        print('actual msg: ',data['msg'])


        group = Group.objects.get(name=self.group_name)

        # create new chat object 
        chat = Chat(
            message=data['msg'],
            group = group,

        )
        
        chat.save()




        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type':'chat.message',
             'message':event['text'],
            })
        

        
    def chat_message(self,event):
        print(event['message'])       
        print(type(event['message']))

        self.send({
            'type':'websocket.send',
            'text':event['message'],
        })



    def websocket_disconnect(self,event):
        print('websocket disconnected...',event)
        print('Channel Layer: ',self.channel_layer)
        print('Channel Name: ',self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer()
    
