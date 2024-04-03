from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    # list_editable=['phone', 'bio', 'image']
    list_display=['thumbnail','user', 'bio', 'phone', 'image']


class ChartMessageAdmin(admin.ModelAdmin):
    list_editable=['is_read']
    list_display=['sender', 'receiver', 'message', 'is_read']

admin.site.register(ChatMessage, ChartMessageAdmin)
admin.site.register(Profile, ProfileAdmin)