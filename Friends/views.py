# from django.contrib.auth.models import User
import permission as permission
from django.contrib.auth.models import User
from django.http import request
from rest_framework.authtoken.models import TokenProxy
from crontab import CronTab
from datetime import datetime, timedelta
from django_crontab import crontab
from django.utils import timezone

from rest_framework import status, viewsets, serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Friend, Story
from .serializers import UserSerializer, LoginSerializer, FriendSerializer, StorySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password')
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    # authentication_classes = [JWTAuthentication]
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user
        return Friend.objects.filter(user=user_id)

    # def create(self, request, *args, **kwargs):
    #     user_username = self.request.data.get('user')
    #     user = User.objects.get(nusername=user_username)
    #     friend_username = self.request.data.get('friend')
    #     friend = User.objects.get(username=friend_username)
    #     if Friend.objects.filter(user=user, friend=friend).exists():
    #         raise serializers.ValidationError('Friend already exists')
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user_username = self.request.data.get('user')
        user = User.objects.get(username=user_username)
        friend_username = self.request.data.get('friend')
        friend = User.objects.get(username=friend_username)
        if Friend.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError('Friend already exists')
        serializer.save(user=user, friend=friend)

    from rest_framework import viewsets, status
    from rest_framework.response import Response

    from .models import Story
    from .serializers import StorySerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Story.objects.filter(user=user_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def like(self, request, *args, **kwargs):
        story = self.get_object()
        liked_story = request.data.get('like')
        if liked_story:
            story.like = Story.objects.get(id=liked_story)
            story.save()
            return Response({'status': 'success'})
        return Response({'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)

    def comment(self, request, *args, **kwargs):
        story = self.get_object()
        comment = request.data.get('comment')
        if comment:
            comment_story = Story.objects.create(user=request.user, message=comment)
            story.comments = comment_story
            story.save()
            return Response({'status': 'success'})
        return Response({'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)

    def reply(self, request, *args, **kwargs):
        story = self.get_object()
        reply = request.data.get('reply')
        if reply:
            reply_story = Story.objects.create(user=request.user, message=reply)
            story.reply = reply_story
            story.save()
            return Response({'status': 'success'})
        return Response({'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)

    # class StoryViewSet(viewsets.ModelViewSet):
    #     queryset = Story.objects.all()
    #     serializer_class = StorySerializer
    #     permission_classes = [IsAuthenticated]
    #
    #     def get_queryset(self):
    #         user_id = self.request.user.id
    #         return Story.objects.filter(user=user_id)
    #
    #     def perform_create(self, serializer):
    #         serializer.save(user=self.request.user)
    #
    #     # def create(self, request, *args, **kwargs):
    #     #     serializer = self.get_serializer(data=request.data)
    #     #     serializer.is_valid(raise_exception=True)
    #     #     self.perform_create(serializer)
    #     #     headers = self.get_success_headers(serializer.data)
    #     #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    #     @action(detail=True, methods=['post'])
    #     def like(self,request,pk=None):
    #         story = self.get.object()
    #         user = request.user
    #         # Check if the user has already liked the story
    #         if story.like.filter(id=user.id).exists():
    #             story.like.remove(user)
    #         else:
    #             story.like.add(user)
    #
    #             serializer = self.get_serializer(story)
    #             return Response(serializer.data)
    #
    #
    #
    #

    def delete_old_stories(self):
        Story.objects.filter(created_at__lte=datetime.now() - timedelta(minutes=5)).delete()

        # old_stories = Story.objects.filter(timestamp__lte=timezone.now() - timezone.timedelta(minutes=5))
