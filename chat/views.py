from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage, Profile
from .serializer import ChartMessageSerializer,ProfileSerializer
from django.db.models import Subquery, Q, OuterRef
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.views.decorators.csrf import csrf_exempt
# Not Useful now
class InboxView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        q=ChatMessage.objects.all()
        data=ChartMessageSerializer(q, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
# Done
class MyInbox(generics.ListAPIView):
    serializer_class=ChartMessageSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user_id=self.request.user
        message=ChatMessage.objects.filter(id__in=Subquery(User.objects.filter(Q(sender__receiver=user_id)|Q(receiver__sender=user_id)).distinct().annotate(last_msg=Subquery(ChatMessage.objects.filter(Q(sender=OuterRef('id'), receiver=user_id)|Q(receiver=OuterRef('id'), sender=user_id)).order_by('-id')[:1].values_list('id', flat=True))).values_list('last_msg', flat=True).order_by('-id'))).order_by('-id')
        return  message
# Done
    
class GetMessages(generics.ListAPIView):
    serializer_class=ChartMessageSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        sender_id=self.request.user.id
        receiver_id=self.kwargs['receiver_id']
        read=ChatMessage.objects.filter(is_read=False, sender=receiver_id, receiver=sender_id)
        read.update(is_read=True)
        messages=ChatMessage.objects.filter(sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id])
        return messages
# Done  
class SendMsg(generics.CreateAPIView):
    serializer_class=ChartMessageSerializer
    # permission_classes=[IsAuthenticated]

# Not important now
class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    queryset= Profile.objects.all()
    permission_classes=[IsAuthenticated]

# Will implement later
class SearchProfile(generics.ListAPIView):
    serializer_class=ProfileSerializer
    queryset=Profile.objects.all()
    # permission_classes=[]
    def list(self, request, *args, **kwargs):
        username=self.kwargs['username']
        logged_in_user=self.request.user
        users=Profile.objects.filter(Q(user__username__icontains=username)| Q(user__email__icontains=username))
        # & ~Q(user=logged_in_user) 

        if not users.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data="{User not fund}")
        serializer=self.get_serializer(users, many=True).data
        return Response(serializer)
    

