from django.urls import path 
from app import views

urlpatterns = [
    path('<str:group_name>/',views.index,name='home'),
]