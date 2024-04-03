


from rest_framework import serializers
from .models import ChatMessage, Profile
from django.contrib.auth.models import User
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['username','first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user_details=UserSerializer(read_only=True)
    class Meta:
        model=Profile
        fields='__all__'#['user','bio','image',user_details]

class ChartMessageSerializer(serializers.ModelSerializer):
    receiver_profile=ProfileSerializer(read_only=True)
    sender_profile=ProfileSerializer(read_only=True)
    msg_count=serializers.SerializerMethodField()
    class Meta:
        model=ChatMessage
        fields=['id', 'user', 'sender', 'receiver', 'message', 'date', 'is_read','receiver_profile', 'sender_profile','msg_count']

    def get_msg_count(self, obj):
        return ChatMessage.objects.filter(is_read=False, sender=obj.sender, receiver=obj.receiver).count()