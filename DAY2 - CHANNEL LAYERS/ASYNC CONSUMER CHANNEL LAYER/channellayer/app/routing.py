from django.urls import path 
from app.consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:groupkname>/',ChatAppConsumer.as_asgi()),
]