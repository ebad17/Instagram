from django.contrib.auth.models import User
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Friend, Story, Like, Comment
from .serializers import UserSerializer, LoginSerializer, StorySerializer, FriendSerializer, LikeSerializer, \
    CommentSerializer


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
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user
        return Friend.objects.filter(user=user_id)

    def perform_create(self, serializer):
        user_username = self.request.data.get('user')
        user = User.objects.get(username=user_username)
        friend_username = self.request.data.get('friend')
        friend = User.objects.get(username=friend_username)
        if Friend.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError('Friend already exists')
        serializer.save(user=user, friend=friend)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        story = self.get_object()
        likes = story.story_likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['GET'])
    def user_likes(self, request):
        user = request.user
        likes = Like.objects.filter(user=user)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        story_id = request.data.get('story')
        if not story_id:
            return Response({'detail': 'Story ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return Response({'detail': 'Story not found.'}, status=status.HTTP_404_NOT_FOUND)

        like_exists = Like.objects.filter(user=request.user, story=story).exists()
        if like_exists:
            # Unlike the story
            Like.objects.filter(user=request.user, story=story).delete()
            return Response({'detail': 'Story unliked successfully.'}, status=status.HTTP_200_OK)

        # Like the story
        new_like = Like(user=request.user, story=story)
        new_like.save()

        return Response({'detail': 'Story liked successfully.'}, status=status.HTTP_201_CREATED)


class CommentViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(reply=None)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

