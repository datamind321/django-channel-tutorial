from django.urls import path 
from app.consumers import MyJSONWebSocket

websocket_urlpatterns = [
    path('ws/chat/<str:groupkaname>/',MyJSONWebSocket.as_asgi()),
]