from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
import json
from .models import *
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class ChatAppConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print('websocket connected....',event)
        print('Channel Layer: ',self.channel_layer)
        print('Channel Name: ',self.channel_name)
        print('Group Name: ',self.scope['url_route']['kwargs']['groupkname'])
        self.group_name = self.scope['url_route']['kwargs']['groupkname']
        # add the channel to group 
        await self.channel_layer.group_add(
            self.group_name,   # group-name
            self.channel_name   # channel name
            )
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self,event):
        print('message reeived from client',event)
        print('message is: ',event['text'])
        print('message is: ',type(event['text']))    # string type data 
        
        # for chat save in databse first convert to text data into python object

        data = json.loads(event['text'])
        print('Data.....',data) 
        print('Type Of Data...',type(data))
        print('actual msg: ',data['msg'])
        print(self.scope['user'])

        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:

            # create new chat object 
            chat = Chat(
                message=data['msg'],
                group = group,

            )

            await database_sync_to_async(chat.save)()
            data['user'] = self.scope['user'].username
            print('Data With userName: ',data)


            await self.channel_layer.group_send(self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data),
                })

        else:
            await self.send({
                'type':'websocket.send',
                'text': json.dumps({"msg": "LogIn Required !","user":"unknown"})
            })  

        
    async def chat_message(self,event):
        print(event['message'])       
        print(type(event['message']))

        await self.send({
            'type':'websocket.send',
            'text':event['message'],
        })



    async def websocket_disconnect(self,event):
        print('websocket disconnected...',event)
        print('Channel Layer: ',self.channel_layer)
        print('Channel Name: ',self.channel_name)
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer()
    











