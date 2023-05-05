from rest_framework.routers import DefaultRouter

from Friends.views import FriendViewSet, StoryViewSet, LikeViewSet, CommentViewSets

# from .views import UserRegistrationViewSet
router = DefaultRouter()
router.register(r'friends', FriendViewSet)
router.register('stories', StoryViewSet, basename='stories')
router.register('like', LikeViewSet, basename='like')
router.register('comment', CommentViewSets, basename='comments')

from django.urls import path

# urlpatterns = [
#     path('register/', registration_view, name='register'),
#     path('login/', login_view, name='login'),
# ]
