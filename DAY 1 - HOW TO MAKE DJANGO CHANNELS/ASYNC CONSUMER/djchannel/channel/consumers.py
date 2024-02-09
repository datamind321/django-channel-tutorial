from channels.consumer import AsyncConsumer
import asyncio 



class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print('websocket connect...',event)

        await self.send({
            'type':'websocket.accept',
        })  


    async def websocket_receive(self,event):
        print('Message Received...',event)
        print('Message Received from client: ',event['text'])
        for i in range(20):
            await self.send({
                'type':'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self,event):
        print('websocket disconnect...',event)