"""
Blog App URL Configuration
"""
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostListCreateView, PostRetrieveUpdateView, CommentListCreateView, CommentRetrieveUpdateView

urlpatterns = [
    path('list-create/', PostListCreateView.as_view(), name='list-create'),
    path('<int:pk>/retrieve-update/', PostRetrieveUpdateView.as_view(), name='retrieve-update'),
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    path('<int:pk>/comments/edit', CommentRetrieveUpdateView.as_view(), name='comments-edit'),
    path('token/', obtain_auth_token, name='obtain-token'),
]
