
from kullanici.models import User,Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = ("first_name","last_name","password","email","il","ilce","phone","adres")
        lookup_field = 'email'
        extra_kwargs = {
            'url': {'lookup_field': 'email'}
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id','image')
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','il','ilce','adres','profile')

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        profile_serializer = ProfileSerializer(instance=instance.profile,data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return super(UserSerializer,self).update(instance,validated_data)