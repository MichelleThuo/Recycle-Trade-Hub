


from django.urls import path
from .views import InboxView, MyInbox, GetMessages,SendMsg, ProfileDetail, SearchProfile

urlpatterns=[
    path('inbox/<str:user_id>', MyInbox.as_view()), #Get all last msg btn logged in user id=user_id and others
    path('chat/<str:sender_id>/<str:receiver_id>',GetMessages.as_view()),
    path('send/', SendMsg.as_view()),
    path('profile/<int:pk>', ProfileDetail.as_view()),
    path('search/<str:username>',SearchProfile.as_view() ),
]