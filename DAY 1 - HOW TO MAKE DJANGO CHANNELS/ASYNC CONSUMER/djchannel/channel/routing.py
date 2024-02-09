from django.urls import path
from channel.consumers import MyAsyncConsumer


websocket_urlpatterns = [
   path('ws/ac/',MyAsyncConsumer.as_asgi()),
]