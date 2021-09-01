from django.db import models
from django.utils import timezone
# Create your models here.

class Contract(models.Model):
    date = models.CharField(max_length=10)
    location = models.TextField()
    item = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    chats = models.TextField(default="채팅로그가 등록되지 않았습니다.")

    def show_Contract(self):
        return

    def __str__(self):
        return self.item + " " + self.created_at.strftime('%Y-%m-%d %H:%M')



class Message(models.Model):
    talker = models.CharField(max_length=1)
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {'talker' : self.talker, 'msg' : self.msg, 'timestamp' : self.timestamp.strftime('%Y-%m-%d %H:%M')}