from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.fields import IntegerField
from rest_framework.response import Response

from Friends.models import Friend, Story


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    # friend = serializers.SerializerMethodField()
    friend_name = serializers.CharField(source='friend.username', read_only=True)

    class Meta:
        model = Friend
        fields = ('id', 'user', 'friend_name')

    def get_friend(self, obj):
        return obj.user.username


class StorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Story
        fields = ('id', 'user', 'message', 'content', 'created_at', 'updated_at')
