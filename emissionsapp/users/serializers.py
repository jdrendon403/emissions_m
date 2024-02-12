from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)

    class Meta:

        model = User
        fields = (
            "username",
            "email",
            "groups",
        )


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=5)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("invalid credentials")
        self.context["user"] = user
        return data
    
    def create(self, data):
        token, created= Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key
    
class LogoutSerializer(serializers.Serializer):

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("invalid credentials")
        self.context["user"] = user
        print(self.context["user"])
        return data
    
    def create(self, data):
        print(self.context["user"])
        token, created= Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key
