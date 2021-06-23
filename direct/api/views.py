from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView,get_object_or_404
from .serializers import ChatSerializer,MessageSerializer
from django.shortcuts import get_object_or_404
from direct.models import ChatModel,Message
from kullanici.models import User
from kullanici.api.permissions import NotAuthenticated
from rest_framework.response import Response
from time import time
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins,serializers
class ChatViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChatSerializer
    def get_queryset(self):
        return ChatModel.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageViewset(mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = MessageSerializer
    def get_queryset(self):
        try:

            chat = ChatModel.objects.get(pk=self.kwargs['id'])
        except:
            raise serializers.ValidationError("Chat Bulunamadı")
        if chat.user != self.request.user:
            raise serializers.ValidationError("Başkasının mesajını göremezsiniz.")
        return Message.objects.filter(chat=chat)
    def perform_create(self, serializer):
        #chat_id = serializer.chat_id
        try:
            chat = ChatModel.objects.get(pk=self.kwargs["id"])
        except:
            raise serializers.ValidationError("Chat Bulunamadı")
        if chat.user != self.request.user:
            raise serializers.ValidationError("Başkasının mesajını göremezsiniz.")

        serializer.save(chat=chat,is_staff=self.request.user.is_staff)
