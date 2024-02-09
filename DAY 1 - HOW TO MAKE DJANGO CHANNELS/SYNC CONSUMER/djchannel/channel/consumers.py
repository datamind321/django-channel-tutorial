from channels.consumer import SyncConsumer
import asyncio 
import json


class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print('websocket connect...',event)

        self.send({
            'type':'websocket.accept',
        })  


    def websocket_receive(self,event):
        print('Message Received...',event)
        print('Message Received from client: ',event['text'])
        for i in range(20):
            self.send({
                'type':'websocket.send',
                'text': json.dumps({"count":i})
            })
            asyncio.sleep(1)

    def websocket_disconnect(self,event):
        print('websocket disconnect...',event)



