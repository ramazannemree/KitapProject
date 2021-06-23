from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView,get_object_or_404
from .serializers import RegisterSerializer,UserSerializer

from kullanici.models import User
from .permissions import NotAuthenticated
from rest_framework.response import Response
from time import time
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    #permission_classes = [NotAuthenticated,]
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'
    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'
    #permission_classes = [NotAuthenticated,]


class TestApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)

class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)