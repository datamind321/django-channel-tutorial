from django.urls import path
from app.views import *

urlpatterns = [
    path('<str:group_name>/',index,name='index'),
   
]