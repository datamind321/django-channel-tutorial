from django.urls import path 
from app.consumers import MyWebSocketConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:groupkaname>/',MyWebSocketConsumer.as_asgi()),
]