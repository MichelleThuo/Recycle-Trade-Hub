from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(max_length=100)
    image=models.ImageField(upload_to='user_profile', default='profile.jpg', blank=True)
    phone=models.CharField(max_length=15, blank=True)

    @property
    def user_details(self):
        user_details=User.objects.get(username=self.user.username)
        return user_details
    @property
    def thumbnail(self):
        return  mark_safe(f"<img src='{self.image.url}' width='50px' height='50px' style='border-radius:50%'/>")

class ChatMessage(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message=models.CharField(max_length=100)
    is_read=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural="Message"

    def __str__(self):
        return f"{self.sender} to {self.receiver} on {self.date}"
    
    @property
    def sender_profile(self):
        sender_profile=Profile.objects.get(user=self.sender)
        return sender_profile   
     
    @property
    def receiver_profile(self):
        receiver_profile=Profile.objects.get(user=self.receiver)
        return receiver_profile
    
