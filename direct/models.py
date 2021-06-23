from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from kullanici.models import User
def val_subject(value):
    if len(value) < 5 :
        raise ValidationError("Mesaj 5 Karakterden Az olamaz")
def val_message(value):
    if len(value) < 25 :
        raise ValidationError("Mesaj 25 Karakterden Az olamaz")
class ChatModel(models.Model):

    message_type = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    priority = models.CharField(max_length=100)
    subject = models.CharField(max_length=150,validators=[val_subject])
    first_message = models.CharField(max_length=250,validators=[val_message])
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.subject
class Message(models.Model):
    chat = models.ForeignKey(ChatModel,on_delete=models.CASCADE)
    msg_text = models.CharField(max_length=250,validators=[val_message])
    is_staff = models.BooleanField(default=False)
    message_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['message_time']
    def __str__(self):
        return self.msg_text
def firstMessageChat(sender,instance,created,**kwargs):
    if created:
        chat = ChatModel.objects.get(id=instance.id)
        firstMessage = chat.first_message
        Message.objects.create(chat=chat,msg_text=firstMessage,is_staff=chat.user.is_staff)


post_save.connect(firstMessageChat,sender=ChatModel)