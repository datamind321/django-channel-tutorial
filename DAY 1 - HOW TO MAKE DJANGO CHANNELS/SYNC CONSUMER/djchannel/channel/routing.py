from django.urls import path
from channel.consumers import MySyncConsumer  


websocket_urlpatterns = [
    path('ws/sc/',MySyncConsumer.as_asgi()),
   
]