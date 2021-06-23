from direct.models import ChatModel,Message
from rest_framework import serializers

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ('id','message_type','priority','subject','first_message',)
class MessageSerializer(serializers.ModelSerializer):
   # chat_id = serializers.IntegerField()
    class Meta:
        model = Message

        fields = ('msg_text','is_staff','message_time')
