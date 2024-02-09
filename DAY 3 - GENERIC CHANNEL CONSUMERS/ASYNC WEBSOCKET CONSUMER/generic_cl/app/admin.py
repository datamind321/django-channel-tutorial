from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['msg','timestamp','group']
